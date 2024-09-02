import os
import random
import shutil

# 路徑
mrc_train_dir = '/home/m112040034/workspace/simulation/mrc/unlabeled_pool'
mrc_labeled_pool_dir = '/home/m112040034/workspace/simulation/mrc/labeled_pool'
box_train_dir = '/home/m112040034/workspace/simulation/box/unlabeled_pool'
box_labeled_pool_dir = '/home/m112040034/workspace/simulation/box/labeled_pool'


# 所有 .mrc 檔名
mrc_files = [f for f in os.listdir(mrc_train_dir) if f.endswith('.mrc')]

# 隨機選擇48個檔名
selected_files = random.sample(mrc_files, 48)

for mrc_file in selected_files:
    base_name = os.path.splitext(mrc_file)[0]
    box_file = base_name + '.box'

    # 移動 .mrc 檔案
    mrc_src_path = os.path.join(mrc_train_dir, mrc_file)
    mrc_dst_path = os.path.join(mrc_labeled_pool_dir, mrc_file)
    shutil.move(mrc_src_path, mrc_dst_path)
    print(f'{mrc_file} moved')

    # 移動 .box 檔案
    box_src_path = os.path.join(box_train_dir, box_file)
    box_dst_path = os.path.join(box_labeled_pool_dir, box_file)
    shutil.move(box_src_path, box_dst_path)
    print(f'{box_file} moved')

print('Random move 48 mrc & box file completely')
