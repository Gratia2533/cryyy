# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 23:15:24 2024
#目的：使用ASPIRE生成mrc與star檔案後，將star檔案轉換為cryolo接受的box格式
@author: Gratia
"""
import os

# in/out put folder path
input_folder = r"/home/m112040034/workspace/simulation/star"
output_folder = r"/home/m112040034/workspace/simulation/box/train"

# check folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 處理每一個star檔案
for i in range(300):
    input_file_path = os.path.join(input_folder, f"micrograph_{i}.star")
    output_file_path = os.path.join(output_folder, f"micrograph_{i}.box")
    
    # 讀取
    with open(input_file_path, 'r') as file:
        lines = file.readlines()
    
    # 處理每一行數據
    processed_lines = []
    for line in lines:
        split_line = line.split()
        if len(split_line) > 3:  # 確保行內有足夠的元素
            x = float(split_line[2])  # 原始star檔案第3個值
            y = float(split_line[3])  # 原始star檔案第4個值
            boxsize = 250  # 指定boxsize
            
            # 計算star to box時的位移
            eman_x = x - boxsize / 2
            eman_y = y - boxsize / 2
            
            # 產出新的行
            new_line = f"{eman_x} {eman_y} 250 250"
            processed_lines.append(new_line + "\n")
    
    # 將結果寫入新檔案
    with open(output_file_path, 'w') as file:
        file.writelines(processed_lines)
    
    print(f"star2box successfully {output_file_path}")

print("All star file convert to box format completely")

