#把所有當前在train的全部移動到history set

import os
import shutil

# 定義來源和目標目錄
mrc_labeled = "/home/m112040034/workspace/simulation/mrc/history"
mrc_history = "/home/m112040034/workspace/simulation/mrc/train"
box_labeled = "/home/m112040034/workspace/simulation/box/history"
box_history = "/home/m112040034/workspace/simulation/box/train"

# 確保目標目錄存在，如果不存在則創建
if not os.path.exists(mrc_history):
    os.makedirs(mrc_history)

# 列出來源目錄中的所有檔案
files = os.listdir(mrc_labeled)

# 將每個檔案從來源目錄移動到目標目錄
for file in files:
    source_file = os.path.join(mrc_labeled, file)
    target_file = os.path.join(mrc_history, file)
    shutil.move(source_file, target_file)

print(f"mrc: from {mrc_labeled} move to {mrc_history}")

# 確保目標目錄存在，如果不存在則創建
if not os.path.exists(box_history):
    os.makedirs(box_history)

# 列出來源目錄中的所有檔案
files = os.listdir(box_labeled)

# 將每個檔案從來源目錄移動到目標目錄
for file in files:
    source_file = os.path.join(box_labeled, file)
    target_file = os.path.join(box_history, file)
    shutil.move(source_file, target_file)

print(f"所有檔案已從 {box_labeled} 移動到 {box_history}")

