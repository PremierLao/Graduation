from flask import Flask, request, render_template,send_file,jsonify
from flask_cors import CORS
import calendar,time,os
import cv2
import subprocess
import nibabel as nib
from PIL import Image
import numpy as np
import shutil
import json
import time
import threading
app = Flask(__name__)
cors = CORS(app,resources={r"/*" : {"origins" : "*"}})
@app.route('/open_folder', methods=['GET'])
def open_folder():
    basePath = os.path.dirname(__file__)  # 当前文件所在路径print(basePath)
    upload_path = os.path.join(basePath, 'output_result')
    upload_path = os.path.abspath(upload_path)  # 将路径转换为绝对路径print("绝对路径：",upload_path)
    os.system(f'explorer "{upload_path}"') # 在macOS上使用"open"命令，Windows上使用"start"命令
    return 'Folder opened successfully!'
@app.route("/clear_output")
def clear_output():
        basePath = os.path.dirname(__file__)  # 当前文件所在路径print(basePath)
        upload_path_01 = os.path.join(basePath, 'output_result', 'output_result_01')
        upload_path_01 = os.path.abspath(upload_path_01)  # 将路径转换为绝对路径print("绝对路径：",upload_path)
        upload_path_02 = os.path.join(basePath, 'output_result', 'output_result_02')
        upload_path_02 = os.path.abspath(upload_path_02)  # 将路径转换为绝对路径print("绝对路径：",upload_path)
        upload_path_03 = os.path.join(basePath, 'output_result', 'output_result_03')
        upload_path_03 = os.path.abspath(upload_path_03)  # 将路径转换为绝对路径print("绝对路径：",upload_path)
        upload_path_04 = os.path.join(basePath, 'infer_result')
        upload_path_04 = os.path.abspath(upload_path_04)  # 将路径转换为绝对路径print("绝对路径：",upload_path)
        upload_path_05 = os.path.join(basePath, 'input_files')
        upload_path_05 = os.path.abspath(upload_path_05)  # 将路径转换为绝对路径print("绝对路径：",upload_path)

        def clear_folder(upload_path):
                try:
                        # 清空文件夹内容
                        for filename in os.listdir(upload_path):
                                file_path = os.path.join(upload_path, filename)
                                try:
                                        if os.path.isfile(file_path) or os.path.islink(file_path):
                                                os.unlink(file_path)
                                        elif os.path.isdir(file_path):
                                                shutil.rmtree(file_path)
                                except Exception as e:
                                        return f"Error: {e}"

                        return "Folder content cleared successfully!"
                except Exception as e:
                        return f"Error: {e}"

        def folder_has_files(folder_path):
                # 检查文件夹是否存在
                if not os.path.exists(folder_path):
                        return False

                # 检查文件夹是否为空
                if not os.listdir(folder_path):
                        return False

                return True

        # 示例用法
        if folder_has_files(upload_path_01):
                clear_folder(upload_path_01)
        else:
                print("The folder is empty or does not exist.")
        if folder_has_files(upload_path_02):
                clear_folder(upload_path_02)
        else:
                print("The folder is empty or does not exist.")
        if folder_has_files(upload_path_03):
                clear_folder(upload_path_03)
        else:
                print("The folder is empty or does not exist.")
        if folder_has_files(upload_path_04):
                clear_folder(upload_path_04)
        else:
                print("The folder is empty or does not exist.")
        if folder_has_files(upload_path_05):
                clear_folder(upload_path_05)
        else:
                print("The folder is empty or does not exist.")
        return {
                'code': 200,
                'messsge': "文件清除成功",
        }
