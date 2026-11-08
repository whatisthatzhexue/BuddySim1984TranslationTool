import sys
import os
##
from shutil import copy
#sys.argv[1]-project_dir
#2-dir_name
dir_name = sys.argv[2]
PROJECT_DIR = sys.argv[1]

INPUT = ""
if len(sys.argv) == 4: INPUT = sys.argv[3]
FOLDER = ""
while True:
    if INPUT == "":
        INPUT = input("请选择一个文件夹:1.Workspace 2.Json_Collected")
    INPUT = INPUT.replace(" ", "")
    if INPUT == "1":
        FOLDER = "Workspace"
        break
    if INPUT == "2":
        FOLDER = "Json_Collected"
        break
    print("无效的输入'" + INPUT + "'.")
    INPUT = ""
EX_DIR = PROJECT_DIR + "\\" + FOLDER + "\\" + dir_name

EX_DIR1_BASE = PROJECT_DIR + "\\Renamed\\" + dir_name + "_renamed"
EX_DIR1 = EX_DIR1_BASE
file_num = 0
while os.path.isdir(EX_DIR1 + "\\"):
    file_num += 1
    EX_DIR1 = EX_DIR1_BASE + "(" + str(file_num) + ")"
os.makedirs(EX_DIR1)
files = os.listdir(EX_DIR)

success = 0
count = 0
for file in files:
    if not file[-5:] == ".json":#筛选格式
        continue
    file = file[:-5]
    pos = file.find("-")
    if pos == -1:
        continue
    file_num = file[:pos]
    source = EX_DIR + "\\" + file + ".json"
    dest = EX_DIR1 + "\\unnamed asset-" + dir_name + "-" + file_num + ".json"
    if os.path.isfile(source):
        copy(source,dest)
        print(source + " -> " + dest)
        success += 1
    else:
        with open('Temp\\notfound.tmp', 'a', encoding='utf-8') as f:
            f.write(dest + "\n")
    count += 1
print('复制完成.应复制' + str(count) + '个文件.')
if success == count:
    print('所有文件全部成功复制.')
    print('生成到文件夹' + EX_DIR1 + "\\")
else:
    print(str(success) + "/" + str(count) + ".缺少文件.丢失的文件为.")
    with open('Temp\\notfound.tmp', encoding='utf-8') as f:
        content = f.read()
    print(content)
    os.remove('Temp\\notfound.tmp')