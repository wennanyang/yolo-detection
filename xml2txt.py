# -*- coding: utf-8 -*-
import os
import xml.etree.ElementTree as ET
import glob
from tqdm import tqdm
DIR_PATH = r'E:/projects/train_data'  # 原来存放xml文件的目录 # 修改label后形成的txt目录


dict_info = {'goods': 0, 'head': 1}  # 有几个 类别 填写几个label names


def get_xml_files(path):
    xml_files = glob.glob(os.path.join(path, "*.xml"))
    return xml_files

def get_dirs(path):
    dirs = []
    for dir_name in os.listdir(DIR_PATH):
        dirs.append(os.path.join(path, dir_name))
    return dirs
def xml2txt(xml_files):
    xml_num = len(xml_files)
    for i in tqdm(range(xml_num), total= xml_num, desc="正在转换", unit="file"):
        root = ET.parse(xml_files[i]).getroot()
        width, height = float(root.find("size")[0].text), float(root.find("size")[1].text)
        filename = root.find('filename').text
        for child in root.findall('object'):
            sub = child.find('bndbox')
            label = child.find('name').text
            label_ = dict_info.get(label)
            if label_:
                label_ = label_
            else:
                label_ = 0
            xmin = float(sub[0].text)
            ymin = float(sub[1].text)
            xmax = float(sub[2].text)
            ymax = float(sub[3].text)
            try:  # 转换成yolov3的标签格式，需要归一化到（0-1）的范围内
                x_center = f"{(xmin + xmax) / (2 * width) :.6f}"
                #print(x_center)
                # x_center = '%.6f' % x_center
                y_center = f"{(ymin + ymax) / (2 * height) :.6f}"
                # y_center = '%.6f' % y_center
                w = f"{(xmax - xmin) / width :.6f}"
                # w = '%.6f' % w
                h = f"{(ymax - ymin) / height :.6f}"
                # h = '%.6f' % h
            except ZeroDivisionError:
                print(f"{filename}的 width为0")
            with open(os.path.join(xml_files[i].split('.xml')[0] + '.txt'), 'a+') as f:
                f.write(' '.join([str(label_), x_center, y_center, w, h + '\n']))

# dirs = get_dirs(DIR_PATH)
# print(f"图片文件夹总共有{len(dirs)}个")
# xml_files = get_xml_files(dirs[0])
# xml_num = len(xml_files)
# print(f"xml文件总共有{xml_num}个")
# xml2txt(xml_files=xml_files)
                
print(glob.glob(os.path.join(DIR_PATH, "exp[0-9]*/*.xml")))






# for path in os.listdir(DIR_PATH):
#   print(path)
#   for fp in os.listdir(os.path.join(dirpath, path)):
#     print(fp)
#     newdir = os.path.join(dirpath, path)
#     if fp.endswith('.xml'):
#         #print(fp)
#         root = ET.parse(os.path.join(dirpath, path, fp)).getroot()
#         xmin, ymin, xmax, ymax = 0, 0, 0, 0
#         sz = root.find('size') 
#         width = float(sz[0].text)
#         height = float(sz[1].text)
#         filename = root.find('filename').text
#         for child in root.findall('object'):  # 找到图片中的所有框
#             sub = child.find('bndbox')  # 找到框的标注值并进行读取
#             label = child.find('name').text
#             label_ = dict_info.get(label)
#             if label_:
#                 label_ = label_
#             else:
#                 label_ = 0
#             xmin = float(sub[0].text)
#             ymin = float(sub[1].text)
#             xmax = float(sub[2].text)
#             ymax = float(sub[3].text)
#             try:  # 转换成yolov3的标签格式，需要归一化到（0-1）的范围内
#                 x_center = (xmin + xmax) / (2 * width)
#                 #print(x_center)
#                 x_center = '%.6f' % x_center
#                 y_center = (ymin + ymax) / (2 * height)
#                 y_center = '%.6f' % y_center
#                 w = (xmax - xmin) / width
#                 w = '%.6f' % w
#                 h = (ymax - ymin) / height
#                 h = '%.6f' % h
#             except ZeroDivisionError:
#                 print(filename, '的 width有问题')
#             with open(os.path.join(newdir, fp.split('.xml')[0] + '.txt'), 'a+') as f:
#                 f.write(' '.join([str(label_), str(x_center), str(y_center), str(w),str(h) + '\n']))
# print('ok')

