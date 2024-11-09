import time
from AutoALTidy.utils.workflow import run_cmd, extract_val_loss_from_output, write_val_loss_to_file
from AutoALTidy.utils.directory import base_cmd, train_config_path, output_path, mrc_path, box_path, evaluation_path, partial_box_path, evaluation_folder_path, evaluation_valid_folder
from AutoALTidy.utils.tool import particles_amount_status, integrate_evaluation
from AutoALTidy.utils.formula import only_get_topt
import os

# 定義 val_loss_log.txt 文件
val_loss_file = os.path.join(evaluation_path, 'val_loss_log.txt')

def main(method, iou_threshold, filter_num):
    start_time = time.time()

    # 自動化流程
    for i in range(9):
        iter_index = "initial" if i == 0 else f"iter{i}"

        # Step 1: Training
        training_cmd = f"{base_cmd} train -c {train_config_path}{iter_index}.json -w 0 -g 0 1 2 3 -nc -1 --gpu_fraction 1.0 -e 10 -lft 2 --cleanup --seed 10 --skip_augmentation"
        output = run_cmd(training_cmd)

        # 提取 val_loss 並保存
        val_loss = extract_val_loss_from_output(output)
        write_val_loss_to_file(val_loss_file, iter_index, val_loss)

        if i<8:
            # Step 2: Prediction
            prediction_cmd = f"{base_cmd} predict -c {train_config_path}{iter_index}.json -w {output_path}{iter_index}/{iter_index}_model.h5 -i {mrc_path}train -o {output_path}{iter_index} -t 0 -d 0 -pbs 3 --gpu_fraction 1.0 -nc -1 --norm_margin 0.0 -sm LINE_STRAIGHTNESS -st 0.95 -sr 1.41 -ad 10 --directional_method PREDICTED -mw 100 -tsr -1 -tmem 0 -mn3d 2 -tmin 5 -twin -1 -tedge 0.4 -tmerge 0.8 -g 2"
        elif i==8:
            prediction_cmd = f"{base_cmd} predict -c {train_config_path}{iter_index}.json -w {output_path}{iter_index}/{iter_index}_model.h5 -i {mrc_path}test -o {output_path}{iter_index} -t 0 -d 0 -pbs 3 --gpu_fraction 1.0 -nc -1 --norm_margin 0.0 -sm LINE_STRAIGHTNESS -st 0.95 -sr 1.41 -ad 10 --directional_method PREDICTED -mw 100 -tsr -1 -tmem 0 -mn3d 2 -tmin 5 -twin -1 -tedge 0.4 -tmerge 0.8 -g 2"
        
        run_cmd(prediction_cmd)


        # Step 3: Evaluation on valid
        evaluation_cmd = f"{base_cmd} evaluation -c {train_config_path}{iter_index}.json -w {output_path}{iter_index}/{iter_index}_model.h5 -o {evaluation_valid_folder}{iter_index}_EVALvalid.html -i {mrc_path}valid -b {box_path}valid -g 3"
        run_cmd(evaluation_cmd)

        evaluation_html_file = evaluation_valid_folder + f"{iter_index}_EVALvalid.html"
        valid_topt = float(only_get_topt(evaluation_html_file))

        # Step 3: Evaluation on test
        evaluation_cmd = f"{base_cmd} evaluation -c {train_config_path}{iter_index}.json -w {output_path}{iter_index}/{iter_index}_model.h5 -o {evaluation_path}{iter_index}_evaluation.html -i {mrc_path}test -b {box_path}test -g 3 -t {valid_topt}"
        run_cmd(evaluation_cmd)

        # Step 4: 執行Python工具生成標註
        if i < 8:
            annotation_cmd = (
                f"python -m AutoALTidy.utils.correction "
                f"{iter_index} --method {method} --iou_threshold {iou_threshold} --filter_num {filter_num}"
            )
            run_cmd(annotation_cmd)

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total execution time: {total_time:.2f} seconds")
    integrate_evaluation(evaluation_folder_path)
    particles_amount_status(os.path.join(partial_box_path, f"{iter_index}"))
    print("The method used in this experiment:", display_dict[method_display])#執行完後確認這次選的方法
    print("All iterations completed.")

if __name__ == "__main__":
    # 顯示用的名稱
    display_dict = {
        1: "Random",
        2: "Entropy Score",
        3: "Low Confidence",
        4: "Entropy Score in Normalize Confidence",
        5: "Boundary Distance"
    }
    
    # 實際傳遞給 correction.py 的參數
    method_dict = {
        1: "random",
        2: "entropy_score",
        3: "low_confidence",
        4: "norm_conf_es",
        5: "boundary_dist"
    }

    # 顯示 method 選項，提示選擇
    method_display = int(input(f'Method: {", ".join([f"{key}.{value}" for key, value in display_dict.items()])}\nEnter integer to choose method: '))
    
    # 分別用於顯示名稱和實際參數
    display_method = display_dict.get(method_display)
    method = method_dict.get(method_display)
    print('processing method:', method)

    if method is None:
        print("Please only enter an integer from 1 to 5.")
        exit(1)  # 輸入不正確時停止
    else:
        print(f"Selected method: {display_method}")

    # 獲取其他參數
    iou_threshold = float(input('Enter IOU threshold (default is 0.7): \n') or 0.7)
    filter_num = int(input('Enter the number of each iteration to be added (default is 70): ') or 70)

    # 執行主函數
    main(method, iou_threshold, filter_num)
