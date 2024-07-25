#對比Groundtruth來校正add裡產出的box
import os

iter = "10"
# 路徑
dir_A = "/home/m112040034/workspace/simulation/box/train" #Groundtruth路徑
dir_B = "/home/m112040034/workspace/simulation/output/loop"+iter+"/process/add"

# check path exists
if not os.path.exists(dir_A):
    raise ValueError(f"Directory A '{dir_A}' does not exist.")
if not os.path.exists(dir_B):
    raise ValueError(f"Directory B '{dir_B}' does not exist.")

def process_files_in_directories(dir_A, dir_B):
    files_A = os.listdir(dir_A)
    files_B = os.listdir(dir_B)
    
    # 確保兩個路徑下的檔案數量和檔案名稱都一致
    if len(files_A) != len(files_B) or sorted(files_A) != sorted(files_B):
        raise ValueError("Directories A and B do not have the same number of files or identical filenames.")
    
    for filename in files_A:
        file_path_A = os.path.join(dir_A, filename)
        file_path_B = os.path.join(dir_B, filename)
        
        # 讀取目錄 A 和 B 中的資料行
        lines_A = read_box_file(file_path_A)
        lines_B = read_box_file(file_path_B)
        
        # 比對並替換符合條件的行
        updated_lines_B = []
        changes = []
        for line_b in lines_B:
            found_match = False
            for line_a in lines_A:
                if is_match(line_a, line_b):
                    updated_lines_B.append(line_a)
                    changes.append(f"{filename} adjust {line_b.strip()} → {line_a.strip()}")
                    found_match = True
                    break
            if not found_match:
                changes.append(f"{filename} delete {line_b.strip()}")
        
        # 將更新後的結果寫入 B 路徑的檔案中
        write_box_file(file_path_B, updated_lines_B)
        
        # 輸出 B 路徑內檔案的變動情形
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
    
    return diff_x < 100 and diff_y < 100

# 執行處理
process_files_in_directories(dir_A, dir_B)