@app.route('/split_Prototype',methods=['POST'])
def split_Prototype():
        basePath = os.path.dirname(__file__)  # 当前文件所在路径print(basePath)
        upload_path_01 = os.path.join(basePath, 'output_result', 'output_result_01')
        upload_path_01 = os.path.abspath(upload_path_01)  # 将路径转换为绝对路径print("绝对路径：",upload_path)
        upload_path_02 = os.path.join(basePath, 'output_result', 'output_result_02')
        upload_path_02 = os.path.abspath(upload_path_02)  # 将路径转换为绝对路径print("绝对路径：",upload_path)
        upload_path_03 = os.path.join(basePath, 'output_result', 'output_result_03')
        upload_path_03 = os.path.abspath(upload_path_03)  # 将路径转换为绝对路径print("绝对路径：",upload_path)
        # 获取上传文件数据
        file = request.files.get('file')
        if file is None:
                # 表示没有发送文件
                return {
                        'message': "文件上传失败"
                }
        file_name = file.filename  # print(file.filename)
        # 获取前缀（文件名称）print(os.path.splitext(file_name)[0])
        # 获取后缀（文件类型）print(os.path.splitext(file_name)[-1])
        suffix = os.path.splitext(file_name)[-1]  # 获取文件后缀（扩展名）
        nowTime = calendar.timegm(time.gmtime())  # 获取当前时间戳改文件名print(nowTime)
        upload_path = os.path.join(basePath, 'input_files',
                                   str(nowTime))
        upload_path = os.path.abspath(upload_path)  # 将路径转换为绝对路径print("绝对路径：",upload_path)
        file.save(upload_path + file_name)  # 保存文件
        path = upload_path + file_name
        nii = nib.load(path)
        # 获取分辨率
        header_dict = dict(nii.header)
        pixdim = header_dict["pixdim"][1:4]
        pixdim_list = pixdim.tolist()  # 将 ndarray 转换为 Python 列表
        json_data = json.dumps({'data': pixdim_list})  # 将数据序列化为 JSON 格式
        # 将data归一化
        data = nii.get_fdata()
        min_val = np.min(data)
        max_val = np.max(data)
        normalized_data = (data - min_val) / (max_val - min_val)
        file_paths_01 = []
        file_paths_02 = []
        file_paths_03 = []
        for i in range(normalized_data.shape[0]):
                # 获取第 i 张图片的数据
                image_array = normalized_data[i, :, :] * 255

                # 将灰度图image_array转换为RGB图像数组
                rgb_image = np.zeros((image_array.shape[0], image_array.shape[1], 3), dtype=np.uint8)
                rgb_image[:, :, 0] = image_array.astype(np.uint8)  # 红色通道
                rgb_image[:, :, 1] = image_array.astype(np.uint8)  # 绿色通道
                rgb_image[:, :, 2] = image_array.astype(np.uint8)  # 蓝色通道

                image = Image.fromarray(rgb_image)

                # 保存图像到文件（假设文件名以数字命名）
                file_name = f"image_01_{i}.png"
                image.save(rf"{upload_path_01}\{file_name}")
                file_paths_01.append(rf"{upload_path_01}\{file_name}")

        for i in range(normalized_data.shape[1]):
                # 获取第 i 张图片的数据
                image_array = normalized_data[:, i, :] * 255

                # 将灰度图image_array转换为RGB图像数组
                rgb_image = np.zeros((image_array.shape[0], image_array.shape[1], 3), dtype=np.uint8)
                rgb_image[:, :, 0] = image_array.astype(np.uint8)  # 红色通道
                rgb_image[:, :, 1] = image_array.astype(np.uint8)  # 绿色通道
                rgb_image[:, :, 2] = image_array.astype(np.uint8)  # 蓝色通道

                image = Image.fromarray(rgb_image)

                # 保存图像到文件（假设文件名以数字命名）
                file_name = f"image_02_{i}.png"
                image.save(rf"{upload_path_02}\{file_name}")
                file_paths_02.append(rf"{upload_path_02}\{file_name}")

        for i in range(normalized_data.shape[2]):
                # 获取第 i 张图片的数据
                image_array = normalized_data[:, :, i] * 255

                # 将灰度图image_array转换为RGB图像数组
                rgb_image = np.zeros((image_array.shape[0], image_array.shape[1], 3), dtype=np.uint8)
                rgb_image[:, :, 0] = image_array.astype(np.uint8)  # 红色通道
                rgb_image[:, :, 1] = image_array.astype(np.uint8)  # 绿色通道
                rgb_image[:, :, 2] = image_array.astype(np.uint8)  # 蓝色通道

                image = Image.fromarray(rgb_image)

                # 保存图像到文件（假设文件名以数字命名）
                file_name = f"image_03_{i}.png"
                image.save(rf"{upload_path_03}\{file_name}")
                file_paths_03.append(rf"{upload_path_03}\{file_name}")

        return {
                'code': 200,
                'messsge': "文件上传成功",
                'file_paths_01':file_paths_01,
                'file_paths_02':file_paths_02,
                'file_paths_03':file_paths_03,
                'data': json_data,
                'transparency': 0
        }
