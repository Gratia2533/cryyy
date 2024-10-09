import method

def EntropyScore(input_file, output_file):
    """
    將CrYOLO的輸出confidence進行Entropy score 的計算
    :param input_file: .CBOX file path
    :param output_file: output file path of preprocessing predict label
    """
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # 刪除前19行
    lines = lines[19:]

    # 處理剩下的每一行
    modified_lines = []
    for line in lines:
        values = line.split()
        if len(values) >= 9:  # 確保有足夠的值
            try:
                confidence = float(values[8])
                indicator = method.entropy_score(confidence)
                # 生成新的行，保留部分原始資料並加入處理後的 indicator
                modified_line = f"{values[0]} {values[1]} {values[3]} {values[4]} {indicator}\n"
                modified_lines.append(modified_line)
            except ValueError:
                continue

    # 寫入新的文件
    with open(output_file, 'w') as file:
        file.writelines(modified_lines)

def origin_confidence(input_file, output_file):
    """
    使用原本CrYOLO輸出的predict label confidence
    :param input_file: .CBOX file path
    :param output_file: output file path of preprocessing predict label
    """
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # 刪除前19行
    lines = lines[19:]

    # 處理剩下的每一行
    modified_lines = []
    for line in lines:
        values = line.split()
        if len(values) >= 9:  # 確保有足夠的值
            try:
                # 取得confidence應用指定的方法
                confidence = float(values[8])
                indicator = confidence  # 使用傳入的方法處理 confidence
                # 生成新的行，保留部分原始資料並加入處理後的 indicator
                modified_line = f"{values[0]} {values[1]} {values[3]} {values[4]} {indicator}\n"
                modified_lines.append(modified_line)
            except ValueError:
                continue

    # 寫入新的文件
    with open(output_file, 'w') as file:
        file.writelines(modified_lines)

def Boundary_distance(input_file, output_file, evaluation_html_dir, topt_log):
    """
    對confidence進行|confidence-topt|
    :param input_file: .CBOX file path
    :param output_file: output file path of preprocessing predict label
    :param evaluation_html_dir: CrYOLO prediction output html file
    :param topt_log: Generate a txt file to save topt value for each iteration
    """
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # 刪除前19行
    lines = lines[19:]

    # 處理剩下的每一行
    modified_lines = []

    # 取得topt
    topt = method.find_topt(evaluation_html_dir, topt_log)

    for line in lines:
        values = line.split()
        if len(values) >= 9:  # 確保有足夠的值
            try:
                confidence = float(values[8])
                indicator = abs(confidence-topt)
                # 生成新的行，保留部分原始資料並加入處理後的 indicator
                modified_line = f"{values[0]} {values[1]} {values[3]} {values[4]} {indicator}\n"
                modified_lines.append(modified_line)
            except ValueError:
                continue

    # 寫入新的文件
    with open(output_file, 'w') as file:
        file.writelines(modified_lines)


def Norm_confidence_EntropyScore(input_file, output_file, CBOX_dir):
    """
    把confidence進行min-max Scale再計算entropy score
    :param input_file: .Cbox file path
    :param output_file: output file path of preprocessing predict label
    :param CBOX_dir: the folder path of .Cbox 
    """
    with open(input_file, 'r') as file:
        lines = file.readlines()[19:]  # 刪除前19行
    min_confidence, max_confidence = method.find_confidence_range(CBOX_dir)
    modified_lines = []
    for line in lines:
        values = line.split()
        if len(values) >= 9:  # 確保有足夠的值
            try:
                confidence = float(values[8])
                # 正規化 confidence
                normalized_confidence = method.normalize_confidence(confidence, min_confidence, max_confidence)
                # 計算 entropy score
                entropyScore = method.entropy_score(normalized_confidence)
                # 保存結果
                modified_line = f"{values[0]} {values[1]} {values[3]} {values[4]} {entropyScore}\n"
                modified_lines.append(modified_line)
            except ValueError:
                continue

    with open(output_file, 'w') as file:
        file.writelines(modified_lines)