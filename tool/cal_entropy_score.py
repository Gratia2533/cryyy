# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 19:43:24 2024
#將Cryolo的預測輸出，依照topaz active learning framework的方法計算entropy score
@author: User
"""
import numpy as np
import pandas as pd

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
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # 找到"data_cryolo_include"的位置，確保尾部信息也被保留
    cryolo_include_idx = lines.index('data_cryolo_include\n')
    header = lines[:19]  # 前19行是頭部信息
    data = lines[19:cryolo_include_idx]  # 中間的數據部分
    footer = lines[cryolo_include_idx:]  # 尾部信息

    processed_data = []
    for line in data:
        if line.strip() == '':  # 遇到空行停止處理
            break
        values = line.split()
        try:
            # 取第9列的值並計算entropy_score
            conf_value = float(values[8])
            new_conf_value = entropy_score(conf_value)
            values[8] = str(new_conf_value)
            processed_data.append(" ".join(values))
        except ValueError:
            # 若無法轉換為float，跳過這行
            continue

    # 合併頭部信息、中間處理過的數據和尾部信息
    processed_lines = header + processed_data + footer

    # 將結果寫入新的文件
    with open(output_file, 'w') as f:
        for line in processed_lines:
            f.write(line + '\n')

input_file = '/home/m112040034/workspace/simulation/output/initial/CBOX/micrograph_0.cbox'
output_file = '/home/m112040034/workspace/simulation/output/initial/process/micrograph_0.cbox'

process_cbox_file(input_file, output_file)