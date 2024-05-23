export CUDA_VISIBLE_DEVICES=0
export TZ=Asia/Shanghai

ckpt_path=./model_best.pt
output_dir=./infer_result

python infer_seg.py --sw_batch_size 2 --overlap 0.5 --num_workers 2 \
    --nifti_path ./example_data/nifti/sub_029_28W/029_2001477996-28W_cor_T2w.nii.gz \
    --output ${output_dir} \
    --checkpoint ${ckpt_path}

python infer_seg.py --sw_batch_size 2 --overlap 0.5 --num_workers 2 \
    --nifti_list ./example_data/infer_list.json \
    --output ${output_dir} \
    --checkpoint ${ckpt_path}

python infer_seg.py --sw_batch_size 2 --overlap 0.5 --num_workers 2 \
    --dicom_dir ./example_data/dicom \
    --dicom_filter 'SSh_TSE SENSE_cor' \
    --output ${output_dir} \
    --checkpoint ${ckpt_path} \
    --save_temp_nifti

python infer_seg.py --sw_batch_size 2 --overlap 0.5 --num_workers 2 --dicom_dir .\example_data\dicom --dicom_filter 'SSh_TSE SENSE_cor' --output .\infer_result --checkpoint .\model_best.pt --save_temp_nifti
