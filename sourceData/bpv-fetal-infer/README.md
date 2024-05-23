# Fetal Brain Parenchyma Ssegmentation (BPV)

## Getting Started

1. Install [Miniconda](https://docs.anaconda.com/free/miniconda/miniconda-install/) (Recommended) or [Anaconda](https://www.anaconda.com/download)

2. Create environment

+ Option 1: Create [conda](https://docs.conda.io/) environment with exported file in [Ubuntu](https://ubuntu.com/)

```shell
conda env create --file bpv_env.yaml
```

+ Option 2: Re-create [conda](https://docs.conda.io/) environment and install the dependencies. (Ubuntu, Windows)

```shell
conda create -n bpv python=3.10
conda install pytorch==1.13.1 torchvision==0.14.1 pytorch-cuda=11.6 -c pytorch -c nvidia
pip install -r requirements.txt
```

## Run Inference

Note: **ONLY** the coronal images are supported for the time being.

+ inference on single NIFTI (.nii/.nii.gz) file

```shell
python infer_seg.py --sw_batch_size 2 --overlap 0.5 --num_workers 2 --nifti_path ${nifti_path} --output ${output_dir} --checkpoint ${ckpt_path}
```

```shell
--sw_batch_size   # batch size in sliding window inference, set larger may make inference faster, set lower if GPU memory is not enough
--overlap         # overlap rate for sliding window inference, set larger may improve precision, default 0.5
--num_workers     # number of workers (processses) to load data. set to 0 will load data in the main process

--nifti_path      # the path of the single NIFTI file
```

+ inference on multi NIFTI files with a infer list file

```shell
python infer_seg.py --sw_batch_size 2 --overlap 0.5 --num_workers 2 --nifti_list ${nifti_list} --output ${output_dir} --checkpoint ${ckpt_path}
```

```shell
--nifti_list      # the path of the NIFTI file list, see example_data/infer_list.json for example
```

+ inference on subject folders with DICOM (.dcm) files

```shell
python infer_seg.py --sw_batch_size 2 --overlap 0.5 --num_workers 2 --dicom_dir ${dicom_list} --dicom_filter 'SSh_TSE SENSE_cor' --save_temp_nifti --output ${output_dir} --checkpoint ${ckpt_path}
```

```shell
--dicom_dir       # the path of the DICOM directory, see the structure of example_data/dicom for example
--dicom_filter    # to filter DICOM files by the Series description
--save_temp_nifti # the process will first convert dicom files to nifti files, set whether to save the temp nifti files
```

+ see usage examples in [run_infer.sh](./run_infer.sh)


