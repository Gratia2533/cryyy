#========================General Workflow========================#
★20240826Meeting page.4 for RE1~4

@base_particle\step1_cbox2box.py
將Cryolo predict後的輸出，使用CBOX轉換為較好處理的BOX

@base_particle\step2_adjust.py
處理後的BOX與Groundtruth進行比對
當預測座標與Groundtruth在X與Y軸上，差距皆不超過150
則將該Groundtruth座標加入至「校正後的座標」

@base_particle\step3_unique.py
首先，同個座標附近可能被多次預測，因此校正後會有許多相同的座標
此處僅保留confidence最大的座標。
其次，剩下的座標，可能有部分已在前次訓練中使用，因此需要刪除已使用的座標

@base_particle\step4_filtered.py
step4會先使得只存在「校正後且尚未使用於訓練」的座標
然後需決定迭代時逐次加入的粒子數(根據confidence由小到大排序，取前X個粒子)
產出為「準備加入下次訓練」的座標

@base_particle\step5_next_ant.py
將前次已使用的座標與準備加入下次訓練的座標進行合併



#===================Variant of General Workflow===================#
※以下變體僅適用於使用前次迭代輸出模型作為Pretrained model的情況
※此流程與General Workflow使用前次迭代輸出模型作為Pretrained model的效果相差不大
※前期嘗試沒有記錄到QQ

@base_particle\step3_unique_modify.py
經step2_adjust.py校正後可能會有許多相同的座標，此處僅保留confidence最大的座標。
其次，剩下的座標，需刪除已存在used_pool的座標

@base_particle\step3-1_merged_ant.py
主要作用為更新used_pool
在首次使用時new=initial, add=iter1
後續使用時new=used_pool, add=iterk (for k = number of iteration)

@base_particle\step4_filtered_modify.py
經step3_unique_modify.py產出的unique資料夾
此處會根據confidence由小到大排序，取前X個粒子
作為下次訓練使用的粒子
※無須再經step5，此流程將保持每次iteration使用的訓練粒子數相同(除初始粒子數之外)



#============if use pretrained model for initial pick============#
@base_particle\initial_pick.py
當使用預訓練模型來進行初始粒子選取(目前使用Cryolo提供的gmodel_phosnet.h5)
預測過後的粒子需經step1轉換為box
再經step2根據Groudtruth校正(其中可能會導致同個座標點重複)
使用此python file保留唯一座標點
最後使用step4決定需要的粒子數