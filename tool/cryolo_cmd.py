#快速取得cryolo command

iter = input("For iter?\n")
action = input("For action?\n")

training = '''
'/home/m112040034/.conda/envs/cryolo/bin/python' -u '/home/m112040034/.conda/envs/cryolo/bin/cryolo_gui.py' \
--ignore-gooey train \
-c '/home/m112040034/workspace/simulation/train_config/'''+iter+'''.json' \
-w '5' \
-g 0 1 2 3 \
-nc '-1' \
--gpu_fraction '1.0' \
-e '10' \
-lft '2' \
--cleanup \
--seed '10' \
--skip_augmentation
'''


evaluation = '''
'/home/m112040034/.conda/envs/cryolo/bin/python' -u '/home/m112040034/.conda/envs/cryolo/bin/cryolo_gui.py' \
--ignore-gooey evaluation \
-c '/home/m112040034/workspace/simulation/train_config/'''+iter+'''.json' \
-w '/home/m112040034/workspace/simulation/output/'''+iter+'''/'''+iter+'''_model.h5' \
-o '/home/m112040034/workspace/simulation/evaluation/'''+iter+'''_evaluation.html' \
-i '/home/m112040034/workspace/simulation/mrc/test' \
-b '/home/m112040034/workspace/simulation/box/test' \
-g '1'
'''

#基於逐次增加粒子數使用
pred = '''
'/home/m112040034/.conda/envs/cryolo/bin/python' -u '/home/m112040034/.conda/envs/cryolo/bin/cryolo_gui.py' \
--ignore-gooey predict \
-c '/home/m112040034/workspace/simulation/train_config/'''+iter+'''.json' \
-w '/home/m112040034/workspace/simulation/output/'''+iter+'''/'''+iter+'''_model.h5' \
-i /home/m112040034/workspace/simulation/mrc/train \
-o '/home/m112040034/workspace/simulation/output/'''+iter+'''' \
-t '0' \
-d '0' \
-pbs '3' \
--gpu_fraction '1.0' \
-nc '-1' \
--norm_margin '0.0' \
-sm 'LINE_STRAIGHTNESS' \
-st '0.95' \
-sr '1.41' \
-ad '10' \
--directional_method 'PREDICTED' \
-mw '100' \
-tsr '-1' \
-tmem '0' \
-mn3d '2' \
-tmin '5' \
-twin '-1' \
-tedge '0.4' \
-tmerge '0.8'
'''

#基於逐次增加mrc使用
mrc_pred = '''
'/home/m112040034/.conda/envs/cryolo/bin/python' -u '/home/m112040034/.conda/envs/cryolo/bin/cryolo_gui.py' \
--ignore-gooey predict \
-c '/home/m112040034/workspace/simulation/train_config/'''+iter+'''.json' \
-w '/home/m112040034/workspace/simulation/output/'''+iter+'''/'''+iter+'''_model.h5' \
-i /home/m112040034/workspace/simulation/mrc/unlabeled_pool \
-o '/home/m112040034/workspace/simulation/output/'''+iter+'''' \
-t '0' \
-d '0' \
-pbs '3' \
--gpu_fraction '1.0' \
-nc '-1' \
--norm_margin '0.0' \
-sm 'LINE_STRAIGHTNESS' \
-st '0.95' \
-sr '1.41' \
-ad '10' \
--directional_method 'PREDICTED' \
-mw '100' \
-tsr '-1' \
-tmem '0' \
-mn3d '2' \
-tmin '5' \
-twin '-1' \
-tedge '0.4' \
-tmerge '0.8'
'''


if action == 't':
    print("training cmd:\n", training)
elif action == 'e':
    print("evaluation cmd:\n", evaluation)
elif action == 'p':
    print("prediction cmd:\n", pred)
elif action == 'mp':
    print("prediction cmd for mrc:\n", mrc_pred)
