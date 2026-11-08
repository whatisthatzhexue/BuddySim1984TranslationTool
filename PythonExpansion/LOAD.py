import sys
import os
#sys.argv[1]-project_dir
#2-dir_name
dir_name = sys.argv[2]
PROJECT_DIR = sys.argv[1]

WORKSPACE_DIR = PROJECT_DIR + "\\Workspace\\"
files = os.listdir(WORKSPACE_DIR)
i = 0
while i < len(files):
    if not files[i][:len(dir_name)] == dir_name:
        del files[i]
        i -= 1
    i += 1
for file in files:
    print(file)

file_ = ""
if len(sys.argv) > 3: file_ = sys.argv[3]
while True:
    if file_ == "":
        file_ = input("请输入要加载的文件名(不含后缀):")
    if not os.path.isfile(WORKSPACE_DIR + file_ + ".txt"):
        print(file_ + ".txt不存在")
        file_ = ""
        continue
    break

print("文本文件转换/记录文件中...")
allfiles = []
editingfile = ""
with open(WORKSPACE_DIR + file_ + ".txt", encoding="utf-8") as f:
    content = f.read()
content = content.split("\n")
for c in content:
    cmd = c.split(":")
    if cmd[0] == "当前文件":
        editingfile = cmd[1]
        allfiles.append(cmd[1])
        file = "Temp\\text_" + os.path.basename(cmd[1]) + ".tmp"
        if os.path.isfile(file):
            os.remove(file)
    elif not cmd[0] == "备注":
        c = c.replace("\t","")
        if len(c) != 0:
            #
            #print(c)
            #
            file = "Temp\\text_" + os.path.basename(editingfile) + ".tmp"
            with open(file, "a", encoding="utf-8") as f:
                f.write(c + "\n")

print("行数文件转换中...")
with open(WORKSPACE_DIR + "行数\\" + dir_name, encoding="utf-8") as f:
    content = f.read()
content = content.split("\n")
for c in content:
    cmd = c.split(":")
    if cmd[0] == "当前文件":
        editingfile = cmd[1]
        file = "Temp\\numb_" + os.path.basename(cmd[1]) + ".tmp"
        if os.path.isfile(file):
            os.remove(file)
    else:
        file = "Temp\\numb_" + os.path.basename(editingfile) + ".tmp"
        with open(file, "a", encoding="utf-8") as f:
            f.write(c + "\n")

print("行数§文字结合中...")
for file in allfiles:
    texfile = "Temp\\text_" + os.path.basename(file) + ".tmp"
    numfile = "Temp\\numb_" + os.path.basename(file) + ".tmp"
    if not os.path.isfile(texfile):
        #allfiles.remove(file)
        continue
    with open(texfile, encoding="utf-8") as f:
        content = f.read()
    with open(numfile, encoding="utf-8") as f:
        content2 = f.read()
    content = content.split("\n")
    content2 = content2.split("\n")
    with open("Temp\\raw_" + os.path.basename(file) + ".tmp", "w", encoding="utf-8") as f:
        for i in range(len(content) - 1):
            f.write(content2[i] + "§" + content[i] + "\n")
    os.remove(texfile)
    os.remove(numfile)
    print("已完成结合:" + os.path.basename(file))

if not os.path.isdir(WORKSPACE_DIR + dir_name + "\\"):
    os.makedirs(os.getcwd() + "\\" + WORKSPACE_DIR + dir_name)

print("最终文件转换为json中...")
#就差转换为json了
for i in allfiles:
    file = "Temp\\raw_" + os.path.basename(i) + ".tmp"
    if not os.path.isfile(file):
        print(os.path.basename(i) + "未转换.")
        continue
    notechoed = True
    str_ = os.path.basename(i)
    #提取MAP
    with open(file, encoding="utf-8") as f:
        content = f.read()
    content = content.split('\n')
    MAP = {}
    for c in content:
        if len(c) == 0: continue
        content2 = c.split('§')
        MAP.update({int(content2[0]):content2[1]})
    #使用MAP
    with open(i, encoding="utf-8") as f:
        content = f.read()
    content = content.split('\n')
    with open(WORKSPACE_DIR + dir_name + "\\" + os.path.basename(i), 'w', encoding='utf-8') as f:
        for c in range(len(content)):
            val = (c * 3 + 3)
            if val in MAP:
                if content[c].find('\\') != -1:
                    f.write(MAP[val])
                else:
                    content2 = content[c].split('"')
                    content2[3] = MAP[val]
                    for t in range(len(content2)):
                        f.write(content2[t])
                        if t != len(content2) - 1: f.write('"')
            else:
                f.write(content[c])
            f.write("\n")
    #删除MAP
    del MAP
    #完成
    print("已完成转换:" + os.path.basename(i))

files = os.listdir("Temp\\")
for i in files:
    i = "Temp\\" + i
    if os.path.isfile(i):
        os.remove(i)
"""
echo 最终文件转换为json中...
for /f "delims=" %%a in (Temp\allfiles.tmp) do (
	if exist Temp\raw_%%~na.tmp (
	echo; > Temp\counter.tmp
	echo; > Temp\notechoed.tmp
	set str=%%~na
	(for /f "delims=" %%b in (%%a) do (
		rem 遍历每一个x(numb)y(text)
		if not exist Temp\line.tmp (
			call :getfirstline
			(for /f "skip=1 delims=" %%z in (Temp\raw_%%~na.tmp) do (
				echo %%z
			))>Temp\raw.tmp
			del Temp\raw_%%~na.tmp
			ren Temp\raw.tmp raw_%%~na.tmp
		)
		rem 遍历第一行
		if exist Temp\line.tmp for /f "tokens=1,2 delims=§" %%x in (Temp\line.tmp) do (
			for %%c in (Temp\counter.tmp) do (
				if "%%~zc" == "%%x" (
					del Temp\line.tmp
					del Temp\notechoed.tmp
					rem 有转义符
					for /f tokens^=1^-2^ delims^=^" %%d in ("%%y") do (
						if not "%%e" == "" (
							echo; > Temp\content.tmp
						)
					)
					if not exist Temp\content.tmp (
						for /f tokens^=1^-5^ delims^=^" %%i in ("%%b") do (
							echo %%i"%%j"%%k"%%y"%%m
						)
					) else (
						echo %%y
						del Temp\content.tmp
					)
				)
			)
		)
		if exist Temp\notechoed.tmp (
			echo %%b
		) else (
			echo; > Temp\notechoed.tmp
		)
		echo; >> Temp\counter.tmp
	)) > %PROJECT_DIR%\Workspace\%dir_name%\%%~na.json
	del Temp\notechoed.tmp
	del Temp\raw_%%~na.tmp
	echo 已完成转换:%%~na
	) else (
	echo %%~na未转换.
	)
	
)
"""