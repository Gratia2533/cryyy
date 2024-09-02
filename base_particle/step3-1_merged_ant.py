import os
import pandas as pd

new = input("new?\n")
add = input("add?\n")
# 設定檔案路徑
dir_newly = '/home/m112040034/workspace/simulation/partial_box/'+new
dir_merged = '/home/m112040034/workspace/simulation/partial_box/'+add
output_dir = '/home/m112040034/workspace/simulation/partial_box/used_pool'
os.makedirs(output_dir, exist_ok=True)

# 讀取和合併兩個目錄中的 .box 文件
def merge_files(dir_newly, dir_merged, output_dir):
    files_newly = os.listdir(dir_newly)
    files_merged = os.listdir(dir_merged)
    
    # 確保兩個目錄下的檔案數量和檔案名稱都一致
    if len(files_newly) != len(files_merged) or sorted(files_newly) != sorted(files_merged):
        raise ValueError("Directories 'newly' and 'merged' do not have the same number of files or identical filenames.")
    
    for filename in files_newly:
        file_path_newly = os.path.join(dir_newly, filename)
        file_path_merged = os.path.join(dir_merged, filename)
        output_file_path = os.path.join(output_dir, filename)
        
        # 讀取兩個目錄中的檔案行
        lines_newly = read_box_file(file_path_newly)
        lines_merged = read_box_file(file_path_merged)
        
        # 合併內容
        merged_lines = lines_newly + lines_merged
        
        # 將合併後的結果寫入新的檔案中
        write_box_file(output_file_path, merged_lines)
        
        print(f"Files {filename} merged successfully.")
        
def read_box_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def write_box_file(file_path, lines):
    with open(file_path, 'w') as file:
        file.writelines(lines)

# 執行合併
merge_files(dir_newly, dir_merged, output_dir)

print(f"All files have been merged and saved in '{output_dir}'")

# 計算 output_dir 中所有檔案的總行數
def count_total_rows(directory):
    total_rows = 0
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r') as file:
            total_rows += sum(1 for _ in file)
    return total_rows

total_rows = count_total_rows(output_dir)
print(f"Particles: {total_rows}")