@app.route('/call_Model',methods=['GET'])
def call_Model():
        basePath = os.path.dirname(__file__)  # 当前文件所在路径print(basePath)
        upload_path_01 = os.path.join(basePath, 'output_result', 'output_result_01')
        upload_path_01 = os.path.abspath(upload_path_01)  # 将路径转换为绝对路径print("绝对路径：",upload_path)
        upload_path_02 = os.path.join(basePath, 'output_result', 'output_result_02')
        upload_path_02 = os.path.abspath(upload_path_02)  # 将路径转换为绝对路径print("绝对路径：",upload_path)
        upload_path_03 = os.path.join(basePath, 'output_result', 'output_result_03')
        upload_path_03 = os.path.abspath(upload_path_03)  # 将路径转换为绝对路径print("绝对路径：",upload_path)

        # data = request.json  # 使用 request.json 获取 JSON 格式的数据

        folder_path = "input_files"
        folder_path_01 = "infer_result"
        path = os.listdir(folder_path)
        path = os.path.join(basePath, folder_path, path[len(path) - 1])
        path = os.path.abspath(path)
        # print(path)

        command = rf"python infer_seg.py --sw_batch_size 2 --overlap 0.5 --num_workers 2 --nifti_path {path} --output {basePath}\infer_result --checkpoint {basePath}\model_best.pt"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        # 打印输出结果
        print("Output:", output.decode())
        print("Error:", error.decode())
        files = os.listdir(folder_path)
        files_01 = os.listdir(folder_path_01)

        resultPath_01 = os.path.join(basePath, 'infer_result', files_01[len(files_01) - 1])
        nii_01 = nib.load(resultPath_01)

        resultPath = os.path.join(basePath, 'input_files', files[len(files) - 1])
        nii = nib.load(resultPath)

        data = nii.get_fdata()
        min_val = np.min(data)
        max_val = np.max(data)
        normalized_data = (data - min_val) / (max_val - min_val)

        data_01 = nii_01.get_fdata()
        min_val_01 = np.min(data_01)
        max_val_01 = np.max(data_01)
        normalized_data1 = (data_01 - min_val_01) / (max_val_01 - min_val_01)

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

                cv2.addWeighted(rgb_image_1, 0.2, rgb_image, 0.8, 0, rgb_image)

                # 将 ndarray 转换为 PIL Image 对象
                image = Image.fromarray(rgb_image)

                # 保存图像到文件（假设文件名以数字命名）
                file_name = f"image_01_{i }.png"
                image.save(rf"{upload_path_01}\{file_name}")

        for i in range(normalized_data.shape[1]):
                # 获取第 i 张图片的数据
                image_array = normalized_data[:, i, :] * 255
                image_array_1 = normalized_data1[:, i, :] * 255

                # 将灰度图image_array转换为RGB图像数组
                rgb_image = np.zeros((image_array.shape[0], image_array.shape[1], 3), dtype=np.uint8)
                rgb_image[:, :, 0] = image_array.astype(np.uint8)  # 红色通道
                rgb_image[:, :, 1] = image_array.astype(np.uint8)  # 绿色通道
                rgb_image[:, :, 2] = image_array.astype(np.uint8)  # 蓝色通道

                # 将黑绿图image_array_1转换为RGB图像数组
                rgb_image_1 = np.zeros((image_array_1.shape[0], image_array_1.shape[1], 3), dtype=np.uint8)
                rgb_image_1[:, :, 1] = image_array_1.astype(np.uint8)  # 绿色通道

                cv2.addWeighted(rgb_image_1, 0.2, rgb_image, 0.8, 0, rgb_image)

                # 将 ndarray 转换为 PIL Image 对象
                image = Image.fromarray(rgb_image)

                # 保存图像到文件（假设文件名以数字命名）
                file_name = f"image_02_{i}.png"
                image.save(rf"{upload_path_02}\{file_name}")

        for i in range(normalized_data.shape[2]):
                # 获取第 i 张图片的数据
                image_array = normalized_data[:, :, i] * 255
                image_array_1 = normalized_data1[:, :, i] * 255

                # 将灰度图image_array转换为RGB图像数组
                rgb_image = np.zeros((image_array.shape[0], image_array.shape[1], 3), dtype=np.uint8)
                rgb_image[:, :, 0] = image_array.astype(np.uint8)  # 红色通道
                rgb_image[:, :, 1] = image_array.astype(np.uint8)  # 绿色通道
                rgb_image[:, :, 2] = image_array.astype(np.uint8)  # 蓝色通道

                # 将黑绿图image_array_1转换为RGB图像数组
                rgb_image_1 = np.zeros((image_array_1.shape[0], image_array_1.shape[1], 3), dtype=np.uint8)
                rgb_image_1[:, :, 1] = image_array_1.astype(np.uint8)  # 绿色通道

                cv2.addWeighted(rgb_image_1, 0.15, rgb_image, 0.85, 0, rgb_image)

                # 将 ndarray 转换为 PIL Image 对象
                image = Image.fromarray(rgb_image)

                # 保存图像到文件（假设文件名以数字命名）
                file_name = f"image_03_{i}.png"
                image.save(rf"{upload_path_03}\{file_name}")

        return {
                'code': 200,
                'messsge': "模型调用成功"
        }
