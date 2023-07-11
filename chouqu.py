# 从数据集每隔几个中抽取一个数据文件
# batch_size为相隔的文件数

import os
import numpy as np
import shutil
# files = 'img/uavdtallimages_rename'
# target_files = 'img_chouqu'
# files = r'F:/original/annotations'
# target_files = r'F:/original/labels'
files = r'F:\DroneVehicle\train\trainlabel'
target_files = r'F:\DroneVehicle\train\labels'
 
def mycopyfile(srcfile, dstpath, ari):
 
    if not os.path.exists(dstpath):
        os.makedirs(dstpath)                       # 创建路径
    print(srcfile)
    shutil.copy(srcfile, target_files + "/" + ari)          # 复制文件
    print("copy %s -> %s"%(srcfile, target_files + ari))
 
 
name1 = os.listdir(files)
name = np.array(name1)
need_num = 1 # 每批图片的前几张图片
batch_size = 3  # 每批图片的数量
n = len(name)
bi = np.floor(np.arange(n) / batch_size).astype(np.int)
bn = bi[-1] + 1
for i in range(bn):
    ari = name[bi == i]
    for x in range(need_num):
        path = files + "/" + ari[x]
        mycopyfile(path, target_files, ari[x])
