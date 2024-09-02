#將這次要加入的標註，加入上一次的標註，成為下一次的標註
import os

iter = input("iter?\n")
next = input("next?\n")
# 設定路徑
path_A = '/home/m112040034/workspace/simulation/partial_box/'+iter
path_B = '/home/m112040034/workspace/simulation/output/'+iter+'/process/filter'
output_dir = '/home/m112040034/workspace/simulation/partial_box/'+next

# 確保輸出路徑存在
os.makedirs(output_dir, exist_ok=True)

def merge_files(path_A, path_B, output_dir):
    files_A = os.listdir(path_A)
    files_B = os.listdir(path_B)
    
    # 確保兩個路徑下的檔案數量和檔案名稱都一致
    if len(files_A) != len(files_B) or sorted(files_A) != sorted(files_B):
        raise ValueError("Directories A and B do not have the same number of files or identical filenames.")

    for filename in files_B:
        file_path_B = os.path.join(path_B, filename)
        output_file_path = os.path.join(output_dir, filename)

        # 檢查 B 中檔案是否為空
        if os.path.getsize(file_path_B) > 0:
            # 讀取 B 路徑中的檔案內容
            with open(file_path_B, 'r') as file_B:
                lines_B = file_B.readlines()

            # 讀取 A 路徑中的檔案內容
            file_path_A = os.path.join(path_A, filename)
            with open(file_path_A, 'r') as file_A:
                lines_A = file_A.readlines()

            # 合併檔案內容
            lines_A.extend(lines_B)

            # 寫入合併後的內容到新的路徑
            with open(output_file_path, 'w') as file_out:
                file_out.writelines(lines_A)
        else:
            # 如果 B 中的檔案為空，直接將 A 的檔案複製到輸出路徑
            file_path_A = os.path.join(path_A, filename)
            with open(file_path_A, 'r') as file_A:
                lines_A = file_A.readlines()

            with open(output_file_path, 'w') as file_out:
                file_out.writelines(lines_A)

    # 輸出所有檔案的總行數
    total_lines = 0
    for filename in os.listdir(output_dir):
        file_path = os.path.join(output_dir, filename)
        with open(file_path, 'r') as file:
            total_lines += len(file.readlines())

    print("Files have been merged successfully.")
    print(f"particles: {total_lines}")

# 執行合併
merge_files(path_A, path_B, output_dir)
