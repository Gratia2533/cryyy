import tool

# 配置路徑
base_cmd = '/home/m112040034/.conda/envs/cryolo/bin/python -u /home/m112040034/.conda/envs/cryolo/bin/cryolo_gui.py --ignore-gooey'
train_config_path = '/home/m112040034/workspace/simulation/train_config/'
output_path = '/home/m112040034/workspace/simulation/output/'
mrc_path = '/home/m112040034/workspace/simulation/mrc/'
box_path = '/home/m112040034/workspace/simulation/box/'

evaluation_folder_path = '/home/m112040034/workspace/simulation/evaluation/BoundaryDistance'
tool.ensure_directories_exist(evaluation_folder_path)
evaluation_path = evaluation_folder_path + '/'

train_groundtruth_box_folder_path = '/home/m112040034/workspace/simulation/box/train'
tool.check_directories_exist(train_groundtruth_box_folder_path)#Groundtruth本來就應該存在

partial_box_path = f"/home/m112040034/workspace/simulation/partial_box/"

