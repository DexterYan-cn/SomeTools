# 批量修改文件名字，用于数据集文件名报错的数据集处理

# _*_ coding: UTF-8 _*_
# Author: liming

import os
import re
import sys

# data_dir = os.getcwd() + '\\' + 'My-Scene'
data_dir = r'F:/AUDD/xml'

folder_list = os.listdir(data_dir)
folder_num = len(folder_list)
num = 1
for folder_name in folder_list: # 当前图像文件夹名称
    print('\n当前场景文件夹名字为: %s\n' % folder_name)
    image_list = os.listdir(data_dir + '/' + folder_name)
    image_num = len(image_list)

    # num = 1
    for image_name in image_list:
        #print('当前场景图像的名字为: %s' % image_name)
        old_name = data_dir + '/' + folder_name + '/' + image_name
        a = image_name[:-4]
        # new_name = data_dir + '/' + folder_name + '/' + folder_name + '_' + str(num) + '.jpg'
        new_name = data_dir + '/' + folder_name + '/' + '9' + str(num) + '.xml'
        os.rename(old_name, new_name)

        num += 1
    print('文件夹%s中的图像已更名完毕.' % folder_name)
    print('---------------------------------------')

print('所有文件夹的图像重命名完毕.')