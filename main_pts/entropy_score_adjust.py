import os
import numpy as np
import pandas as pd
import argparse
import math

"""
使用entropy score較大者
"""
####參數設定####
#adjust_distance = 50 #校正時的誤差接受範圍

iou_threshold =0.7 #校正使用的iou閾值

filter_num = 70 #每次iteration要增加的粒子數

####路徑設定####
# 設定命令行參數解析
parser = argparse.ArgumentParser(description='Generate annotations based on the current iteration.')
parser.add_argument('iter', type=str, help='Current iteration (e.g., "initial" or "iter7")')
args = parser.parse_args()
iter = args.iter

if iter == 'initial':
    next = 'iter1'
else:
    part1 = ''.join([char for char in iter if not char.isdigit()])
    part2 = ''.join([char for char in iter if char.isdigit()])
    next = part1+str(int(part2)+1)

CBOX_dir = "/home/m112040034/workspace/simulation/output/" + iter + "/CBOX"
box_dir = "/home/m112040034/workspace/simulation/output/" + iter + "/process/box"
gt_dir = "/home/m112040034/workspace/simulation/box/train"  # Groundtruth 路徑
adjust_dir = "/home/m112040034/workspace/simulation/output/" + iter + "/process/adjust"
unique_dir = "/home/m112040034/workspace/simulation/output/" + iter + "/process/unique"
current_dir = "/home/m112040034/workspace/simulation/partial_box/"+iter
filter_dir = '/home/m112040034/workspace/simulation/output/'+iter+'/process/filter'

next_dir = '/home/m112040034/workspace/simulation/partial_box/'+next


#$====================================step1====================================$#


def logit(p):
    """
    計算logit函數
    :param p: 機率值或包含機率值的numpy數組，範圍應該是0到1之間
    :return: logit值
    """
    if np.any((p <= 0) | (p >= 1)):
        raise ValueError("The probability value should be in the range 0 < p < 1")
    
    logit_value = np.log(p / (1 - p))
    return logit_value

def sigmoid(x):
    """
    計算sigmoid函數
    :param x: 輸入值或包含輸入值的numpy數組
    :return: sigmoid值
    """
    sigimoid_value = 1 / (1 + np.exp(-x))
    return sigimoid_value

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
                entropyScore = entropy_score(confidence)
                modified_line = f"{values[0]} {values[1]} {values[3]} {values[4]} {entropyScore}\n"
                modified_lines.append(modified_line)
            except ValueError:
                continue

    # 寫入新的文件
    with open(output_file, 'w') as file:
        file.writelines(modified_lines)

if not os.path.exists(box_dir):
    os.makedirs(box_dir)

for filename in os.listdir(CBOX_dir):
    if filename.endswith(".cbox"):
        input_file_path = os.path.join(CBOX_dir, filename)
        output_file_path = os.path.join(box_dir, filename.replace(".cbox", ".box"))
        process_cbox_file(input_file_path, output_file_path)

#$====================================step2====================================$#

# 確保目錄存在
if not os.path.exists(gt_dir):
    raise ValueError(f"Directory A '{gt_dir}' does not exist.")
if not os.path.exists(box_dir):
    raise ValueError(f"Directory B '{box_dir}' does not exist.")
if not os.path.exists(adjust_dir):
    os.makedirs(adjust_dir)  # 如果輸出目錄不存在，則創建它

def process_files_in_directories(gt_dir, box_dir, adjust_dir):
    files_A = os.listdir(gt_dir)
    files_B = os.listdir(box_dir)
    
    # 確保兩個目錄下的檔案數量和檔案名稱都一致
    if len(files_A) != len(files_B) or sorted(files_A) != sorted(files_B):
        raise ValueError("Directories A and B do not have the same number of files or identical filenames.")
    
    for filename in files_A:
        file_path_gt = os.path.join(gt_dir, filename)
        file_path_box = os.path.join(box_dir, filename)
        output_file_path = os.path.join(adjust_dir, filename)
        
        # 讀取目錄 A 和 B 中的檔案行
        lines_gt = read_box_file(file_path_gt)
        lines_box = read_box_file(file_path_box)
        
        # 比對並替換符合條件的行
        updated_lines_box = []
        changes = []
        for line_box in lines_box:
            found_match = False
            line_box_elements = line_box.split()
            for line_gt in lines_gt:
                if is_match(line_gt, line_box):
                    line_gt_elements = line_gt.split()
                    updated_line = f"{line_gt_elements[0]} {line_gt_elements[1]} {line_gt_elements[2]} {line_gt_elements[3]} {line_box_elements[4]}\n"
                    updated_lines_box.append(updated_line)
                    changes.append(f"{filename} adjust {line_box.strip()} → {updated_line.strip()}")
                    found_match = True
                    break
            if found_match == False:
                # 沒有找到匹配的行，則直接刪除這一行
                changes.append(f"{filename} delete {line_box.strip()}")
                continue
        
        # 將更新後的結果寫入新的檔案中
        write_box_file(output_file_path, updated_lines_box)
        
        # 輸出更動結果
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

