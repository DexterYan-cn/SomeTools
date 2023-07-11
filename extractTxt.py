# 从指定文件夹中提取txt文件中指定名字的文件到另一个目录


# 导入需要使用的python包
import shutil
import os

# 根据txt文件中存储的文件名，提取对应的文件保存到另一个文件夹

data = []

# 读取存储val.txt文件
# for line in open(r"F:/Visdrone2019Yolo/images/img_20001500/train.txt", "r"):  # 设置文件对象并读取每一行文件
for line in open(r"F:/AI_TOD_Yolo/images/val.txt", "r"):  # 设置文件对象并读取每一行文件
    data.append(line)

# 我的数据是jpg格式，如果你的数据是其他格式，则将下面代码中的jpg替换即可
for a in data:
    # src是总文件夹
    # src = r'F:/Visdrone2019Yolo/labels/train/{}.txt'.format(a[:-1])
    src = r'F:/AI_TOD_Yolo/labels/val/{}.txt'.format(a[:-1])

    # dst是保存提取结果的文件夹
    dst = r'F:/AI_TOD_Yolo/labels/txtval/{}.txt'.format(a[:-1])
    os.makedirs(os.path.dirname(dst),exist_ok=True)
    shutil.move(src, dst)