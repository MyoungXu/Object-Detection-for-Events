import sys
import shutil
import numpy as np
import os
from tqdm import tqdm
import argparse

def get_image_prefixes(folder_path):
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']  # 可以根据需要添加其他图片扩展名

    prefixes = []
    for filename in os.listdir(folder_path):
        if any(filename.lower().endswith(ext) for ext in image_extensions):
            prefix = os.path.splitext(filename)[0]
            prefixes.append(prefix)

    return prefixes
def save_prefixes_to_file(prefixes, output_file):
    with open(output_file, 'w') as f:
        for prefix in prefixes:
            f.write(prefix + '\n')
def find_line_number(timestamp_file, timestamp):
    with open(timestamp_file, 'r') as file:
        lines = file.readlines()
        for i, line in enumerate(lines, start=1):
            if int(line[:-1]) == timestamp:
                return i
    return -1


folder_path = r'dataset_to_be_detected/images/train'
name_list = r'dataset_to_be_detected/output.txt'
# 创建解析器
parser = argparse.ArgumentParser(description='Process npy and timestamp files.')
# 添加命令行参数
parser.add_argument('--nt', type=str, help='Path to the npy and timestamp folder')
parser.add_argument('--p', type=str, help='Path to the pictures')
# 解析命令行参数
args = parser.parse_args()
# 检查命令行参数并更新变量值
if args.nt:
    basepath = args.nt
    npy_file = basepath + '/tracks.npy'
    timestamp_file = basepath + '/timestamps.txt'
if args.p:
    pics_path = args.p
    shutil.rmtree(folder_path)
    shutil.copytree(pics_path, folder_path)

data = np.load(npy_file)

# 记录图像名称
prefixes = get_image_prefixes(folder_path)
save_prefixes_to_file(prefixes, name_list)

# 删除文件夹中的所有文件和子文件夹
label_path = r'dataset_to_be_detected/labels/train'
shutil.rmtree(label_path)
# 创建一个空的文件夹
os.mkdir(label_path)

# 删除所有cache文件
directory = r'dataset_to_be_detected/labels'  # 目录路径
for filename in os.listdir(directory):
    if filename.endswith("cache"):
        file_path = os.path.join(directory, filename)  # 文件完整路径
        os.remove(file_path)  # 删除文件
        print(f"The file '{filename}' has been deleted.")

pic_h = 480
pic_w = 640

# 获取第一行的第一个数
first_value = data[0][0]
# 获取最后一行的第一个数
last_value = data[-1][0]
print(first_value)
print(last_value)
# 提取npy的数据并存放在txt里面
for item in tqdm(data):
    # 官方数据给错了，w和h反了
    t = item[0]
    if t == first_value or t == last_value:
        continue
    # x = item[1]
    # y = item[2]
    # w = item[3]
    # h = item[4]
    x = max(item[1], 1)
    y = max(item[2], 1)
    w = min(item[3], pic_w - x)
    h = min(item[4], pic_h - y)
    class_id = item[5]
    line_number = find_line_number(timestamp_file, t) - 1
    # 重新分类给标签
    if class_id == 0:
        new_id = 0
    elif class_id == 1:
        new_id = 0
    elif class_id == 2:
        new_id = 2
    elif class_id == 3:
        new_id = 5
    elif class_id == 4:
        new_id = 7
    elif class_id == 5:
        new_id = 1
    elif class_id == 6:
        new_id = 3
    elif class_id == 7:
        new_id = 6
    else:
        print("label class error!")
        sys.exit()
    YOLO1 = str(new_id)
    YOLO2 = str((x + w / 2) / pic_w)
    YOLO3 = str((y + h / 2) / pic_h)
    YOLO4 = str(w / pic_w)
    YOLO5 = str(h / pic_h)

    # 将YOLO数据按空格拼接并添加到列表中
    yolo_line = ' '.join([YOLO1, YOLO2, YOLO3, YOLO4, YOLO5])
    with open(name_list, 'r') as file:
        lines = file.readlines()
        if line_number > 0 and line_number <= len(lines):
            line = lines[line_number - 1].strip()
        else:
            print("\nfail to find {}".format(t))
            print(line_number, len(lines))
            continue

    file_path = r'dataset_to_be_detected/labels/train/' + str(line) + '.txt'
    with open(file_path, 'a') as file:
        file.write(yolo_line + '\n')