def is_match(line_gt, line_box):

    '''
    #絕對距離的校正方法
    gt_values = line_gt.split()
    box_values = line_box.split()
    
    # 檢查第一個和第二個值的差距
    diff_x = abs(float(gt_values[0]) - float(box_values[0]))
    diff_y = abs(float(gt_values[1]) - float(box_values[1]))
    
    return diff_x < adjust_distance and diff_y < adjust_distance
    '''
    # 取得groundtruth的方框左上角座標和寬高
    gt_values = list(map(float, line_gt.split()[:4]))  # [x, y, width, height]
    box_values = list(map(float, line_box.split()[:4]))  # [x, y, width, height]
    
    # Groundtruth圓心座標 = 左上角座標 + 寬高的一半
    center_gt_x = gt_values[0] + gt_values[2] / 2
    center_gt_y = gt_values[1] + gt_values[3] / 2
    radius = gt_values[2] / 2  #設Groundtruth與Predict label的半徑一樣
    
    # 預測框的圓心座標 = 左上角座標 + 寬高的一半
    center_box_x = box_values[0] + box_values[2] / 2
    center_box_y = box_values[1] + box_values[3] / 2
    
    # 計算圓形的IOU
    iou = calculate_circle_iou([center_gt_x, center_gt_y, radius], 
                               [center_box_x, center_box_y, radius])
    
    # 檢查IOU是否超過指定的閾值
    return iou >= iou_threshold

def calculate_circle_iou(circle1, circle2):
    # circle1 和 circle2 的格式應為 [x, y, radius]
    # 兩個圓的半徑相同，使用 r 表示
    x1, y1, r = circle1
    x2, y2, r = circle2
    
    # 計算兩個圓心之間的距離
    distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    
    # 如果兩個圓不相交，IOU為0
    if distance >= 2 * r:
        return 0
    
    # 如果一個圓完全包含另一個圓，IOU為1，因為面積相同
    if distance == 0:
        return 1
    
    # 計算兩個圓的重疊面積
    part = r**2 * math.acos((distance) / (2 * r))#半徑平方*(圓心距離/直徑的比例，透過反餘弦得到弧度)
    diamond = 0.5 * math.sqrt(distance**2 * (4 * r**2 - distance**2))
    
    inter_area = 2 * part - diamond#兩個扇形，減掉上半跟下半三角形
    
    # 計算兩個圓的總面積（這裡兩個圓的面積相等）
    union_area = 2 * (math.pi * r**2) - inter_area
    
    # 計算IOU
    return inter_area / union_area

# 執行處理
process_files_in_directories(gt_dir, box_dir, adjust_dir)

#$====================================step3====================================$#

# 確保輸出目錄存在
if not os.path.exists(unique_dir):
    os.makedirs(unique_dir)  # 如果輸出目錄不存在，則創建它

def process_files(adjust_dir, unique_dir, current_dir):
    # 讀取參考檔案中的所有行
    partial_lines = read_all_lines_from_directory(current_dir)
    partial_keys = set((line.split()[0], line.split()[1]) for line in partial_lines)
    
    files = os.listdir(adjust_dir)
    
    for filename in files:
        file_path = os.path.join(adjust_dir, filename)
        output_file_path = os.path.join(unique_dir, filename)
        
        # 讀取檔案內容
        lines = read_box_file(file_path)
        
        # 將行根據 index=0 和 index=1 的值進行分組，並保留 index=4 最大的行
        grouped_lines = group_lines_by_indices(lines)
        
        # 過濾掉在 current_dir 中已存在的行
        filtered_lines = filter_lines(grouped_lines, partial_keys)
        
        # 將處理後的結果寫入新的檔案中
        write_box_file(output_file_path, filtered_lines)
    
    print("Processing complete. Files have been saved to:", unique_dir)

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
process_files(adjust_dir, unique_dir, current_dir)

