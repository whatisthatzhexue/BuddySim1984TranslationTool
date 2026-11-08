import sys
import os
#sys.argv[1]-project_dir
#2-dir_name
dir_name = sys.argv[2]
PROJECT_DIR = sys.argv[1]

JC_DIR = PROJECT_DIR + "\\Json_Collected\\" + dir_name + "\\"
WORKSPACE_DIR = PROJECT_DIR + "\\Workspace\\"
files = os.listdir(JC_DIR)
for file in files:
    if not file[-5:] == '.json':
        files.remove(file)
print('共',end='')
print(len(files),end='')
print('个json文件')

#提前获取banlist
with open('PythonExpansion\\Documents\\Banlist.txt', encoding='utf-8') as f:
    banlist = f.read().split('\n')
#textsign
with open('PythonExpansion\\Documents\\Textsign.txt', encoding='utf-8') as f:
    textsign = f.read().split('\n')
for i in range(len(textsign)):
    text = textsign[i]
    textsign[i] = '1 ' + text[:text.find('=')]

print('正在输出' + dir_name + '文本.txt...')
ban = False
buddy = False
with open(WORKSPACE_DIR + dir_name + '文本.txt', 'w', encoding='utf-8') as fi:
    for file in files:
        file_path = JC_DIR + file
        fi.write('当前文件:' + file_path + '\n')
        with open(file_path, encoding='utf-8') as f:
            content = f.read().split('\n')
        for c in content:
            if c.find('\\') != -1:
                fi.write(c + '\n')
                continue
            c = c.split('"')
            if len(c) < 3: continue
            if c[1] == '1 UInt8 isBuddy':
                if not ban:
                    if buddy:
                        if c[2] == ': 0,':
                            fi.write('备注:	已经检测不到Buddy消息\n')
                            buddy = False
                elif buddy == False:
                    if c[2] == ': 1,':
                        fi.write('备注:	已经检测到Buddy消息\n')
                        buddy = True
                continue
            if len(c) < 4: continue
            text = c[3]
            if c[1] in textsign:
                ban = False
                list_ = text.split(' ')
                for l in list_:
                    if l == '':
                        list_.remove(l)
                if len(list_) == 0:
                    continue
                list_[0] = list_[0].lower()
                ban = list_[0] in banlist
                if ban: continue
                fi.write('\t' + text + '\n')
                continue
            if c[1] == '1 string id':
                fi.write('备注:' + text + '\n')
                continue
            if c[1] == '1 string otherObjectName':
                fi.write('备注:物体名:' + text + '\n')
                continue
        buddy = False

if not os.path.isdir(WORKSPACE_DIR + '行数\\'):
    os.makedirs(WORKSPACE_DIR + '行数')
print('正在输出行数文件...')
ban = False
with open(WORKSPACE_DIR + '行数\\' + dir_name, 'w', encoding='utf-8') as fi:
    for file in files:
        file_path = JC_DIR + file
        fi.write('当前文件:' + file_path + '\n')
        with open(file_path, encoding='utf-8') as f:
            content = f.read().split('\n')
        line = 0
        for c in content:
            line += 3
            if c.find('\\') != -1:
                fi.write('\t' + str(line) + '\n')
                continue
            c = c.split('"')
            if len(c) < 2: continue
            if c[1] in textsign:
                if len(c) < 4: continue
                text = c[3]
                ban = False
                list_ = text.split(' ')
                for l in list_:
                    if l == '':
                        list_.remove(l)
                if len(list_) == 0:
                    continue
                list_[0] = list_[0].lower()
                ban = list_[0] in banlist
                if ban: continue
                fi.write('\t' + str(line) + '\n')
                continue

print('完成.')