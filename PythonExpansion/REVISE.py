import sys
import os
#sys.argv[1]-project_dir
#2-dir_name
dir_name = sys.argv[2]
PROJECT_DIR = sys.argv[1]

#
from hashlib import md5

"""
若没有文件记录，开始生成[文本][文本翻译,用作参考][文本翻译-baidu]
逻辑如下：
检测文本baidu，如果“都”有文本翻译与之对应，将该文本剔除，
反之，将以以下形式呈现“一个文件”：
---文件*---
*全文(英文)
*全文(翻译)
-----
原文:(必须和文本翻译不同)
Baidu:
修订:(不输入，直接回车，视为放弃修订)
-----
...
修订内容:

每次修订结束，跟进修订记录

...

修订文件生成完成.
"""

def GenerateFiles(src, dst):
    global dir_name
    Files = [
    src + dir_name + '文本.txt',
    src + dir_name + '文本翻译.txt',
    src + dir_name + '文本翻译_baidu.txt',
    ]
    #建夹
    for num in range(len(Files)):
        NEW = dst + str(num)
        if not os.path.isdir(NEW):
            os.makedirs(NEW)
    #生成
    for num in range(len(Files)):
        with open(Files[num], encoding='utf-8') as f:
            content = f.read().split('\n')
        for c in content:
            m = c.split(':')
            if m[0] == '当前文件':
                editingfile = m[1]
                continue
            if m[0] == '备注':
                continue
            NEW = dst + str(num) + '\\' + os.path.basename(editingfile) + '.tmp'
            with open(NEW, 'a', encoding='utf-8') as f:
                f.write(c.replace('\t','') + '\n')
    #剔除
    #思路:先0和1比较，删除1中和0重复的部分
    #再1和2比较，删除2中和1重复的部分，以及0中的相同部分
    #删除1
    Files = os.listdir(dst + '0\\')
    T_DIR = dst + '1\\'
    for fname in Files:
        file = dst + '0\\' + fname
        fileb = T_DIR + fname
        if not os.path.isfile(fileb):
            continue
        with open(file, encoding='utf-8') as f:
            content = f.read()
        with open(fileb, encoding='utf-8') as f:
            content1 = f.read()
        if content == content1:
            #os.remove(file)
            os.remove(fileb)
            #filec = dst + '2\\' + fname
            #if os.path.isfile(filec):
            #    os.remove(filec)
    Files = os.listdir(dst + '1\\')
    T_DIR = dst + '2\\'
    for fname in Files:
        file = dst + '1\\' + fname
        fileb = T_DIR + fname
        if not os.path.isfile(fileb):
            continue
        with open(file, encoding='utf-8') as f:
            content = f.read()
        with open(fileb, encoding='utf-8') as f:
            content1 = f.read()
        if content == content1:
            os.remove(file)
            os.remove(fileb)
            filec = dst + '0\\' + fname
            if os.path.isfile(filec):
                os.remove(filec)
    #os.rmdir(dst + '1\\')
    #存档
    with open(dst + 'Process.txt', 'w', encoding='utf-8') as f:
        f.write('Editing:0\n')
        f.write('Number:0')

def SaveFiles(folder, src, dst):
    #保存文件
    if not os.path.isdir(folder + 'WordLib\\'):
        os.makedirs(folder + 'WordLib\\')
    with open('Temp\\TEXT.tmp', 'w', encoding='utf-8') as g:
        g.write(src + '\n')
    with open('Temp\\TEXT.tmp', 'rb') as g:
        md5_ = md5(g.read()).hexdigest()
    os.remove('Temp\\TEXT.tmp')
    NEW = folder + 'WordLib\\' + md5_
    with open(NEW, 'w', encoding='utf-8') as g:
        g.write(dst + '\n')
    
def SaveProcess(num1, num2):
    #保存进度
    global PROCESS
    with open(PROCESS, 'w', encoding='utf-8') as g:
        g.write('Editing:' + str(num1) + '\n')
        g.write('Number:' + str(num2))

def GetProcess():
    global PROCESS
    result = [0, 0]
    with open(PROCESS, encoding='utf-8') as f:
            content = f.read().split('\n')
    for c in content:
        c = c.split(':')
        if len(c) < 2: continue
        if c[0] == 'Editing':
            result[0] = int(c[1])
            continue
        if c[0] == 'Number':
            result[1] = int(c[1])
            continue
    return result
   