#$====================================step4====================================$#

# 確保輸出目錄存在
os.makedirs(filter_dir, exist_ok=True)

# 讀取所有 .box 文件
data_frames = []
for file_name in os.listdir(unique_dir):
    if file_name.endswith('.box'):
        file_path = os.path.join(unique_dir, file_name)
        # 檢查檔案是否為空
        if os.path.getsize(file_path) > 0:
            # 讀取文件，以空格為分隔符
            df = pd.read_csv(file_path, delimiter=' ', header=None)
            # 新增column為檔案名
            df['filename'] = file_name
            data_frames.append(df)
        else:
            print(f"Skipping empty file: {file_name}")

# 合併所有dataframe
if data_frames:  # 檢查是否有任何非空檔案
    combined_df = pd.concat(data_frames, ignore_index=True)
    # 按照每一行第4個元素由大到小排序
    combined_df_sorted = combined_df.sort_values(by=4, ascending=False)
    # 只保留前X行數據
    top_X_df = combined_df_sorted.head(filter_num).reset_index(drop=True)
    top_X_df = top_X_df.drop(columns=[4])

    # 按照 filename 分組並將資料寫入對應的檔案
    for filename, group in top_X_df.groupby('filename'):
        # 設定檔案路徑
        file_path = os.path.join(filter_dir, filename)
        # 將分組資料寫入對應的檔案
        group.drop('filename', axis=1).to_csv(file_path, sep=' ', header=False, index=False)

    print("The data has been successfully written to the corresponding .box file")
else:
    print("No non-empty .box files found to process.")

# 檢查並創建缺少的 .box 檔案
expected_files = [f"micrograph_{i}.box" for i in range(70)]
existing_files = os.listdir(filter_dir)

missing_files = set(expected_files) - set(existing_files)
for missing_file in missing_files:
    open(os.path.join(filter_dir, missing_file), 'w').close()

print(f"Missing files have been created: {', '.join(missing_files)}")


#$====================================step5====================================$#

# 確保輸出目錄存在
os.makedirs(next_dir, exist_ok=True)

def merge_files(current_dir, filter_dir, next_dir):
    files_A = os.listdir(current_dir)
    files_B = os.listdir(filter_dir)
    
    # 確保兩個目錄下的檔案數量和檔案名稱都一致
    if len(files_A) != len(files_B) or sorted(files_A) != sorted(files_B):
        raise ValueError("Directories A and B do not have the same number of files or identical filenames.")

    for filename in files_B:
        file_filter_dir = os.path.join(filter_dir, filename)
        output_file_path = os.path.join(next_dir, filename)

        # 檢查 B 中檔案是否為空
        if os.path.getsize(file_filter_dir) > 0:
            # 讀取 B 路徑中的檔案內容
            with open(file_filter_dir, 'r') as file_B:
                lines_B = file_B.readlines()

            # 讀取 A 路徑中的檔案內容
            file_current_dir = os.path.join(current_dir, filename)
            with open(file_current_dir, 'r') as file_A:
                lines_A = file_A.readlines()

            # 合併檔案內容
            lines_A.extend(lines_B)

            # 寫入合併後的內容到新的路徑
            with open(output_file_path, 'w') as file_out:
                file_out.writelines(lines_A)
        else:
            # 如果 B 中的檔案為空，直接將 A 的檔案複製到輸出目錄
            file_current_dir = os.path.join(current_dir, filename)
            with open(file_current_dir, 'r') as file_A:
                lines_A = file_A.readlines()

            with open(output_file_path, 'w') as file_out:
                file_out.writelines(lines_A)

    # 輸出所有檔案的總行數
    total_lines = 0
    for filename in os.listdir(next_dir):
        file_path = os.path.join(next_dir, filename)
        with open(file_path, 'r') as file:
            total_lines += len(file.readlines())

    print("Files have been merged successfully.")
    print(f"particles: {total_lines}")

# 執行合併
merge_files(current_dir, filter_dir, next_dir)