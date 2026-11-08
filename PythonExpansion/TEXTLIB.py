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
if not os.path.isdir(LIB_DIR):
    os.makedirs(LIB_DIR)
files = os.listdir(MESH_DIR)
for file in files:
    file_path = MESH_DIR + '\\' + file
    if not file[-4:] == ".txt":
        continue
    with open(file_path, encoding='utf-8') as f:
        content = f.read().split('\n')
    for c in content:
        list_ = c.split(' ')
        for e in list_:
            if e == '':
                list_.remove(e)
        if len(list_) < 3: continue
        if not list_[2] == 'm_Text':
            continue
        with open('Temp\\TEXT.tmp', 'w', encoding='utf-8') as g:
            g.write(c + '\n')
        with open('Temp\\TEXT.tmp', 'rb') as g:
            md5_ = md5(g.read()).hexdigest()
        NEW = LIB_DIR + md5_
        if os.path.isfile(NEW): continue
        with open(NEW, 'w', encoding='utf-8') as f:
            f.write(c + '\n')
        print(c + '已存储.地址.' + md5_)
        with open(PROJECT_DIR + '\\TextMesh\\地址.txt', 'a', encoding='utf-8') as f:
            f.write(md5_ + '\n')
            f.write(c + '\n')
if os.path.isfile('Temp\\TEXT.tmp'):
    os.remove('Temp\\TEXT.tmp')