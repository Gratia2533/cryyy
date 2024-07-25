# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 23:50:40 2024
#目的：將處理過後符合cryolo接受的box format，減少至?%的標註量，用來作為active learning的初始粒子選取
@author: Gratia
"""

import os
import random

# in/out put folder path
input_folder = r"/home/m112040034/workspace/simulation/box/train"
output_folder = r"/home/m112040034/workspace/simulation/partial_box/initial"

# check folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 刪除?%的行數
delete_percentage = 0.875

# 處理每個.box檔案
for i in range(240):
    input_file_path = os.path.join(input_folder, f"micrograph_{i}.box")
    output_file_path = os.path.join(output_folder, f"micrograph_{i}.box")
    
    # 讀取
    with open(input_file_path, 'r') as file:
        lines = file.readlines()
    
    # 計算要刪除的行數
    num_lines_to_delete = int(delete_percentage * len(lines))
    
    # 隨機選擇要刪除的行索引
    lines_to_delete = random.sample(range(len(lines)), num_lines_to_delete)
    
    # 保留未被選中的行
    remaining_lines = [line for idx, line in enumerate(lines) if idx not in lines_to_delete]
    
    # 寫入處理後的檔案
    with open(output_file_path, 'w') as file:
        file.writelines(remaining_lines)
    
    print(f"Reduce 87.5% annot: {output_file_path}")

print("All annotation file are reduce")
