import nibabel as nib
import numpy as np
import os
import cv2
from PIL import Image, ImageEnhance

path = "input_files/1716305709029_2001477996-28W_cor_T2w.nii.gz"
path1 = "infer_result/1716305709029_2001477996-28W_cor_T2w_seg.nii.gz"

basePath = os.path.dirname(__file__)  # 当前文件所在路径print(basePath)
upload_path = os.path.join(basePath, 'output_result','output_result_01')
upload_path = os.path.abspath(upload_path)  # 将路径转换为绝对路径print("绝对路径：",upload_path)

nii = nib.load(path)
nii1 = nib.load(path1)

###
header_dict = dict(nii.header)
pixdim = header_dict["pixdim"][1:4]
###

data = nii.get_fdata()
min_val = np.min(data)
max_val = np.max(data)
normalized_data = (data - min_val) / (max_val - min_val)

data1 = nii1.get_fdata()
min_val1 = np.min(data1)
max_val1 = np.max(data1)
normalized_data1 = (data1 - min_val1) / (max_val1 - min_val1)
# 遍历每张图片
for i in range(normalized_data.shape[0]):
    # 获取第 i 张图片的数据
    image_array = normalized_data[i, :, :] * 255
    image_array_1 = normalized_data1[i, :, :] * 255

    # 将灰度图image_array转换为RGB图像数组
    rgb_image = np.zeros((image_array.shape[0], image_array.shape[1], 3), dtype=np.uint8)
    rgb_image[:, :, 0] = image_array.astype(np.uint8)  # 红色通道
    rgb_image[:, :, 1] = image_array.astype(np.uint8)  # 绿色通道
    rgb_image[:, :, 2] = image_array.astype(np.uint8)  # 蓝色通道

    # 将黑绿图image_array_1转换为RGB图像数组
    rgb_image_1 = np.zeros((image_array_1.shape[0], image_array_1.shape[1], 3), dtype=np.uint8)
    rgb_image_1[:, :, 1] = image_array_1.astype(np.uint8)  # 绿色通道

    # image_01 = Image.fromarray(rgb_image)
    # image_02 = Image.fromarray(rgb_image_1)

    cv2.addWeighted(rgb_image_1, 0.15, rgb_image, 0.85,
                    0, rgb_image)

    # # 创建新的RGB图像数组，将灰度图作为底层，黑绿图作为上层
    # combined_image = np.maximum(rgb_image, rgb_image_1)  # 取两个图像数组中对应位置像素的较大值

    # 将 ndarray 转换为 PIL Image 对象
    image = Image.fromarray(rgb_image)

    # 保存图像到文件（假设文件名以数字命名）
    file_name = f"image_{i}.png"
    image.save(rf"{upload_path}\{file_name}")

# for i in range(normalized_data.shape[2]):
#     # 获取第 i 个图像的数据
#     image_array = normalized_data[:, :, i] * 255
#     image_array_1 = normalized_data1[:, :, i] * 255
#
#     # 将灰度图像数组转换为 RGBA 图像数组，并设置 alpha 通道值
#     rgba_image = cv2.merge([image_array.astype(np.uint8)] * 3 + [np.ones_like(image_array).astype(np.uint8) * 255])
#
#     # 将灰度图像数组转换为 RGBA 图像数组，并设置 alpha 通道值
#     alpha_channel = (image_array_1 * 255).astype(np.uint8)
#     rgba_image_1 = cv2.merge([image_array_1.astype(np.uint8)] * 3 + [alpha_channel])
#
#     # 调整 rgba_image_1 的 alpha 通道，使其部分透明
#     rgba_image_1[:, :, 3] = alpha_channel
#
#     # 使用 alpha 混合将 rgba_image_1 以半透明形式覆盖 rgba_image
#     blended = cv2.addWeighted(rgba_image_1, 0.5, rgba_image, 0.5, 0)
#
#     # 保存混合后的图像到文件（假设文件名是按编号命名的）
#     file_name = f"image_{i}.png"
#     cv2.imwrite(f"{upload_path}/{file_name}", blended)

# for i in range(data.shape[2]):
#     # 获取第 i 张图片的数据
#     image_array = data[:, :, i]*255
#
#     # 将 ndarray 转换为 PIL Image 对象
#     image = Image.fromarray(image_array.astype('uint8'))  # 注意：转换为 uint8 类型
#
#     # 调整对比度
#     contrast_enhancer = ImageEnhance.Contrast(image)
#     image = contrast_enhancer.enhance(1.5)  # 调整对比度为原始的1.5倍
#
#     # 调整亮度
#     brightness_enhancer = ImageEnhance.Brightness(image)
#     image = brightness_enhancer.enhance(1.2)  # 调整亮度为原始的1.2倍
#
#     # 保存图像到文件（假设文件名以数字命名）
#     file_name = f"image_{i}.png"
#     image.save(rf"{upload_path}\{file_name}")
#
#     print(rf"Image {i + 1} saved as {upload_path}\{file_name}")

# print(data)
print(pixdim)

