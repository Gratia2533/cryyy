import os
import math
from . import tool
#========Step2:adjust========#
def correction_by_iou(gt_dir, box_dir, adjust_dir, iou_th):
    '''
    包含第四元素值的Predict label與Groundtruth做比對，第四元素值有不同的方法計算
    符合條件的Predict label校正以Groundtruth的座標寫入新的.box file
    :param gt_dir:the folder path for Groundtruth
    :param box_dir:the folder path for preprocessing predict label
    :param adjust_dir:the new folder path for save result of comparison
    :iou_th: IOU value which the experiment accepted
    '''
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
        lines_gt = tool.read_box_file(file_path_gt)
        lines_box = tool.read_box_file(file_path_box)
        
        # 比對並替換符合條件的行
        updated_lines_box = []
        changes = []
        for line_box in lines_box:
            found_match = False
            line_box_elements = line_box.split()
            for line_gt in lines_gt:
                if is_match(line_gt, line_box, iou_th):
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
        tool.write_box_file(output_file_path, updated_lines_box)
        
        # 輸出更動結果
        print(f"Changes in {filename}:")
        for change in changes:
            print(change)
        print()


def is_match(line_gt, line_box, iou_th):

    '''
    比對準則:確認IoU
    :param line_gt: A row data of Groundtruth
    :line_box: A row data of preprocessing predict label
    :iou_th: IOU value which the experiment accepted
    :return: True or False
    '''
    # 取得groundtruth的方框左上角座標和寬高
    gt_values = list(map(float, line_gt.split()[:4]))  # [x, y, width, height]
    box_values = list(map(float, line_box.split()[:4]))  # [x, y, width, height]

    radius = gt_values[2]/2

    # Groundtruth圓心座標 = 左上角座標 + 寬高的一半
    center_gt_x = gt_values[0] + radius
    center_gt_y = gt_values[1] + radius
    
    # 預測框的圓心座標 = 左上角座標 + 寬高的一半
    center_box_x = box_values[0] + radius
    center_box_y = box_values[1] + radius
    

    # 計算圓形的IOU
    iou = calculate_circle_iou([center_gt_x, center_gt_y], 
                               [center_box_x, center_box_y],radius)
    
    # 檢查IOU是否超過指定的閾值
    return iou >= iou_th

def calculate_circle_iou(circle1, circle2, radius):
    '''
    計算IOU
    :param circle1: coordinate of the circle
    :param circle2: coordinate of another circle
    :param radius: the value of index=2 or 3  which in box file of groundtruth
    the shape of param circle like [x, y] 
    :return: IOU值
    '''
    x1, y1 = circle1
    x2, y2 = circle2

    r = radius
    
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
    diamond = 2 * 0.5 * distance * math.sqrt(abs(r**2 - (distance/2)**2)) #2個等腰三角形，distance是底，後面是在算高，r是斜邊
    
    inter_area = 2 * part - diamond #兩個扇形，減掉2個等邊三角形
    
    # 計算兩個圓的總面積（這裡兩個圓的面積相等）
    union_area = 2 * (math.pi * r**2) - inter_area
    
    # 計算IOU
    return inter_area / union_area

#========Step3:Unique========#

def unique_row_data(adjust_dir, unique_dir, current_dir):
    """
    避免輸出的資料行中有重複，或與當次迭代重複
    :param adjust_dir: 經過IOU threshold比對後，且替換成Groundtruth座標的predict label的資料夾路徑
    :unique_dir: 去除重複的row data後的新box file路徑
    :current_dir: 當次迭代使用的box file路徑
    """
    # 讀取參考檔案中的所有行
    partial_lines = read_all_lines(current_dir)
    partial_keys = set((line.split()[0], line.split()[1]) for line in partial_lines)
    
    files = os.listdir(adjust_dir)
    
    for filename in files:
        file_path = os.path.join(adjust_dir, filename)
        output_file_path = os.path.join(unique_dir, filename)
        
        # 讀取檔案內容
        lines = tool.read_box_file(file_path)
        
        # 將行根據 index=0 和 index=1 的值進行分組，並保留 index=4 最大的行
        grouped_lines = group_lines_by_indices(lines)
        
        # 過濾掉在 current_dir 中已存在的行
        filtered_lines = only_lines(grouped_lines, partial_keys)
        
        # 將處理後的結果寫入新的檔案中
        tool.write_box_file(output_file_path, filtered_lines)
    
    print("Processing complete. Files have been saved to:", unique_dir)

def read_all_lines(directory):
    """
    一次讀取路徑中所有的資料行(座標)
    :param directory:校正後的box file資料夾路徑
    """
    all_lines = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        lines = tool.read_box_file(file_path)
        all_lines.extend(lines)
    return all_lines

def group_lines_by_indices(lines):
    """
    當座標相同時，保留指標值最大的row data
    :param lines: a row data of the box file
    """
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

def only_lines(lines, partial_keys):
    """
    沒有重複的row，則直接加入作為下次迭代*可能*使用的particle
    """
    filtered_lines = []
    for line in lines:
        elements = line.split()
        key = (elements[0], elements[1])
        if key not in partial_keys:
            filtered_lines.append(line)
    return filtered_lines

#========Step5:Generate next iteration .box========#
def generate_next_iter_annot(current_dir, filter_dir, next_dir):
    """
    :param current_dir: 當前迭代的.box資料夾路徑
    :param filter_dir: 只保含準備要新加入的row data資料夾路徑
    :param next_dir: 下次迭代要使用的.box輸出路徑
    """
    files_A = os.listdir(current_dir)
    files_B = os.listdir(filter_dir)
    
    # 確保兩個路徑下的檔案數量和檔案名稱都一致
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