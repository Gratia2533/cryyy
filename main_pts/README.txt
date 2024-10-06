autoAL_basePts.py

1.需要修改"#設定路徑"

2.如果epoch數有更改，"#提取val_loss"的if處也要對應修改   
                                                                             
3.每次加入個數以及IOU threshold的設定需在以下★.py修改 
                                                                                    
4.Training config的路徑也要檢查有符合autoAL_basePts.py的設定                        

5."initial_random_select.py，輸入需求個數可以從Groundtruth抽取作為初始選取粒子 


initial_random_select.py:Enter the number required for random selection, then generate use_pool/initial & unuse_pool/initial.

★only_IOU.py:Only checked through IOU, not filtered according to any indicators.

★entropy_score_adjust.py:Check through IOU and select those with larger entropy score.

★low_confidence_adjust.py:Check through IOU and select those with lower confidence.

★norm_conf_es.py:First normalize the confidence and then calculate the entropy score. After checking through IOU, select those with larger entropy scores.

★boundary_dist.py:Check through IOU and select those with lower |confidence-topt|(boundary distance).

autoAL_basePts.py:Replace the python file in the annotation_cmd in the Step4 with the above mark ★ to achieve active learning with different methods