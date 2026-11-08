import sys
import os
##
from shutil import copy
#sys.argv[1]-project_dir
#2-dir_name
dir_name = sys.argv[2]
PROJECT_DIR = sys.argv[1]

TXT_DIR = PROJECT_DIR + "\\MonoBehaviour\\" + dir_name
JSON_DIR = PROJECT_DIR + "\\Json\\" + dir_name
EX_DIR = PROJECT_DIR + "\\Json_Collected\\" + dir_name
if not os.path.isdir(EX_DIR + "\\"):
    os.makedirs(EX_DIR)
files = os.listdir(TXT_DIR)

success = 0
count = 0
for file in files:
    if not file[-4:] == ".txt":#筛选格式
        continue
    file = file[:-4]
    pos = file.find("-")
    if pos == -1:
        continue
    file_num = file[:pos]
    source = JSON_DIR + "\\unnamed asset-" + dir_name + "-" + file_num + ".json"
    dest = EX_DIR + "\\" + file + ".json"
    if os.path.isfile(source):
        copy(source,dest)
        #print(source + " -> " + dest)
        success += 1
    else:
        with open('Temp\\notfound.tmp', 'a', encoding='utf-8') as f:
            f.write(dest + "\n")
    count += 1
print('复制完成.应复制' + str(count) + '个文件.')
if success == count:
    print('所有文件全部成功复制.')
else:
    print(str(success) + "/" + str(count) + ".缺少文件.丢失的文件为.")
    with open('Temp\\notfound.tmp', encoding='utf-8') as f:
        content = f.read()
    print(content)
    os.remove('Temp\\notfound.tmp')