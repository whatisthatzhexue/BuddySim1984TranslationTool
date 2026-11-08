import sys
import os
##
from shutil import copy
#sys.argv[1]-project_dir
#2-dir_name
dir_name = sys.argv[2]
PROJECT_DIR = sys.argv[1]

def filterr(PROJECT_DIR, dir_name):
    ALL_DIR = PROJECT_DIR + "\\MonoBehaviour_All\\" + dir_name
    EX_DIR = PROJECT_DIR + "\\MonoBehaviour\\" + dir_name

    if not os.path.isdir(EX_DIR + "\\"):
        os.makedirs(EX_DIR)
    previous = 0
    files = os.listdir(ALL_DIR)
    previous = len(files)
    print("即将对" + ALL_DIR + "\\进行过滤.当前文件数" + str(previous) + ".")

    #提前获取banlist
    with open('PythonExpansion\\Documents\\Banlist.txt', encoding='utf-8') as f:
        banlist = f.read().split('\n')
    #textsign
    with open('PythonExpansion\\Documents\\Textsign.txt', encoding='utf-8') as f:
        textsign = f.read().split('\n')
    for i in range(len(textsign)):
        text = textsign[i]
        textsign[i] = text[:text.find('=')]

    count = 0
    for file in files:
        count += 1
        #检查
        success = False
        fname = ALL_DIR + "\\" + file
        with open(fname, encoding='utf-8') as f:
            content = f.read().split('\n')
        for c in content:
            c = c.replace('\t','')
            c = c.split(' = ')
            if len(c) < 2:
                continue
            if c[0] in textsign:
                text = c[1][1:-1]
                text = text.split(' ')
                #
                for t in text:
                    if t == '':
                        text.remove(t)
                        continue
                if len(text) == 0:
                    continue
                if not text[0].lower() in banlist:
                    success = True
                    break
        if success:
            print('进度' + str(count) + "/" + str(previous) + "." + os.path.basename(fname) + '通过检查.')
            src = ALL_DIR + "\\" + file
            dst = EX_DIR + "\\" + file
            copy(src, dst)
        else:
            print('进度' + str(count) + "/" + str(previous) + "." + os.path.basename(fname) + '未通过.')
    count = len(os.listdir(EX_DIR))
    print('过滤完成.得到文件数' + str(count) + '.先前为' + str(previous) + ".")
    if count == 0:
        print('已清除空文件夹.')
        os.rmdir(EX_DIR + "\\")

#全选模式
ALL_MODE = "0"
if len(sys.argv) == 4: ALL_MODE = sys.argv[3].replace(" ","")

if ALL_MODE == "1":
    ALL_DIR = PROJECT_DIR + "\\MonoBehaviour_All\\"
    folders = os.listdir(ALL_DIR)
    for folder in folders:
        if os.path.isfile(ALL_DIR + folder):
            continue
        filterr(PROJECT_DIR, folder)
    sys.exit()
filterr(PROJECT_DIR, dir_name)