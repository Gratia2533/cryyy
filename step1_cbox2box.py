#把Cryolo prediction output的CBOX轉回有包含confidence的box檔案，然後進行entropy_score計算存回
import os
import numpy as np

#計算logit
def logit(p):
    if np.any((p <= 0) | (p >= 1)):
        raise ValueError("The probability value should be in the range 0 < p < 1")
    return np.log(p / (1 - p))
#定義sigmoid函數
def sigmoid(x):
    return 1 / (1 + np.exp(-x))
#定義entropy score計算
def entropy_score(x):
    logits = logit(x)
    H = -sigmoid(logits) * np.log(sigmoid(logits)) - sigmoid(-logits) * np.log(sigmoid(-logits))
    return H

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
                # 計算 entropy_score
                confidence = float(values[8])
                #對cryolo輸出的confidence計算entropy score
                entropy = entropy_score(confidence)
                #(X,Y),boxsize,boxsize,entropy score
                modified_line = f"{values[0]} {values[1]} {values[3]} {values[4]} {entropy}\n"
                modified_lines.append(modified_line)
            except ValueError:
                continue

    # 寫入新的檔案
    with open(output_file, 'w') as file:
        file.writelines(modified_lines)

iter = '10'
input_dir = "/home/m112040034/workspace/simulation/output/loop"+iter+"/CBOX"
output_dir = "/home/m112040034/workspace/simulation/output/loop"+iter+"/process/score"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for filename in os.listdir(input_dir):
    if filename.endswith(".cbox"):
        input_file_path = os.path.join(input_dir, filename)
        output_file_path = os.path.join(output_dir, filename.replace(".cbox", ".box"))
        process_cbox_file(input_file_path, output_file_path)
