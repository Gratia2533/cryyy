#將所有預測的box檔案，通過groundtruth進行校正

import os

iter = input("iter?\n")
# 路徑
dir_A = "/home/m112040034/workspace/simulation/box/train"  # Groundtruth 路徑
dir_B = "/home/m112040034/workspace/simulation/output/" + iter + "/process/box"
output_dir = "/home/m112040034/workspace/simulation/output/" + iter + "/process/adjust"  # 新的輸出路徑

# 確保路徑存在
if not os.path.exists(dir_A):
    raise ValueError(f"Directory A '{dir_A}' does not exist.")
if not os.path.exists(dir_B):
    raise ValueError(f"Directory B '{dir_B}' does not exist.")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)  # 如果輸出目錄不存在，則創建它

def process_files_in_directories(dir_A, dir_B, output_dir):
    files_A = os.listdir(dir_A)
    files_B = os.listdir(dir_B)
    
    # 確保兩個目錄下的檔案數量和檔案名稱都一致
    if len(files_A) != len(files_B) or sorted(files_A) != sorted(files_B):
        raise ValueError("Directories A and B do not have the same number of files or identical filenames.")
    
    for filename in files_A:
        file_path_A = os.path.join(dir_A, filename)
        file_path_B = os.path.join(dir_B, filename)
        output_file_path = os.path.join(output_dir, filename)
        
        # 讀取目錄 A 和 B 中的檔案行
        lines_A = read_box_file(file_path_A)
        lines_B = read_box_file(file_path_B)
        
        # 比對並替換符合條件的行
        updated_lines_B = []
        changes = []
        for line_b in lines_B:
            found_match = False
            line_b_elements = line_b.split()
            for line_a in lines_A:
                if is_match(line_a, line_b):
                    line_a_elements = line_a.split()
                    updated_line = f"{line_a_elements[0]} {line_a_elements[1]} {line_a_elements[2]} {line_a_elements[3]} {line_b_elements[4]}\n"
                    updated_lines_B.append(updated_line)
                    changes.append(f"{filename} adjust {line_b.strip()} → {updated_line.strip()}")
                    found_match = True
                    break
            if not found_match:
                # 沒有找到匹配的行，則直接刪除這一行
                changes.append(f"{filename} delete {line_b.strip()}")
                continue
        
        # 將更新後的結果寫入新的檔案中
        write_box_file(output_file_path, updated_lines_B)
        
        # 印出 B 目錄的變動報告
        print(f"Changes in {filename}:")
        for change in changes:
            print(change)
        print()

def read_box_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def write_box_file(file_path, lines):
    with open(file_path, 'w') as file:
        file.writelines(lines)

def is_match(line_a, line_b):
    a_values = line_a.split()
    b_values = line_b.split()
    
    # 檢查第一個和第二個值的差距
    diff_x = abs(float(a_values[0]) - float(b_values[0]))
    diff_y = abs(float(a_values[1]) - float(b_values[1]))
    
    return diff_x < 150 and diff_y < 150

# 執行處理
process_files_in_directories(dir_A, dir_B, output_dir)
