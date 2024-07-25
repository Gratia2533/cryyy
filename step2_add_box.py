#從預測出的標註檔案中，尋找前幾個最大不確定性的粒子
import os

iter="10"
input_dir = "/home/m112040034/workspace/simulation/output/loop"+iter+"/process/score"
output_dir = "/home/m112040034/workspace/simulation/output/loop"+iter+"/process/add"

# 確保輸出目錄存在
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

#定義根據不確定性尋找的方法
def process_box_file(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    # 解析每一行，並根據第4個值進行排序(索引4為entropy score)
    parsed_lines = [line.split() for line in lines]
    sorted_lines = sorted(parsed_lines, key=lambda x: float(x[4]), reverse=True)
    
    # 保留前 X 大的行
    top_lines = sorted_lines[:16]
    
    # 將結果寫入新的檔案
    with open(output_file, 'w') as file:
        for line in top_lines:
            file.write(' '.join(line) + '\n')

# 對目錄中所有 .box 進行尋找
for filename in os.listdir(input_dir):
    if filename.endswith(".box"):
        input_file_path = os.path.join(input_dir, filename)
        output_file_path = os.path.join(output_dir, filename)
        process_box_file(input_file_path, output_file_path)
