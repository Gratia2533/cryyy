initial_random_select.py:Enter the number required for random selection, then generate use_pool/initial & unuse_pool/initial.

★only_IOU.py:Only checked through IOU, not filtered according to any indicators.

★entropy_score_adjust.py:Check through IOU and select those with larger entropy score.

★low_confidence_adjust.py:Check through IOU and select those with lower confidence.

★norm_conf_es.py:First normalize the confidence and then calculate the entropy score. After checking through IOU, select those with larger entropy scores.

autoAL_basePts.py:Replace the python file in the annotation_cmd in the Step4 with the above mark ★ to achieve active learning with different methods