# 统计数据集中大中小数据的占比，使用coco指标。  即统计某个类别的标签，大中小目标的占比
# 改1：102行103行图像大小
# 改2：113行数据集类别
# 改3：161行的数据集label文件指向
# 改4：172行的统计类别数



# 1、统计数据集中小、中、大 GT的个数
# 2、统计某个类别小、中、大 GT的个数
# 3、统计数据集中ss、sm、sl GT的个数
import os
from pathlib import Path
import matplotlib.pyplot as plt

# 设置中文字体为微软雅黑
plt.rcParams['font.sans-serif'] = 'SimHei'

# coding=utf-8  2023.5.10加入
# def check_charset(file_path):
#     import chardet
#     with open(file_path, "rb") as f:
#         data = f.read(4)
#         charset = chardet.detect(data)['encoding']
#     return charset

def getGtAreaAndRatio(label_dir):
    """
    得到不同尺度的gt框个数
    :params label_dir: label文件地址
    :return data_dict: {dict: 3}  3 x {'类别':{’area':[...]}, {'ratio':[...]}}
    """
    data_dict = {}
    assert Path(label_dir).is_dir(), "label_dir is not exist"
    
    # encoding=check_charset(label_dir)
    txts = os.listdir(label_dir)  # 得到label_dir目录下的所有txt GT文件


    for txt in txts:  # 遍历每一个txt文件
        with open(os.path.join(label_dir, txt), 'r') as f:  # 打开当前txt文件 并读取所有行的数据
            lines = f.readlines()
        # with open(os.path.join(label_dir, txt), encoding=check_charset(os.path.join(label_dir, txt))) as f:  # 打开当前txt文件 并读取所有行的数据
        #     lines = f.readlines()

        for line in lines:  # 遍历当前txt文件中每一行的数据
            temp = line.split()  # str to list{5}
            coor_list = list(map(lambda x: x, temp[1:]))  # [x, y, w, h]
            area = float(coor_list[2]) * float(coor_list[3])  # 计算出当前txt文件中每一个gt的面积
            # center = (int(coor_list[0] + 0.5*coor_list[2]),
            #           int(coor_list[1] + 0.5*coor_list[3]))
            
            # 自改添加 由于标注问题，会出现被除数为0情况，跳过这条数据
            if float(coor_list[3]) == 0 or float(coor_list[2]) == 0:
                continue
            # ——————————————————

            ratio = round(float(coor_list[2]) / float(coor_list[3]), 2)  # 计算出当前txt文件中每一个gt的 w/h

            if temp[0] not in data_dict:
                data_dict[temp[0]] = {}
                data_dict[temp[0]]['area'] = []
                data_dict[temp[0]]['ratio'] = []

            data_dict[temp[0]]['area'].append(area)
            data_dict[temp[0]]['ratio'].append(ratio)

    return data_dict

def getSMLGtNumByClass_bysize(data_dict, class_num):
    """
    计算某个类别的小物体、中物体、大物体的个数
    params data_dict: {dict: 3}  3 x {'类别':{’area':[...]}, {'ratio':[...]}}
    params class_num: 类别  0, 1, 2
    return s: 该类别小物体的个数  0 < area <= 32*32
           m: 该类别中物体的个数  32*32 < area <= 96*96
           l: 该类别大物体的个数  area > 96*96
    """
    s, m, l = 0, 0, 0
    for item in data_dict['{}'.format(class_num)]['area']:
        if item * 640 * 640 <= 32 * 32:
            s += 1
        elif item * 640 * 640 <= 96 * 96:
            m += 1
        else:
            l += 1
    return s, m, l

def getSMLGtNumByClass_xiangdui(data_dict, class_num):
    """
    计算某个类别的小物体、中物体、大物体的个数
    params data_dict: {dict: 3}  3 x {'类别':{’area':[...]}, {'ratio':[...]}}
    params class_num: 类别  0, 1, 2
    return s: 该类别小物体的个数  0 < area <= 0.25%
           m: 该类别中物体的个数  0.25% < area <= 2.25%
           l: 该类别大物体的个数  area > 2.25%
    """
    s, m, l = 0, 0, 0
    # 图片的尺寸大小 注意修改!!!
    # h = 480
    # w = 586
    w = 1920
    h = 1080
    for item in data_dict['{}'.format(class_num)]['area']:
        if item * h * w <= h * w * 0.0025:#改这个界限
            s += 1
        elif item * h * w <= h * w * 0.0225:
            m += 1
        else:
            l += 1
    return s, m, l

def plotSMLByClass(sml, c):
    if c == 0:
        txt = 'vehicle'
    elif c == 1:
        txt = 'cycle'
    elif c == 2:
        txt = 'truck'
    elif c == 3:
        txt = 'bus'
    elif c == 4:
        txt = 'van'
    # if c == 0:
    #     txt = 'pedestrian'
    # elif c == 1:
    #     txt = 'people'
    # elif c == 2:
    #     txt = 'bicycle'
    # elif c == 3:
    #     txt = 'car'
    # elif c == 4:
    #     txt = 'van'
    # elif c == 5:
    #     txt = 'truck'
    # elif c == 6:
    #     txt = 'tricycle'
    # elif c == 7:
    #     txt = 'awning-tricycle'
    # elif c == 8:
    #     txt = 'bus'
    # elif c == 9:
    #     txt = 'motor'
    x = ['S:[0, 32x32]', 'M:[32x32, 96x96]', 'L:[96*96, 640x640]']
    fig = plt.figure(figsize=(10, 8))  # 画布大小和像素密度
    plt.bar(x, sml, width=0.5, align="center", color=['skyblue', 'orange', 'green'])
    for a, b, i in zip(x, sml, range(len(x))):  # zip 函数
        plt.text(a, b + 0.01, "%d" % int(sml[i]), ha='center', fontsize=15, color="r")  # plt.text 函数
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.xlabel('gt大小', fontsize=16)
    plt.ylabel('数量', fontsize=16)
    plt.title('广佛手{}小、中、大GT分布情况(640x640)'.format(txt), fontsize=16)
    plt.show()
    # 保存到本地
    # plt.savefig("")



if __name__ == '__main__':
    labeldir = r'F:\RAIVD_Self\labels\train/'#改这个路径
    data_dict = getGtAreaAndRatio(labeldir)
    # 2、数据集某个类别小中大GT分布情况

    # "holothurian",
    # "echinus",
    # "scallop",
    # "starfish",
    # 0: 白粉病 powdery_mildew
    # 1: 潜叶蛾 leaf_miner
    # 2: 炭疽病 anthracnose
    c = 4  #改这个类别
    sml = getSMLGtNumByClass_xiangdui(data_dict, c)
    plotSMLByClass(sml, c)

