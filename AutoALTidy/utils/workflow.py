import subprocess
import re

def run_cmd(cmd):
    """執行命令並捕獲輸出"""
    print(f"Running: {cmd}")
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True)
    output = ""
    for line in process.stdout:
        print(line, end='')
        output += line
    process.wait()
    return output

def extract_val_loss_from_output(output):
    """提取 val_loss"""
    final_val_loss = None
    for line in output.splitlines():
        if "Epoch 00005:" in line and "val_loss" in line:
            # 使用正則表達式提取符合 0.XXXXX 格式的數字
            matches = re.findall(r"\b0\.\d{5}\b", line)
            if matches:
                losses = [float(match) for match in matches]
                if len(losses) == 1:
                    final_val_loss = losses[0]
                elif len(losses) == 2:
                    final_val_loss = min(losses)
    return final_val_loss

def write_val_loss_to_file(val_loss_file, iter_name, val_loss):
    """保存 val_loss 到文件"""
    if val_loss is not None:
        with open(val_loss_file, 'a') as f:
            f.write(f"{iter_name}:{val_loss:.5f}\n")
        print(f"Saved {iter_name} val_loss: {val_loss:.5f}")
    else:
        print(f"No val_loss found for {iter_name}.")
