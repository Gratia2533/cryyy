import os
import re
import subprocess
import time

#num_iteration = 9 #iteraion次數包含initial那次

# 設定路徑
base_cmd = '/home/m112040034/.conda/envs/cryolo/bin/python -u /home/m112040034/.conda/envs/cryolo/bin/cryolo_gui.py --ignore-gooey'
train_config_path = '/home/m112040034/workspace/simulation/train_config/'
output_path = '/home/m112040034/workspace/simulation/output/'
mrc_path = '/home/m112040034/workspace/simulation/mrc/'
box_path = '/home/m112040034/workspace/simulation/box/'
evaluation_path = '/home/m112040034/workspace/simulation/evaluation/pts280_IOU7_random/'

# 執行命令並捕獲輸出
def run_cmd(cmd):
    print(f"Running: {cmd}")
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True)
    output = ""
    for line in process.stdout:
        print(line, end='')
        output += line
    process.wait()
    return output

# 提取 val_loss
def extract_val_loss_from_output(output):
    final_val_loss = None
    for line in output.splitlines():
        if "Epoch 00005:" in line and "val_loss" in line:
            # 使用正則表達式提取符合 0.XXXXX 格式的數字
            matches = re.findall(r"\b0\.\d{5}\b", line)
            if matches:
                losses = [float(match) for match in matches]
                # 如果有兩個小數，取最小值
                if len(losses) == 1:
                    final_val_loss = losses[0]
                elif len(losses) == 2:
                    final_val_loss = min(losses)
    return final_val_loss

# 保存 val_loss 到文件
def write_val_loss_to_file(val_loss_file, iter_name, val_loss):
    if val_loss is not None:
        with open(val_loss_file, 'a') as f:
            f.write(f"{iter_name}:{val_loss:.5f}\n")
        print(f"Saved {iter_name} val_loss: {val_loss:.5f}")
    else:
        print(f"No val_loss found for {iter_name}.")

# 定義 val_loss_log.txt 文件
val_loss_file = os.path.join(evaluation_path, 'val_loss_log.txt')

start_time = time.time()

# 自動化流程
for i in range(1):
    iter = "initial" if i == 0 else f"iter{i}"

    # Step 1: Training
    training_cmd = f"{base_cmd} train -c {train_config_path}{iter}.json -w 0 -g 0 1 2 -nc -1 --gpu_fraction 1.0 -e 10 -lft 2 --cleanup --seed 10 --skip_augmentation"
    output = run_cmd(training_cmd)
    
    # 提取 val_loss 並保存
    val_loss = extract_val_loss_from_output(output)
    write_val_loss_to_file(val_loss_file, iter, val_loss)
    
    # Step 2: Prediction
    if i < 8:  # 在 iter8 時跳過這一步
        prediction_cmd = f"{base_cmd} predict -c {train_config_path}{iter}.json -w {output_path}{iter}/{iter}_model.h5 -i {mrc_path}train -o {output_path}{iter} -t 0 -d 0 -pbs 3 --gpu_fraction 1.0 -nc -1 --norm_margin 0.0 -sm LINE_STRAIGHTNESS -st 0.95 -sr 1.41 -ad 10 --directional_method PREDICTED -mw 100 -tsr -1 -tmem 0 -mn3d 2 -tmin 5 -twin -1 -tedge 0.4 -tmerge 0.8"
        run_cmd(prediction_cmd)
    
    # Step 3: Evaluation
    evaluation_cmd = f"{base_cmd} evaluation -c {train_config_path}{iter}.json -w {output_path}{iter}/{iter}_model.h5 -o {evaluation_path}{iter}_evaluation.html -i {mrc_path}test -b {box_path}test -g 1"
    run_cmd(evaluation_cmd)
    
    #Step 4: 執行Python工具生成標註
    if i < 8:  # 在 iter8 時跳過這一步
        #annotation_cmd = f"python /home/m112040034/workspace/simulation/tool/main/entropy_score_adjust.py {iter}"
        #隨機加入時使用
        annotation_cmd = f"python /home/m112040034/workspace/simulation/tool/main/only_IOU.py {iter}"
        #選擇較低信心程度使用
        #annotation_cmd = f"python /home/m112040034/workspace/simulation/tool/main/low_confidence_adjust.py {iter}"
        #使用正規化後再求entropy score
        #annotation_cmd = f"python /home/m112040034/workspace/simulation/tool/main/norm_conf_es.py.py {iter}"
        run_cmd(annotation_cmd)

end_time = time.time()
total_time = end_time - start_time
print(f"Total execution time: {total_time:.2f} seconds")
print("All iterations completed.")
