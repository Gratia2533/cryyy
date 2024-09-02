#========================General Workflow========================#
★20240805Meeting page.5 & page.6 for E4, E5

@base_mrc\initial_sampling_mrc.py
隨機選擇48個.mrc&.box檔案作為初始訓練數據

@base_mrc\step1_cbox2box_by_confidence.py
對unlabeled_pool進行predict後
將Cryolo predict後的輸出，使用CBOX轉換為較好處理的BOX

@base_mrc\step2_move_pool.py
首先計算每張mrc檔案的不確定性
方法：
將每張mrc的預測座標，依照confidence由小到大排序，
取前50%的值做算術平均。
每次找出前28張小的前半confidence算術平均，加入label_pool

#===================Variant of General Workflow===================#
★20240805Meeting page.5 & page.7 for E6

※以下變體僅適用於使用前次迭代輸出模型作為Pretrained model的情況

@base_mrc\step1-1_move_to_history.py
將所有在labeled_pool裡的數據放入history

@base_mrc\step1-2_resample_to_labeled.py
從history隨機選取14個數據放入labeled_pool

※結合step2_move_to_history加入的28張
此流程將保持每次訓練使用數據量同樣為42個.mrc&.box

#==============================Tool==============================#
@base_mrc\folder_status.py
查看當前各池.mrc以及.box檔案數量