import os
import numpy as np
import re

#========process indicator method========#
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
    """
    計算entropy分數
    :param x: 機率值或包含機率值的numpy數組，範圍應該是0到1之間
    :return: entropy score
    """
    logits = logit(x)
    H = -sigmoid(logits) * np.log(sigmoid(logits)) - sigmoid(-logits) * np.log(sigmoid(-logits))
    return H

def normalize_confidence(confidence, min_confidence, max_confidence):
    """
    將 confidence 值正規化到 [0.01, 0.99] 的範圍內
    """
    return 0.01 + (confidence - min_confidence) * (0.99 - 0.01) / (max_confidence - min_confidence)

# 找出所有檔案中 confidence 的最大值和最小值，決定正規化的範圍
def find_confidence_range(CBOX_dir):
    min_confidence = float('inf')
    max_confidence = float('-inf')

    for filename in os.listdir(CBOX_dir):
        if filename.endswith(".cbox"):
            input_file_path = os.path.join(CBOX_dir, filename)
            with open(input_file_path, 'r') as file:
                lines = file.readlines()[19:]  # 刪除前19行
                
                for line in lines:
                    values = line.split()
                    if len(values) >= 9:  # 確保有足夠的值
                        confidence = float(values[8])
                        min_confidence = min(min_confidence, confidence)
                        max_confidence = max(max_confidence, confidence)

    return min_confidence, max_confidence

def find_topt(html_file_path, topt_log):
    """
    :param html_file_path: CrYOLO進行evaluation後輸出的HTML文件路徑
    :param topt_log: 紀錄topt的log文件路徑，以便後續可能需要檢查
    :return: 返回 topt 值，供計算boundary_distance使用
    """
    # 確保 html_file_path 是一個文件路徑
    if not os.path.isfile(html_file_path):
        raise FileNotFoundError(f"HTML file not found: {html_file_path}")
    
    # 讀取 evaluation HTML 文件內容
    with open(html_file_path, 'r') as file:
        content = file.read()

    # 使用正則表達式搜尋 topt 
    match = re.search(r"Best confidence threshold \( -t \) according F1 statistic:\s*(0\.\d+)", content)
    
    if match:
        topt = float(match.group(1))  # group(1) 提取的是 topt 值
        
        # 檢查 topt_log 是否存在，不存在則新增
        if not os.path.exists(topt_log):
            with open(topt_log, 'w') as f:
                pass  # 檔案不存在時新增空文件

        # 將找到的 topt 值記錄下來
        with open(topt_log, 'a') as f:  # 用追加寫入，紀錄每次迭代的 topt
            f.write(f"{topt}\n")
        print(f"topt: {topt} saved to {topt_log}")
        
        return topt  # 返回 topt 值
    else:
        raise ValueError("Cannot find the 'Best confidence threshold according F1 statistic' in the file.")

'''
def boundary_dist(topt):
    """
    Returns a function that calculates the absolute distance between confidence and topt.
    :param topt: The topt value calculated from find_topt
    :return: A function that takes confidence and calculates abs(confidence - topt)
    """
    def calculate_distance(confidence):
        return abs(confidence - topt)
    
    return calculate_distance
'''   





