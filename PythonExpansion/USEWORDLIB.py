import sys
import os
#sys.argv[1]-project_dir
#2-dir_name
dir_name = sys.argv[2]
PROJECT_DIR = sys.argv[1]

#
from hashlib import md5

LIB_DIR = PROJECT_DIR + "\\WordLib\\"
WORK_DIR = PROJECT_DIR + "\\Workspace\\"
if not os.path.isdir(LIB_DIR):
    print('错误.词库不存在.')
    sys.exit()
c = 0
files = os.listdir(WORK_DIR)
i = 0
while i < len(files):
    if (not files[i][:len(dir_name)] == dir_name) or (not os.path.isfile(WORK_DIR + files[i])):
        del files[i]
        i -= 1
    i += 1
for file in files:
    print(file)

file_ = ""
if len(sys.argv) > 3: file_ = sys.argv[3] + '.txt'
if i > 1:
    while True:
        if file_ == "":
            file_ = input("请输入要加载的文件名(不含后缀):") + '.txt'
        if not file_ in files:
            print(file_ + "不是选项之一")
            file_ = ""
            continue
        break
else:
    if i == 0:
        print('错误.找不到文件.')
        sys.exit()
    file_ = files[0]

fname = file_[:-4]
old = WORK_DIR + file_
new = WORK_DIR + fname + '_Translated.txt'
if not os.path.isfile(WORK_DIR + dir_name + '文本翻译.txt'):
    new = WORK_DIR + dir_name + '文本翻译.txt'

SPECIAL = ['备注', '当前文件']
print('正在使用词库翻译' + dir_name + '...')
with open(old, encoding='utf-8') as f:
    content = f.read().split('\n')
TOTAL = ''
for c in content:
    if c.split(':')[0] in SPECIAL:
        TOTAL += c + '\n'
        continue
    with open('Temp\\TEXT.tmp', 'w', encoding='utf-8') as g:
        g.write(c.replace('\t','') + '\n')
    with open('Temp\\TEXT.tmp', 'rb') as g:
        md5_ = md5(g.read()).hexdigest()
    NEW_LIB = LIB_DIR + md5_
    if os.path.isfile(NEW_LIB):
        with open(NEW_LIB, encoding='utf-8') as g:
            c = g.read()
            if c.find('"') == -1:#无转义符
                TOTAL += '\t'
            c = c[:-1]
    TOTAL += c + '\n'
with open(new, 'w', encoding='utf-8') as f:
    f.write(TOTAL[:-1])

print('已翻译为' + new + '文件.')
os.remove('Temp\\TEXT.tmp')