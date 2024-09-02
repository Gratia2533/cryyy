#確認當前各路徑的mrc數量
import os

# 路徑
mrc_unlabeled_dir = '/home/m112040034/workspace/simulation/mrc/unlabeled_pool'
mrc_labeled_dir = '/home/m112040034/workspace/simulation/mrc/labeled_pool'
box_unlabeled_dir = '/home/m112040034/workspace/simulation/box/unlabeled_pool'
box_labeled_dir = '/home/m112040034/workspace/simulation/box/labeled_pool'
mrc_history_dir = "/home/m112040034/workspace/simulation/mrc/history"
box_history_dir = "/home/m112040034/workspace/simulation/box/history"

print(' mrc unlabeled:',len(os.listdir(mrc_unlabeled_dir)),
      '\n mrc labeled:',len(os.listdir(mrc_labeled_dir)),
      '\n mrc history:',len(os.listdir(box_history_dir)),
      '\n box unlabeled:',len(os.listdir(box_unlabeled_dir)),
      '\n box labeled:',len(os.listdir(box_labeled_dir)),
      '\n box history:',len(os.listdir(box_history_dir)))

#print(os.listdir(mrc_labeled_dir))