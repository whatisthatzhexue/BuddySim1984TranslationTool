import sys
import os
#sys.argv[1]-project_dir
#2-dir_name
#dir_name = sys.argv[2]
PROJECT_DIR = sys.argv[1]

print('若要停止coding，请输入单个句号"."')
print('指令格式:<指令>(<参数>)')
print('若要一行输入多个指令，请以";"分割')
#储存
COMMAND_LIST = []
while True:
    new = input('>>')
    if new == '.':
        break
    COMMAND_LIST.append(new)

#分析与执行(按照指令格式)
for CMD in COMMAND_LIST:
    CMD = CMD.split(';')
    for C in CMD:
        i1 = C.find('(')
        i2 = C.rfind(')')
        if (i1 == -1 or i2 == -1):
           print('指令无法识别:' + C)
           continue
        Args = C[(i1 + 1):i2]
        Args = Args.split(',')
        C = C[:i1]
        C = C.replace(' ','')
        CMDSTR = 'python PythonExpansion\\' + C + '.py "' + PROJECT_DIR + '"'
        for Arg in Args:
            CMDSTR += ' "' + Arg + '"'
        os.system(CMDSTR)