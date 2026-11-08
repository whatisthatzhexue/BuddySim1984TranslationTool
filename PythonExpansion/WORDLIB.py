import sys
import os
#sys.argv[1]-project_dir
#2-dir_name
dir_name = sys.argv[2]
PROJECT_DIR = sys.argv[1]
#
from hashlib import md5

WORK_DIR = PROJECT_DIR + '\\Workspace\\'
LIB_DIR = PROJECT_DIR + '\\WordLib\\'
print('文本翻译文件转换/记录文件中...')
with open(WORK_DIR + dir_name + '文本翻译.txt', encoding='utf-8') as f:
    content = f.read().split('\n')
LOCK = False
allfiles = []
for c in content:
    m = c.split(':')
    if m[0] == '当前文件':
        LOCK = False
        editingfile = m[1]
        continue
    if m[0] == '备注':
        continue
    with open('Temp\\text_' + os.path.basename(editingfile) + '.tmp', 'a', encoding='utf-8') as f:
        f.write(c.replace('\t','') + '\n')
    if not LOCK:
        LOCK = True
        allfiles.append(editingfile)

print('文本文件转换中...')
with open(WORK_DIR + dir_name + '文本.txt', encoding='utf-8') as f:
    content = f.read().split('\n')
for c in content:
    m = c.split(':')
    if m[0] == '当前文件':
        editingfile = m[1]
        continue
    if m[0] == '备注':
        continue
    with open('Temp\\texten_' + os.path.basename(editingfile) + '.tmp', 'a', encoding='utf-8') as f:
        f.write(c.replace('\t','') + '\n')

print('文本§文本翻译结合中...')
for fname in allfiles:
    fname = os.path.basename(fname)
    texfile = "Temp\\text_" + fname + ".tmp"
    numfile = "Temp\\texten_" + fname + ".tmp"
    with open(texfile, encoding="utf-8") as f:
        content = f.read().split("\n")
    with open(numfile, encoding="utf-8") as f:
        content2 = f.read().split("\n")
    if not len(content) == len(content2):
        print(texfile + '读取失败.')
        print('CH:')
        for c in content:
            print(c)
        print('EN:')
        for c in content2:
            print(c)
        continue
    with open("Temp\\raw_" + os.path.basename(fname) + ".tmp", "w", encoding="utf-8") as f:
        for i in range(len(content) - 1):
            f.write(content2[i] + "§" + content[i] + "\n")
    os.remove(texfile)
    os.remove(numfile)
    #print("已完成结合:" + os.path.basename(fname))

if not os.path.isdir(LIB_DIR):
    os.makedirs(LIB_DIR)

print('最终文件转换为词库中...')
for fname in allfiles:
    fname = os.path.basename(fname)
    rawfile = "Temp\\raw_" + fname + ".tmp"
    if not os.path.isfile(rawfile):
        continue
    with open(rawfile, encoding='utf-8') as f:
        content = f.read().split('\n')
    for c in content:
        c = c.split('§')
        if len(c) < 2: continue
        if c[0] == c[1]:
            continue
        with open('Temp\\TEXT.tmp', 'w', encoding='utf-8') as g:
            g.write(c[0] + '\n')
        with open('Temp\\TEXT.tmp', 'rb') as g:
            md5_ = md5(g.read()).hexdigest()
        NEW = LIB_DIR + md5_
        if os.path.isfile(NEW):
            continue
        with open(NEW, 'w', encoding='utf-8') as g:
            g.write(c[1] + '\n')
        #print(c[0] + '翻译到' + c[1] + '.储存于文件' + NEW + '.')

files = os.listdir("Temp\\")
for i in files:
    i = "Temp\\" + i
    if os.path.isfile(i):
        os.remove(i)
print('词库更新完毕.')