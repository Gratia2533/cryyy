import os
import random


pts_num = int(input('number?\n')) #隨機抽取的初始數量

# 定義路徑
source_dir = '/home/m112040034/workspace/simulation/box/train'
target_dir = '/home/m112040034/workspace/simulation/partial_box/used_pool/initial'
unused_dir = '/home/m112040034/workspace/simulation/partial_box/unused_pool/initial'

# 確保目標目錄存在
os.makedirs(target_dir, exist_ok=True)
os.makedirs(unused_dir, exist_ok=True)

# 獲取所有 .box 檔案名
box_files = [f for f in os.listdir(source_dir) if f.endswith('.box')]

# 所有檔案的資料行
all_lines = []

# 讀取所有檔案的資料行
for file_name in box_files:
    file_path = os.path.join(source_dir, file_name)
    with open(file_path, 'r') as file:
        lines = file.readlines()
    all_lines.extend([(file_name, line) for line in lines])

# 隨機抽取X行資料行
sampled_lines = random.sample(all_lines, min(pts_num, len(all_lines)))

# 根據檔名分類抽取的資料行
file_lines = {file_name: [] for file_name in box_files}
for file_name, line in sampled_lines:
    file_lines[file_name].append(line)

# 計算未被抽取到的資料行
all_lines_dict = {file_name: [] for file_name in box_files}
for file_name, line in all_lines:
    all_lines_dict[file_name].append(line)

# 將資料行寫入對應的檔案
for file_name, lines in file_lines.items():
    target_file_path = os.path.join(target_dir, file_name)
    if lines:
        with open(target_file_path, 'w') as file:
            file.writelines(lines)
    else:
        # 創建空檔案
        open(target_file_path, 'w').close()

# 將未被抽取到的資料行寫入對應的檔案
for file_name, lines in all_lines_dict.items():
    unused_lines = [line for line in lines if (file_name, line) not in sampled_lines]
    unused_file_path = os.path.join(unused_dir, file_name)
    if unused_lines:
        with open(unused_file_path, 'w') as file:
            file.writelines(unused_lines)
    else:
        # 創建空檔案
        open(unused_file_path, 'w').close()
