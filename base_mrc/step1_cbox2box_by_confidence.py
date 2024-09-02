#把Cryolo prediction output的CBOX轉回有包含confidence的box檔案
import os
import numpy as np


def process_cbox_file(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # 刪除前19行
    lines = lines[19:]

    # 處理剩下的每一行
    modified_lines = []
    for line in lines:
        values = line.split()
        if len(values) >= 9:  # 確保有足夠的值
            try:
                #x,y座標、boxsize長寬、confidence
                modified_line = f"{values[0]} {values[1]} {values[3]} {values[4]} {values[8]}\n"
                modified_lines.append(modified_line)
            except ValueError:
                continue
    # 寫入新的文件
    with open(output_file, 'w') as file:
        file.writelines(modified_lines)

iter = input("iter?\n")
input_dir = "/home/m112040034/workspace/simulation/output/" + iter + "/CBOX"
output_dir = "/home/m112040034/workspace/simulation/output/" + iter + "/box"


if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for filename in os.listdir(input_dir):
    if filename.endswith(".cbox"):
        input_file_path = os.path.join(input_dir, filename)
        output_file_path = os.path.join(output_dir, filename.replace(".cbox", ".box"))
        process_cbox_file(input_file_path, output_file_path)
