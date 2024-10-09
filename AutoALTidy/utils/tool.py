import os


#========tool========#
def read_box_file(file_path):
    '''
    讀取.box file
    :param filepath: file path for .box file
    '''
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def write_box_file(file_path, lines):
    '''
    寫入新的.box file
    :param filepath: the new file path for .box file
    :param lines: the content would be write in
    '''
    with open(file_path, 'w') as file:
        file.writelines(lines)

# 確保目錄存在，若不存在則創建
def ensure_directories_exist(*directories):
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Directory created: {directory}")
        else:
            print(f"Directory already exists: {directory}")

# 檢查目錄是否存在，若不存在則返回錯誤訊息
def check_directories_exist(*directories):
    missing_directories = []
    for directory in directories:
        if not os.path.exists(directory):
            missing_directories.append(directory)

    if missing_directories:
        raise FileNotFoundError(f"Please to check following path: {', '.join(missing_directories)}")
    else:
        print("All paths that should exist have been confirmed")


#確認使用的粒子數量
def particles_amount_status(path):
    """
    計算指定目錄下所有 .box 檔案中的總行數（即粒子數量）。 
    :param path (str): 包含 .box 檔案的目錄路徑。
    :return:total_lines (int): 總粒子數量。
    """
    # 初始化變數
    total_lines = 0

    # 遍歷目錄中的所有 .box 文件
    for filename in os.listdir(path):
        if filename.endswith(".box"):
            file_path = os.path.join(path, filename)
            with open(file_path, 'r') as file:
                lines = file.readlines()
                total_lines += len(lines)

    # 輸出結果
    print(f"Total particles: {total_lines}")
