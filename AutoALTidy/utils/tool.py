import os
from bs4 import BeautifulSoup
import pandas as pd

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

#================================================================================#
    '''
    以下3個函式的差異在於
    ensure_directories_exist:不存在會去建立資料夾
    check_directories_exist:單純檢查是否存在資料夾，不存在則報錯
    check_file_exists:用於確認是否有該"檔案"
    '''
#================================================================================#

# 確保路徑存在，若不存在則建立
def ensure_directories_exist(*directories):
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Directory created: {directory}")
        else:
            print(f"Directory already exists: {directory}")

# 檢查路徑是否存在，若不存在則返回錯誤訊息
def check_directories_exist(*directories):
    missing_directories = []
    for directory in directories:
        if not os.path.exists(directory):
            missing_directories.append(directory)

    if missing_directories:
        raise FileNotFoundError(f"Please to check following path: {', '.join(missing_directories)}")
    else:
        print("All paths that should exist have been confirmed")

def check_file_exists(file_path):
    """
    確認檔案是否存在，若不存在則報錯
    :param file_path: 要確認的檔案路徑
    :raises FileNotFoundError: 若檔案不存在則拋出錯誤
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    else:
        print(f"File confirmed: {file_path}")
#================================================================================#
#================================================================================#

#確認使用的粒子數量
def particles_amount_status(path):
    """
    計算指定路徑下所有 .box 檔案中的總行數（即粒子數量）。 
    :param path (str): 包含 .box 檔案的資料夾路徑。
    :return:total_lines (int): 總粒子數量。
    """
    # 初始化變數
    total_lines = 0

    # 遍歷路徑中的所有 .box 檔案
    for filename in os.listdir(path):
        if filename.endswith(".box"):
            file_path = os.path.join(path, filename)
            with open(file_path, 'r') as file:
                lines = file.readlines()
                total_lines += len(lines)

    # 輸出結果
    print(f"Total particles: {total_lines}")

#統整evaluation多次迭代的結果
def integrate_evaluation(folder_path):
    """
    整合資料夾中的HTML文件，提取結果並生成CSV文件。
    
    :param folder_path: 包含HTML文件的資料夾路徑
    :return: 輸出生成的CSV文件路徑
    """
    # 定義欄位名稱
    columns = [
        'iter', 'AUC', 'Topt', 'R Topt', 'R 0.3', 'R 0.2',
        'P Topt', 'P 0.3', 'P 0.2', 'F1 Topt', 'F1 0.3', 'F1 0.2',
        'IOU Topt', 'IOU 0.3', 'IOU 0.2',
        'Topt F1', 'Topt F2'
    ]

    # 定義排序順序
    iter_order = ['initial', 'iter1', 'iter2', 'iter3', 'iter4', 'iter5', 'iter6', 'iter7', 'iter8']

    # 替換資料夾路徑中的反斜杠
    
    # 搜尋目錄中的HTML文件
    html_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.html')]

    # 創建空的DataFrame列表
    df_list = []

    for html_file in html_files:
        with open(html_file, "r", encoding="utf-8") as file:
            html_content = file.read()

        # 解析HTML
        soup = BeautifulSoup(html_content, "lxml")

        # 提取<pre>標籤中的文本內容
        pre_content = soup.find("pre").get_text()

        # 將文本內容按行分割並存儲在列表中
        lines = pre_content.splitlines()
        info = lines[19]  # 假設表格內容在第20行
        content = [item.strip() for item in info.strip('|').split('|')]
        bct_F1 = [item.strip() for item in lines[22].strip(' ').split(' ')][9]
        bct_F2 = [item.strip() for item in lines[23].strip(' ').split(' ')][9]

        # 取得檔名作為第一個元素
        filename = os.path.splitext(os.path.basename(html_file))[0]
        filename = filename.split('_')[0]
        content[0] = filename
        content.append(bct_F1)
        content.append(bct_F2)

        # 轉換成DataFrame的一行
        df_list.append(pd.DataFrame([content], columns=columns))

    # 合併所有DataFrame
    df = pd.concat(df_list, ignore_index=True)

    # 設置 iter 欄位為類別型，並指定排序順序
    df['iter'] = pd.Categorical(df['iter'], categories=iter_order, ordered=True)

    # 按照 iter 欄位進行排序
    df = df.sort_values('iter').reset_index(drop=True)

    # 生成輸出文件名
    filename = folder_path.split('/')[-1]
    output_file = os.path.join(folder_path, f"{filename}_result.csv")

    # 將DataFrame存成CSV文件
    df.to_csv(output_file, index=False)

    print(f"All evaluation result of each iterations are save to: {output_file}")
    return output_file
