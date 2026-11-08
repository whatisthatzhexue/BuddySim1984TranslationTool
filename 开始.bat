@echo off
CHCP 65001
cls
title JSON批处理器
echo 欢迎来到JSON批处理器 (版本v1.0.0)
echo 输入h获取更多帮助
set PROJECT_DIR=Projects\New
if exist 当前项目.txt (
	for /f "delims=" %%a in (当前项目.txt) do (
		set PROJECT_DIR=%%a
	)
)
echo 当前工作目录:%PROJECT_DIR%\
if exist 备忘录.txt (
	echo 以下是备忘录.可使用edit修改备忘录内容.
	for /f "delims=" %%a in (备忘录.txt) do (
		echo %%a
	)
)
:GETINPUT
set /p INPUT=指令:
for /f "tokens=1-4" %%a in ("%INPUT%") do (
	if exist "Functions\%%a.bat" (
		if /i not "%%a" == "h" (
		if /i not "%%a" == "manage" (
		if not exist %PROJECT_DIR%\ (
			echo 错误:工作目录不存在.请输入manage命令修改工作目录.
			echo 提示:使用md指令.即cmd自带指令.可以新建目录.
			goto :GETINPUT
		)
		)
		)
		call "Functions\%%a.bat" %%b %%c %%d
	) else (
		call %INPUT%
	)
)
goto :GETINPUT
pause