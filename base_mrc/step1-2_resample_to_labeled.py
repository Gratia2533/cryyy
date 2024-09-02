import os
import shutil
import random

# 定義目錄路徑
mrc_labeled = "/home/m112040034/workspace/simulation/mrc/labeled_pool"
mrc_history = "/home/m112040034/workspace/simulation/mrc/history"
box_labeled = "/home/m112040034/workspace/simulation/box/labeled_pool"
box_history = "/home/m112040034/workspace/simulation/box/history"

# 獲取 mrc_history 中的所有 .mrc 檔案
mrc_files = [f for f in os.listdir(mrc_history) if f.endswith('.mrc')]

# 隨機選取 14 個 .mrc 檔案
selected_mrc_files = random.sample(mrc_files, 14)

# 確保目標目錄存在，如果不存在則創建
os.makedirs(mrc_labeled, exist_ok=True)
os.makedirs(box_labeled, exist_ok=True)

# 移動選取的 .mrc 檔案及其對應的 .box 檔案
for mrc_file in selected_mrc_files:
    # 構造完整的檔案路徑
    mrc_source_file = os.path.join(mrc_history, mrc_file)
    mrc_target_file = os.path.join(mrc_labeled, mrc_file)

    # 移動 .mrc 檔案
    shutil.move(mrc_source_file, mrc_target_file)

    # 對應的 .box 檔案
    box_file = mrc_file.replace('.mrc', '.box')
    box_source_file = os.path.join(box_history, box_file)
    box_target_file = os.path.join(box_labeled, box_file)

    # 移動 .box 檔案
    shutil.move(box_source_file, box_target_file)

print(f"已隨機選取14個.mrc檔案並移動到 {mrc_labeled}，對應的.box檔案已移動到 {box_labeled}")
