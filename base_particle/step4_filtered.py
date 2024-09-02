#將經step3處理過後的標註，根據confidence由小到大排序
#取前X的資料行作為要加入下次訓練的標註
import pandas as pd
import os

iter = input("iter?\n")

# 設定檔案路徑
input_dir = '/home/m112040034/workspace/simulation/output/'+iter+'/process/unique'
# 設定資料夾路徑
output_dir = '/home/m112040034/workspace/simulation/output/'+iter+'/process/filter'
# 確保輸出路徑存在
os.makedirs(output_dir, exist_ok=True)

# 讀取所有 .box 文件
data_frames = []
for file_name in os.listdir(input_dir):
    if file_name.endswith('.box'):
        file_path = os.path.join(input_dir, file_name)
        # 檢查檔案是否為空
        if os.path.getsize(file_path) > 0:
            # 讀取文件，以空格為分隔符
            df = pd.read_csv(file_path, delimiter=' ', header=None)
            # 新增column為檔案名
            df['filename'] = file_name
            data_frames.append(df)
        else:
            print(f"Skipping empty file: {file_name}")

# 合併所有dataframe
if data_frames:  # 檢查是否有任何非空檔案
    combined_df = pd.concat(data_frames, ignore_index=True)
    # 按照每一行第4個元素由小到大排序(confidence)
    combined_df_sorted = combined_df.sort_values(by=4, ascending=True)
    # 只保留前X行數據
    top_X_df = combined_df_sorted.head(930).reset_index(drop=True)#調整要新增的粒子數
    top_X_df = top_X_df.drop(columns=[4])

    # 按照 filename 分組並將資料寫入對應的檔案
    for filename, group in top_X_df.groupby('filename'):
        # 設定檔案路徑
        file_path = os.path.join(output_dir, filename)
        # 將分組資料寫入對應的檔案
        group.drop('filename', axis=1).to_csv(file_path, sep=' ', header=False, index=False)

    print("The data has been successfully written to the corresponding .box file")
else:
    print("No non-empty .box files found to process.")

# 檢查並創建缺少的 .box 檔案(確保要加入下次訓練使用的標註，有對應數量的檔案)
expected_files = [f"micrograph_{i}.box" for i in range(240)]
existing_files = os.listdir(output_dir)

missing_files = set(expected_files) - set(existing_files)
for missing_file in missing_files:
    open(os.path.join(output_dir, missing_file), 'w').close()

print(f"Missing files have been created: {', '.join(missing_files)}")
