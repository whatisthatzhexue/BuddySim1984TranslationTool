import sys
import os
#sys.argv[1]-project_dir
#2-dir_name
dir_name = sys.argv[2]
PROJECT_DIR = sys.argv[1]
#
from hashlib import md5

LIB_DIR = PROJECT_DIR + '\\TextLib\\'
MESH_DIR = PROJECT_DIR + '\\TextMesh\\' + dir_name
T_DIR = PROJECT_DIR + '\\TextMesh\\Translated\\' + dir_name + '_T\\'
if not os.path.isdir(LIB_DIR):
    print('错误.text库不存在.')
    sys.exit()
if not os.path.isdir(T_DIR):
    os.makedirs(T_DIR)

print('正在使用text库翻译' + dir_name + '...')
files = os.listdir(MESH_DIR)
for file in files:
    file_path = MESH_DIR + '\\' + file
    if not file[-4:] == ".txt":
        continue
    TOTAL = ''
    NEED = False
    with open(file_path, encoding='utf-8') as f:
        content = f.read().split('\n')
    for c in content:
        list_ = c.split(' ')
        for e in list_:
            if e == '':
                list_.remove(e)
        if len(list_) < 3:
            TOTAL += c + '\n'
            continue
        if not list_[2] == 'm_Text':
            TOTAL += c + '\n'
            continue
        with open('Temp\\TEXT.tmp', 'w', encoding='utf-8') as g:
            g.write(c + '\n')
        with open('Temp\\TEXT.tmp', 'rb') as g:
            md5_ = md5(g.read()).hexdigest()
        NEW = LIB_DIR + md5_
        if os.path.isfile(NEW):
            with open(NEW, encoding='utf-8') as f:
                d = f.read()[:-1]
            if not c == d:
                NEED = True
                c = d
        TOTAL += c + '\n'
        
    if not NEED: continue
    NEWFILE = T_DIR + file
    with open(NEWFILE, 'w', encoding='utf-8') as f:
        f.write(TOTAL)
    print('完成翻译:' + NEWFILE)
if os.path.isfile('Temp\\TEXT.tmp'):
    os.remove('Temp\\TEXT.tmp')