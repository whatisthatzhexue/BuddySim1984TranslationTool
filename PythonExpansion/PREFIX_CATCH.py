import sys
import os
#sys.argv[1]-project_dir
#2-dir_name
PROJECT_DIR = sys.argv[1]

ALL_DIR = PROJECT_DIR + "\\MonoBehaviour_All\\"

def check(fname):
    global textsign
    global sample
    #检查
    success = False
    with open(fname, encoding='utf-8') as f:
        content = f.read().split('\n')
    for c in content:
        c = c.replace('\t','')
        c = c.split(' = ')
        if not c[0].split(' ')[0] == 'string':
            continue
        if not c[0] in textsign:
            text = c[1][1:-1]
            if text == '':
                continue
            textsign.append(c[0])
            sample.append(text)
            break
textsign = []
sample = []
folders = os.listdir(ALL_DIR)
for folder in folders:
    folder = ALL_DIR + folder
    if os.path.isdir(folder):
        files = os.listdir(folder)
        print(folder)
        for file in files:
            check(folder + "\\" + file)
    else:
        check(folder)

for i in range(len(textsign)):
    print(textsign[i] + "=" + sample[i])

with open("PythonExpansion\\Documents\\Textsign_catch.txt", "w", encoding="utf-8") as f:
    for i in range(len(textsign)):
        f.write(textsign[i] + "=" + sample[i])
        f.write('\n')