import os
import re
import glob
import shutil
from tqdm import tqdm

IMAGE_DIR = "E:/projects/train_data"
DESTINATION_DIR = "E:/projects/train_data2"
assert os.path.exists(IMAGE_DIR), "源图片文件目录不存在"

if not os.path.exists(DESTINATION_DIR):
    os.makedirs(DESTINATION_DIR)
xml_files = glob.glob(os.path.join(IMAGE_DIR, "exp[0-9]*/*.xml"))

index = []
image_files = []
for i in range(len(xml_files)):
    image_file = xml_files[i].split(".")[0]+'.jpg'
    if not os.path.exists(image_file):
        index.append(i)
        continue
    image_files.append(image_file)
xml_files = [xml_files[i] for i in range(len(xml_files)) if i not in index]
# image_files = [xml_file.split(".")[0]+'.jpg' for xml_file in xml_files]
assert len(xml_files) == len(image_files), f"xml文件{len(xml_files)}和jpg图片{len(image_files)},列表文件长度不一致"
print(f"xml类型的数据一共有{len(xml_files)}个,jpg一共有{len(image_files)}个")

n = len(image_files)
for i in tqdm(range(n),desc="正在复制",total=n,unit="file"):
    copy_dir = os.path.join(DESTINATION_DIR, xml_files[i].split("\\")[-2])
    if not os.path.exists(copy_dir):
        os.makedirs(copy_dir)
    shutil.copy2(xml_files[i], os.path.join(copy_dir, xml_files[i].split("\\")[-1]))
    shutil.copy2(image_files[i], os.path.join(copy_dir, image_files[i].split("\\")[-1]))

xml_num = len(glob.glob(os.path.join(DESTINATION_DIR, "exp[0-9]*/*.xml")))
jpg_num = len(glob.glob(os.path.join(DESTINATION_DIR, "exp[0-9]*/*.jpg")))
print(f"移动后文件夹内的xml文件有{xml_num}个,jpg文件有{jpg_num}个")

