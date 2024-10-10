import os
import argparse
from . import cbox2box as cb2b
from . import tool, directory, regular, filter_pts, formula

def main():
    """
    根據 method 選擇不同的校正方法
    """
    # 設定命令行參數解析
    parser = argparse.ArgumentParser(description='Generate annotations based on the current iteration.')
    parser.add_argument('iter_index', type=str, help='Current iteration (e.g., "initial" or "iter7")')
    parser.add_argument('--method', type=str, required=True, help='The method used for correction.')
    parser.add_argument('--iou_threshold', type=float, default=0.7, help='IOU threshold for correction.')
    parser.add_argument('--filter_num', type=int, default=70, help='Number of particles to filter.')
    
    args = parser.parse_args()

    iter_index = args.iter_index
    method = args.method
    iou_threshold = args.iou_threshold
    filter_num = args.filter_num

    if iter_index == 'initial':
        next_iter = 'iter1'
    else:
        part1 = ''.join([char for char in iter_index if not char.isdigit()])
        part2 = ''.join([char for char in iter_index if char.isdigit()])
        next_iter = part1 + str(int(part2) + 1)

    # 使用從 directory 模組中導入的路徑變數
    CBOX_dir = os.path.join(directory.output_path, f"{iter_index}/CBOX")
    box_dir = os.path.join(directory.output_path, f"{iter_index}/process/box")
    gt_dir = directory.train_groundtruth_box_folder_path  # Groundtruth 路徑
    adjust_dir = os.path.join(directory.output_path, f"{iter_index}/process/adjust")
    unique_dir = os.path.join(directory.output_path, f"{iter_index}/process/unique")
    current_dir = os.path.join(directory.partial_box_path, f"{iter_index}")
    filter_dir = os.path.join(directory.output_path, f"{iter_index}/process/filter")
    next_dir = os.path.join(directory.partial_box_path, f"{next_iter}")

    evaluation_html_file = directory.evaluation_path + f"{iter_index}_evaluation.html"
    topt_log = directory.evaluation_path + "topt_log.txt"

    # 確保路徑存在，不存在會創建
    tool.ensure_directories_exist(box_dir, adjust_dir, unique_dir, filter_dir, next_dir)
    # 確保檔案存在，不存在則報錯
    tool.check_file_exists(evaluation_html_file)
    # 原本應該就要存在的路徑，不存在將報錯
    tool.check_directories_exist(CBOX_dir, gt_dir, current_dir)

    # 先決定 `step1` 中要使用的處理函數
    def get_step1_function(method):
        if method == "entropy_score":
            return cb2b.EntropyScore
        elif method == "confidence" or method == "random":
            return cb2b.origin_confidence
        elif method == "boundary_dist":
            topt = formula.find_topt(evaluation_html_file, topt_log)
            return lambda input_file_path, output_file_path: cb2b.Boundary_distance(input_file_path, output_file_path, topt)
        elif method == "norm_conf_es":
            return lambda input_file_path, output_file_path: cb2b.Norm_confidence_EntropyScore(input_file_path, output_file_path, CBOX_dir)
        else:
            raise ValueError(f"Unsupported method: {method}")

    # 判斷 `step1` 中的處理函數
    step1_function = get_step1_function(method)

    # $====================================step1====================================$#
    for filename in os.listdir(CBOX_dir):
        if filename.endswith(".cbox"):
            input_file_path = os.path.join(CBOX_dir, filename)
            output_file_path = os.path.join(box_dir, filename.replace(".cbox", ".box"))

            # 調用選擇的函數處理
            step1_function(input_file_path, output_file_path)

    # $====================================step2====================================$#
    regular.correction_by_iou(gt_dir, box_dir, adjust_dir, iou_th=iou_threshold)

    # $====================================step3====================================$#
    regular.unique_row_data(adjust_dir, unique_dir, current_dir)

    # $====================================step4====================================$#
    '''
    根據 method 判斷過濾行為，只需判斷一次，acd 是 sort_values 的 ascending
    如果是Entropy Score或Entropy Score in Normalize Confidence，則要取較大值
    如果是Low Confidence或Boundary Distance，則要取較小值
    '''
    acd = method not in ["entropy_score", "norm_conf_es"]

    if method == "random":
        #隨機挑選，只需要check IOU，因此不需要設置acd
        filter_pts.random_filter_row_data(unique_dir, filter_num, filter_dir)
    else:
        filter_pts.filter_row_data(unique_dir, filter_num, filter_dir, acd)

    # $====================================step5====================================$#
    regular.generate_next_iter_annot(current_dir, filter_dir, next_dir)

if __name__ == "__main__":
    main()
