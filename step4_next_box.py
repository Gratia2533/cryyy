#將要加入的標註融合到上一次loop的標註檔裡，且刪除重複的部分
import os

iter = "10"
add_dir = "/home/m112040034/workspace/simulation/output/loop"+iter+"/process/add"
prvs_dir = "/home/m112040034/workspace/simulation/quarter_box/loop"+iter
next_dir = "/home/m112040034/workspace/simulation/quarter_box/loop"+str(int(iter)+1)

# check path exists
os.makedirs(next_dir, exist_ok=True)

# 讀取並合併 add 和 prvs 路徑的檔案
for filename in os.listdir(add_dir):
    if filename.endswith(".box"):
        add_file = os.path.join(add_dir, filename)
        prvs_file = os.path.join(prvs_dir, filename)
        next_file = os.path.join(next_dir, filename)

        with open(prvs_file, 'r') as f_prvs:
            prvs_lines = f_prvs.readlines()
        
        with open(add_file, 'r') as f_add:
            add_lines = f_add.readlines()

        # 合併 add 的內容到 prvs
        merged_lines = prvs_lines + add_lines

        # 使用集合去除重複行，並保留順序
        unique_lines = list(dict.fromkeys(merged_lines))

        # 計算刪除的重複行數量及內容
        deleted_lines = len(merged_lines) - len(unique_lines)
        deleted_content = set(merged_lines) - set(unique_lines)

        # 寫入到 next 目錄
        with open(next_file, 'w') as f_next:
            f_next.writelines(unique_lines)

        # 列出刪除的部分
        if deleted_lines > 0:
            print(f"Delete {filename}:{deleted_lines}")
            for line in deleted_content:
                print(line.strip())

# 顯示所有 box 檔案總共有幾行
total_lines = 0
for filename in os.listdir(next_dir):
    if filename.endswith(".box"):
        next_file = os.path.join(next_dir, filename)
        with open(next_file, 'r') as f_next:
            lines_count = len(f_next.readlines())
            total_lines += lines_count

print(f"Now have {total_lines} particles.")
