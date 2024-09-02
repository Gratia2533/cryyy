import os
import numpy as np
import shutil

iter = input("iter?\n")
# 路徑
folder_path = "/home/m112040034/workspace/simulation/output/"+iter+"/box"

# 初始化存結果的list
file_averages = []

# 讀取資料夾中的每個.box檔案
for file_name in os.listdir(folder_path):
    if file_name.endswith(".box"):
        file_path = os.path.join(folder_path, file_name)
        
        # 讀取檔案內容
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # 根據confidence排序
        values = [float(line.split()[4]) for line in lines]
        values.sort()
        
        # 計算前半部分最小值的平均(決定當前影像的不確定性)
        half_count = int(len(values) // 2)
        average_of_smallest_half = np.mean(values[:half_count])
        
        # 將結果儲存到list中
        file_averages.append((file_name, average_of_smallest_half))

# 找出前28個最小值的檔案名
file_averages.sort(key=lambda x: x[1])
top_28_files = [os.path.splitext(file[0])[0] for file in file_averages[:28]]



# 路徑
mrc_unlabeled_dir = '/home/m112040034/workspace/simulation/mrc/unlabeled_pool'
mrc_labeled_dir = '/home/m112040034/workspace/simulation/mrc/labeled_pool'
box_unlabeled_dir = '/home/m112040034/workspace/simulation/box/unlabeled_pool'
box_labeled_dir = '/home/m112040034/workspace/simulation/box/labeled_pool'

for filename in top_28_files:
    mrc_file = filename + '.mrc'
    box_file = filename + '.box'

    # 移動 .mrc 檔案
    mrc_src_path = os.path.join(mrc_unlabeled_dir, mrc_file)
    mrc_dst_path = os.path.join(mrc_labeled_dir, mrc_file)
    shutil.move(mrc_src_path, mrc_dst_path)
    print(f'{mrc_file} moved')

    # 移動 .box 檔案
    box_src_path = os.path.join(box_unlabeled_dir, box_file)
    box_dst_path = os.path.join(box_labeled_dir, box_file)
    shutil.move(box_src_path, box_dst_path)
    print(f'{box_file} moved')

print('move file completely',
      '\n mrc unlabeled:',len(os.listdir(mrc_unlabeled_dir)),
      '\n mrc labeled:',len(os.listdir(mrc_labeled_dir)),
      '\n box unlabeled:',len(os.listdir(box_unlabeled_dir)),
      '\n mrc labeled:',len(os.listdir(box_labeled_dir)))