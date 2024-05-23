import argparse
from pathlib import Path
from tqdm import tqdm
import json
import shutil

import torch
from monai.inferers import sliding_window_inference
from monai.data import Dataset, DataLoader, decollate_batch
from monai.networks.nets import DynUNet

from utils.data_transforms import get_test_transform, infer_post_transforms
from utils.logger import create_logger
from utils.dicom_utils import convert_subject


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--nifti_path', type=str, default=None, help='Path of the raw NIFTI file (.nii, .nii.gz)')
    parser.add_argument('--nifti_list', type=str, default=None, help='Path of JSON file with list of path of NIFTI files')
    parser.add_argument('--dicom_dir', type=str, default=None, help='Path of directory with DICOM series files')
    parser.add_argument('--dicom_filter', type=str, default='SSh_TSE SENSE_cor', help='filter files to process by matching DICOM SeriesDescription')
    parser.add_argument('--save_temp_nifti', action='store_true', default=False, help='whether to save the temp ')
    parser.add_argument('--output', type=str, required=True, help='Directory path of inference output folder')
    parser.add_argument('--checkpoint', type=str, required=True, help='Path of model checkpoint')

    parser.add_argument('--sw_batch_size', type=int, default=2, help='Batch size for sliding window inference')
    parser.add_argument('--overlap', type=float, default=0.5, help='Sub-volume overlapped percentage')
    parser.add_argument("--norm_name", default="instance", type=str, help="normalization name")
    parser.add_argument('--num_workers', type=int, default=2, help='Number of workers')

    parser.add_argument("--in_channels", default=1, type=int, help="number of input channels")
    parser.add_argument("--out_channels", default=2, type=int, help="number of output channels")

    return parser.parse_args()


def main():
    assert torch.cuda.is_available()

    args = get_args()
    args.output = Path(args.output)
    args.output.mkdir(parents=True, exist_ok=True)

    logger = create_logger(name="bpv-infer")
    args.logger = logger

    test_transforms = get_test_transform(args)
    post_transforms = infer_post_transforms(test_transforms, args, save_pred=True)

    if args.nifti_path is not None:
        data_path = args.nifti_path
        data_type = "Single NIFTI"
        test_list = [{"image": data_path}]
    elif args.nifti_list is not None:
        data_path = args.nifti_list
        data_type = "List NIFTI"
        with open(data_path, 'r') as fp:
            test_dict = json.load(fp)
            data_root = Path(test_dict["data_root"])
            test_list = [{"image": data_root / p["image"]} for p in test_dict["test"]]
    elif args.dicom_dir is not None:
        data_path = args.dicom_dir
        data_type = f"DICOM Dir ({args.dicom_filter})"
        temp_nifti_dir = args.output / "temp_nifti"
        temp_nifti_dir.mkdir(parents=True, exist_ok=True)
        convert_subject(data_path, temp_nifti_dir, description_filter=args.dicom_filter, reorient=False)
        test_list = [{"image": p} for p in temp_nifti_dir.glob("*.nii.gz")]
    else:
        raise RuntimeError("data_path is needed.")

    test_dataset = Dataset(data=test_list, transform=test_transforms)
    test_loader = DataLoader(
        dataset=test_dataset,
        batch_size=1,
        shuffle=False,
        num_workers=args.num_workers,
        pin_memory=True
    )

    logger.info(f"Loaded data {data_type} from {data_path}")

    model = DynUNet(
        spatial_dims=3,
        in_channels=1,
        out_channels=2,
        kernel_size=[(3, 3, 3)] * 5,
        strides=[(1, 1, 1)] + [(2, 2, 1)] * 4,
        upsample_kernel_size=[(2, 2, 1)] * 4,
        filters=[32, 64, 128, 256, 512],
        norm_name=args.norm_name,
        res_block=True
    ).cuda()

    checkpoint = torch.load(args.checkpoint, map_location="cpu")
    model.load_state_dict(checkpoint["model"])

    run_infer(test_loader, model, post_transforms, args)

    if data_type.startswith("DICOM Dir") and not args.save_temp_nifti:
        shutil.rmtree(temp_nifti_dir)


@torch.no_grad()
def run_infer(infer_loader: DataLoader, model: torch.nn.Module, post_transforms, args):
    model.eval()

    epoch_iterator = tqdm(infer_loader, desc=f"Inference", dynamic_ncols=True)

    for batch in epoch_iterator:
        infer_inputs: torch.Tensor = batch["image"]
        infer_inputs = infer_inputs.cuda()

        batch["pred"] = sliding_window_inference(
            inputs=infer_inputs,
            roi_size=args.spatial_size,
            sw_batch_size=args.sw_batch_size,
            predictor=model,
            overlap=args.overlap
        )

        post_infer = [post_transforms(x) for x in decollate_batch(batch)]


if __name__ == "__main__":
    main()
