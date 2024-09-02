#查看當前資料夾的標註粒子數量
import os
import numpy as np
from collections import defaultdict

# 設定路徑
folder = input("folder?\n")
input_dir = "/home/m112040034/workspace/simulation/partial_box/"+folder

# 初始化變數
total_lines = 0
values = []

# 遍歷路徑中的所有 .box 文件
for filename in os.listdir(input_dir):
    if filename.endswith(".box"):
        file_path = os.path.join(input_dir, filename)
        with open(file_path, 'r') as file:
            lines = file.readlines()
            total_lines += len(lines)
            '''
            for line in lines:
                value = float(line.split()[4])
                values.append(value)'''
'''
# 找出最小值和最大值
min_value = min(values)
max_value = max(values)

# 初始化計數字典
value_ranges = defaultdict(int)

# 計算每個範圍內的行數
step = 0.01
current_value = min_value
while current_value < max_value:
    upper_bound = current_value + step
    count = sum(1 for value in values if current_value < value <= upper_bound)
    value_ranges[(current_value, upper_bound)] = count
    current_value = upper_bound
'''
# 輸出結果
print(f"Total particles: {total_lines}")
'''
print(f"Minimum value: {min_value}")
print(f"Maximum value: {max_value}")
print("Value ranges and their counts:")
for value_range, count in value_ranges.items():
    print(f"{value_range}: {count}")
'''