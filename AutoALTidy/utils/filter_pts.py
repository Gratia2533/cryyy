import os
import pandas as pd
from sklearn.utils import shuffle 


#========Step4:filter========#
def filter_row_data(unique_dir, filter_num, filter_dir, acd):
    """
    讀取 unique_dir 中的所有 .box 檔案，合併資料並篩選出前 filter_num 條資料。
    然後按照檔案名分組，將結果寫入 filter_dir，並檢查並創建缺少的 .box 檔案。

    :param unique_dir: 包含 .box 檔案的目錄
    :param filter_num: 要保留的行數
    :param filter_dir: 只包含準備要新加入的row data的輸出路徑
    :param acd: 決定要取較小的值或較大的值(True = 取較小, False = 取較大)
    """
    # 讀取所有 .box 文件
    data_frames = []
    for file_name in os.listdir(unique_dir):
        if file_name.endswith('.box'):
            file_path = os.path.join(unique_dir, file_name)
            # 檢查檔案是否為空
            if os.path.getsize(file_path) > 0:
                # 讀取文件，以空格為分隔符
                df = pd.read_csv(file_path, delimiter=' ', header=None)
                # 新增 column 為檔案名
                df['filename'] = file_name
                data_frames.append(df)
            else:
                print(f"Skipping empty file: {file_name}")

    # 合併所有 dataframe
    if data_frames:  # 檢查是否有任何非空檔案
        combined_df = pd.concat(data_frames, ignore_index=True)
        # 按照每一行第4個元素排序(視方法ascending會調整，False取較大，True取較小)
        combined_df_sorted = combined_df.sort_values(by=4, ascending=acd)
        # 只保留前 filter_num 行數據
        top_X_df = combined_df_sorted.head(filter_num).reset_index(drop=True)
        top_X_df = top_X_df.drop(columns=[4])

        # 按照 filename 分組並將資料寫入對應的檔案
        for filename, group in top_X_df.groupby('filename'):
            # 設定檔案路徑
            file_path = os.path.join(filter_dir, filename)
            # 將分組資料寫入對應的檔案
            group.drop('filename', axis=1).to_csv(file_path, sep=' ', header=False, index=False)

        print("The data has been successfully written to the corresponding .box file")
    else:
        print("No non-empty .box files found to process.")

    # 檢查並創建缺少的 .box 檔案
    expected_files = [f"micrograph_{i}.box" for i in range(70)]
    existing_files = os.listdir(filter_dir)

    missing_files = set(expected_files) - set(existing_files)
    for missing_file in missing_files:
        open(os.path.join(filter_dir, missing_file), 'w').close()

    print(f"Missing files have been created: {', '.join(missing_files)}")

#if random
def random_filter_row_data(unique_dir, filter_num, filter_dir):
    """
    隨機抽取 .box 文件中的行數據，並寫入到對應的檔案中。

    :param unique_dir: 包含 .box 文件的目錄路徑
    :param filter_num: 每個檔案隨機抽取的行數
    :param filter_dir: 輸出抽取結果的目錄
    """
    # 讀取所有 .box 文件
    data_frames = []
    for file_name in os.listdir(unique_dir):
        if file_name.endswith('.box'):
            file_path = os.path.join(unique_dir, file_name)
            # 檢查檔案是否為空
            if os.path.getsize(file_path) > 0:
                # 讀取文件，以空格為分隔符
                df = pd.read_csv(file_path, delimiter=' ', header=None)
                # 新增 column 為檔案名
                df['filename'] = file_name
                data_frames.append(df)
            else:
                print(f"Skipping empty file: {file_name}")

    # 合併所有 dataframe
    if data_frames:  # 檢查是否有任何非空檔案
        combined_df = pd.concat(data_frames, ignore_index=True)
        # 隨機抽取前 filter_num 行數據
        shuffled_df = shuffle(combined_df).reset_index(drop=True)
        top_X_df = shuffled_df.head(filter_num).reset_index(drop=True)
        top_X_df = top_X_df.drop(columns=[4])

        # 按照 filename 分組並將資料寫入對應的檔案
        for filename, group in top_X_df.groupby('filename'):
            # 設定檔案路徑
            file_path = os.path.join(filter_dir, filename)
            # 將分組資料寫入對應的檔案
            group.drop('filename', axis=1).to_csv(file_path, sep=' ', header=False, index=False)

        print("The data has been successfully written to the corresponding .box file")
    else:
        print("No non-empty .box files found to process.")

    # 檢查並創建缺少的 .box 檔案
    expected_files = [f"micrograph_{i}.box" for i in range(70)]
    existing_files = os.listdir(filter_dir)

    missing_files = set(expected_files) - set(existing_files)
    for missing_file in missing_files:
        open(os.path.join(filter_dir, missing_file), 'w').close()

    print(f"Missing files have been created: {', '.join(missing_files)}")