@app.route('/post', methods=['POST'])
def post_example():
        basePath = os.path.dirname(__file__)  # 当前文件所在路径print(basePath)
        upload_path_01 = os.path.join(basePath, 'output_result', 'output_result_01')
        upload_path_01 = os.path.abspath(upload_path_01)  # 将路径转换为绝对路径print("绝对路径：",upload_path)
        upload_path_02 = os.path.join(basePath, 'output_result', 'output_result_02')
        upload_path_02 = os.path.abspath(upload_path_02)  # 将路径转换为绝对路径print("绝对路径：",upload_path)
        upload_path_03 = os.path.join(basePath, 'output_result', 'output_result_03')
        upload_path_03 = os.path.abspath(upload_path_03)  # 将路径转换为绝对路径print("绝对路径：",upload_path)
        upload_path_04 = os.path.join(basePath, 'infer_result')
        upload_path_04 = os.path.abspath(upload_path_04)  # 将路径转换为绝对路径print("绝对路径：",upload_path)
        upload_path_05 = os.path.join(basePath, 'input_files')
        upload_path_05 = os.path.abspath(upload_path_05)  # 将路径转换为绝对路径print("绝对路径：",upload_path)

        # 获取上传文件数据
        file = request.files.get('file')
        if file is None:
                # 表示没有发送文件
                return {
                        'message': "文件上传失败"
                }
        file_name = file.filename  # print(file.filename)
        # 获取前缀（文件名称）print(os.path.splitext(file_name)[0])
        # 获取后缀（文件类型）print(os.path.splitext(file_name)[-1])
        suffix = os.path.splitext(file_name)[-1]  # 获取文件后缀（扩展名）
        nowTime = calendar.timegm(time.gmtime())  # 获取当前时间戳改文件名print(nowTime)
        upload_path = os.path.join(basePath, 'input_files',
                                   str(nowTime))
        upload_path = os.path.abspath(upload_path)  # 将路径转换为绝对路径print("绝对路径：",upload_path)
        file.save(upload_path + file_name)  # 保存文件
        path = upload_path + file_name

        command = rf"python infer_seg.py --sw_batch_size 2 --overlap 0.5 --num_workers 2 --nifti_path {path} --output {basePath}\infer_result --checkpoint {basePath}\model_best.pt"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        # 打印输出结果
        print("Output:", output.decode())
        print("Error:", error.decode())

        nii = nib.load(path)
        # 获取分辨率
        header_dict = dict(nii.header)
        pixdim = header_dict["pixdim"][1:4]
        pixdim_list = pixdim.tolist()  # 将 ndarray 转换为 Python 列表
        json_data = json.dumps({'data': pixdim_list})  # 将数据序列化为 JSON 格式
        # 将data归一化
        folder_path = "input_files"
        folder_path_01 = "infer_result"
        files = os.listdir(folder_path)
        files_01 = os.listdir(folder_path_01)

        resultPath_01 = os.path.join(basePath, 'infer_result', files_01[len(files_01) - 1])
        nii_01 = nib.load(resultPath_01)

        resultPath = os.path.join(basePath, 'input_files', files[len(files) - 1])
        nii = nib.load(resultPath)

        data = nii.get_fdata()
        min_val = np.min(data)
        max_val = np.max(data)
        normalized_data = (data - min_val) / (max_val - min_val)

        data_01 = nii_01.get_fdata()
        min_val_01 = np.min(data_01)
        max_val_01 = np.max(data_01)
        normalized_data1 = (data_01 - min_val_01) / (max_val_01 - min_val_01)

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

                cv2.addWeighted(rgb_image_1, 0.2, rgb_image, 0.8, 0, rgb_image)

                # 将 ndarray 转换为 PIL Image 对象
                image = Image.fromarray(rgb_image)

                # 保存图像到文件（假设文件名以数字命名）
                file_name = f"image_01_{i}.png"
                image.save(rf"{upload_path_01}\{file_name}")

        for i in range(normalized_data.shape[1]):
                # 获取第 i 张图片的数据
                image_array = normalized_data[:, i, :] * 255
                image_array_1 = normalized_data1[:, i, :] * 255

                # 将灰度图image_array转换为RGB图像数组
                rgb_image = np.zeros((image_array.shape[0], image_array.shape[1], 3), dtype=np.uint8)
                rgb_image[:, :, 0] = image_array.astype(np.uint8)  # 红色通道
                rgb_image[:, :, 1] = image_array.astype(np.uint8)  # 绿色通道
                rgb_image[:, :, 2] = image_array.astype(np.uint8)  # 蓝色通道

                # 将黑绿图image_array_1转换为RGB图像数组
                rgb_image_1 = np.zeros((image_array_1.shape[0], image_array_1.shape[1], 3), dtype=np.uint8)
                rgb_image_1[:, :, 1] = image_array_1.astype(np.uint8)  # 绿色通道

                cv2.addWeighted(rgb_image_1, 0.2, rgb_image, 0.8, 0, rgb_image)

                # 将 ndarray 转换为 PIL Image 对象
                image = Image.fromarray(rgb_image)

                # 保存图像到文件（假设文件名以数字命名）
                file_name = f"image_02_{i}.png"
                image.save(rf"{upload_path_02}\{file_name}")

        for i in range(normalized_data.shape[2]):
                # 获取第 i 张图片的数据
                image_array = normalized_data[:, :, i] * 255
                image_array_1 = normalized_data1[:, :, i] * 255

                # 将灰度图image_array转换为RGB图像数组
                rgb_image = np.zeros((image_array.shape[0], image_array.shape[1], 3), dtype=np.uint8)
                rgb_image[:, :, 0] = image_array.astype(np.uint8)  # 红色通道
                rgb_image[:, :, 1] = image_array.astype(np.uint8)  # 绿色通道
                rgb_image[:, :, 2] = image_array.astype(np.uint8)  # 蓝色通道

                # 将黑绿图image_array_1转换为RGB图像数组
                rgb_image_1 = np.zeros((image_array_1.shape[0], image_array_1.shape[1], 3), dtype=np.uint8)
                rgb_image_1[:, :, 1] = image_array_1.astype(np.uint8)  # 绿色通道

                cv2.addWeighted(rgb_image_1, 0.15, rgb_image, 0.85, 0, rgb_image)

                # 将 ndarray 转换为 PIL Image 对象
                image = Image.fromarray(rgb_image)

                # 保存图像到文件（假设文件名以数字命名）
                file_name = f"image_03_{i}.png"
                image.save(rf"{upload_path_03}\{file_name}")

        return {
                'code': 200,
                'messsge': "文件上传成功",
        }
@app.route('/change_Transparency', methods=['POST'])
def change_Transparency():
        data = request.json  # 使用 request.json 获取 JSON 格式的数据
        print(data)

app.run(host='0.0.0.0', port=5000)