def GetLib(folder, src):
    #保存文件
    if not os.path.isdir(folder + 'WordLib\\'):
        return ''
    with open('Temp\\TEXT.tmp', 'w', encoding='utf-8') as g:
        g.write(src + '\n')
    with open('Temp\\TEXT.tmp', 'rb') as g:
        md5_ = md5(g.read()).hexdigest()
    os.remove('Temp\\TEXT.tmp')
    NEW = folder + 'WordLib\\' + md5_
    if not os.path.isfile(NEW):
        return ''
    with open(NEW, encoding='utf-8') as g:
        content = g.read()
    content = content[:-1]
    return content

def find_n(string, sub, num):
    t = 0
    delta = 0
    index = string.find(sub)
    while index != -1:
        t += 1
        if t >= num: break
        delta += (index + 1)
        string = string[(index + 1):]
        index = string.find(sub)
    return (index + delta)

WORK_DIR = PROJECT_DIR + '\\Workspace\\'
RE_DIR = 'PythonExpansion\\Documents\\Revision\\' + dir_name + '\\'
LIB_DIR = 'PythonExpansion\\Documents\\'

PROCESS = RE_DIR + 'Process.txt'
if not os.path.isfile(PROCESS):
    print('首次进行' + dir_name + '修订活动。正在生成文件中...')
    os.makedirs(RE_DIR)
    GenerateFiles(WORK_DIR, RE_DIR)
#以下是读取文件
print('文件' + dir_name + '已找到。')
INPUT = ''
Editing = 0
Number = 0
PATH_0 = RE_DIR + '0\\'
PATH_1 = RE_DIR + '1\\'
PATH_2 = RE_DIR + '2\\'
Files = os.listdir(PATH_0)
#决定
while True:
    num1, num2 = GetProcess()
    print('---上次进度---')
    print('文件:', num1, ':', Files[num1])
    print('行数:', num2)
    INPUT = input('继续上次进度吗？(Y/N)')
    if len(INPUT) == 0:
        continue
    if INPUT[0].lower() == 'n':
        for i in range(len(Files)):
            print(i, ':', Files[i])
        num1 = input('请输入想打开的文件:')
        num2 = input('请输入想打开的行:')
        SaveProcess(num1, num2)
        print('进度已保存。输入Y以开始编辑。')
        continue
    if INPUT[0].lower() == 'y':
        Editing, Number = GetProcess()
        break
#编辑器
for i in range(Editing, len(Files)):
    fname = Files[i]
    print('--第' + str(i + 1) + '/' + str(len(Files)) + '号文件--')
    print('---' + fname + '---')
    with open(PATH_0 + fname, encoding='utf-8') as f:
        content0 = f.read().split('\n')
    if os.path.isfile(PATH_1 + fname):
        with open(PATH_1 + fname, encoding='utf-8') as f:
            content1 = f.read().split('\n')
    else:
        content1 = []
    with open(PATH_2 + fname, encoding='utf-8') as f:
        content2 = f.read().split('\n')
    print('**原文')
    print('**百度翻译')
    for c in range(len(content0)):
        if content0[c] == '': continue
        print(content0[c])
        if content0[c] == content2[c]: continue
        print(content2[c])
        print('')
    print('-----')
    for c in range(Number, len(content0)):
        if content0[c] == '': continue
        SLASH = [False, '', '', '']
        if (content0[c].find('\\') != -1):
            #待完成
            STR = content0[c]
            CODE = STR.replace('\\"', '00')
            INDEX1 = (find_n(STR, '"', 3) + 1)    #寻找第三个"的位置and +1
            INDEX2 = STR.rfind('"')               #最后一个"
            SLASH = [True, STR[:INDEX1], STR[INDEX1:INDEX2], STR[INDEX2:]]
            del STR
            del CODE
            del INDEX1
            del INDEX2
            print('原文:' + SLASH[2])
        else:
            print('原文:' + content0[c])
        DEFAULT = content0[c]
        if (len(content1) > 0) and (not content0[c] == content1[c]):
            print('翻译:' + content1[c])
            DEFAULT = content1[c]
        elif not content0[c] == content2[c]:
            print('Baidu:' + content2[c])
            DEFAULT = content2[c]
        SaveProcess(i, c) #保存进度
        #如果已有wordlib
        Lib = GetLib(LIB_DIR, content0[c])
        if Lib == '':
            REVISE = input('>') #检测输入
            if SLASH[0]:
                REVISE = (SLASH[1] + REVISE + SLASH[3])
        else:
            REVISE = Lib
        print('-----')
        #输入判定
        if REVISE == '':
            REVISE = DEFAULT
        #更新wordlib
        SaveFiles(LIB_DIR, content0[c], REVISE)
        print('修订内容:' + REVISE)
        print('-----')
    Number = 0