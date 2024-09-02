#step2校正後，可能會有同個座標點多次重複的情況
#刪除本身重複的座標點，接著再刪除已學習過的座標點(存在於used_pool)

#此step3變體用於將標註分為used/unused pool，當迭代使用pretrained weight時，不重複使用已學習過標註
import os

iter = input("iter?\n")
input_dir = "/home/m112040034/workspace/simulation/output/" + iter + "/process/adjust"  # 原始檔案路徑
output_dir = "/home/m112040034/workspace/simulation/output/" + iter + "/process/unique"  # 新的輸出路徑
partial_dir = "/home/m112040034/workspace/simulation/partial_box/used_pool"  # 參考檔案路徑

# 確保輸出目錄存在
if not os.path.exists(output_dir):
    os.makedirs(output_dir)  # 如果輸出目錄不存在，則創建它

def process_files(input_dir, output_dir, partial_dir):
    # 讀取參考檔案中的所有行
    partial_lines = read_all_lines_from_directory(partial_dir)
    partial_keys = set((line.split()[0], line.split()[1]) for line in partial_lines)
    
    files = os.listdir(input_dir)
    
    for filename in files:
        file_path = os.path.join(input_dir, filename)
        output_file_path = os.path.join(output_dir, filename)
        
        # 讀取檔案內容
        lines = read_box_file(file_path)
        
        # 將行根據 index=0 和 index=1 的值進行分組，並保留 index=4 最大的行
        grouped_lines = group_lines_by_indices(lines)
        
        # 過濾掉在 partial_dir 中已存在的行
        filtered_lines = filter_lines(grouped_lines, partial_keys)
        
        # 將處理後的結果寫入新的檔案中
        write_box_file(output_file_path, filtered_lines)
    
    print("Processing complete. Files have been saved to:", output_dir)

def read_box_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def write_box_file(file_path, lines):
    with open(file_path, 'w') as file:
        file.writelines(lines)

def read_all_lines_from_directory(directory):
    all_lines = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        lines = read_box_file(file_path)
        all_lines.extend(lines)
    return all_lines

def group_lines_by_indices(lines):
    line_dict = {}
    
    for line in lines:
        elements = line.split()
        key = (elements[0], elements[1])
        if key in line_dict:
            # 比較 index=4 的值，保留最大的那個行
            existing_line = line_dict[key]
            if float(elements[4]) > float(existing_line.split()[4]):
                line_dict[key] = line
        else:
            line_dict[key] = line
    
    return list(line_dict.values())

def filter_lines(lines, partial_keys):
    filtered_lines = []
    for line in lines:
        elements = line.split()
        key = (elements[0], elements[1])
        if key not in partial_keys:
            filtered_lines.append(line)
    return filtered_lines

# 執行處理
process_files(input_dir, output_dir, partial_dir)
