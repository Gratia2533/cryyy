from . import tool

# 配置路徑
##應為固定路徑
#command line的方式運行CrYOLO的prefix
base_cmd = '/home/m112040034/.conda/envs/cryolo/bin/python -u /home/m112040034/.conda/envs/cryolo/bin/cryolo_gui.py --ignore-gooey'
train_config_path = '/home/m112040034/workspace/simulation/train_config/'#train config路徑
output_path = '/home/m112040034/workspace/simulation/output/'#訓練模型的輸出位置、預測標籤的輸出位置
mrc_path = '/home/m112040034/workspace/simulation/mrc/'#全部的mrc資料夾路徑，該目錄下應該要有train、test、valid三個資料夾
box_path = '/home/m112040034/workspace/simulation/box/'#全部的box資料夾路徑，該目錄下應該要有train、test、valid三個資料夾
train_groundtruth_box_folder_path = '/home/m112040034/workspace/simulation/box/train'
tool.check_directories_exist(train_groundtruth_box_folder_path)#Groundtruth本來就應該存在


##應用不同method時，應替換這個路徑，避免覆蓋掉evaluation的結果
evaluation_folder_path = '/home/m112040034/workspace/simulation/evaluation/Random10028'
tool.ensure_directories_exist(evaluation_folder_path)
evaluation_path = evaluation_folder_path + '/'

#Catcha Topt would be used
evaluation_valid_folder_path = evaluation_path + 'EVALvalid'
tool.ensure_directories_exist(evaluation_valid_folder_path)
evaluation_valid_folder = evaluation_valid_folder_path + '/'


##每次iteration使用的粒子儲存的地方，須避免覆蓋或進行另一次實驗重複寫入
partial_box_path = f"/home/m112040034/workspace/simulation/partial_box/"

