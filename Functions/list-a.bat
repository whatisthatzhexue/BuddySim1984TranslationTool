@echo off
setlocal enabledelayedexpansion

set /a skip_=0
if not "%3" == "" (
	set /a skip_=%3
)
echo 开始列举文件%1 \ %2...
set dir_name=%1
set /a count=0
set txt_path=%PROJECT_DIR%\%dir_name%\%2
for %%i in (%txt_path%\*.json) do (
	set /a count+=1
)
set Total=%count%
set /a count=0
for %%i in (%txt_path%\*.json) do (
	if !skip_! equ 0 (
	set num=%%~ni
	set /a c=0
	call :charat
	echo 进度:!count!/%Total%
	echo !num!
	pause
	) else (
	set /a skip_-=1
	)
	set /a count+=1
)
echo 列举完成.共%count%个文件.
endlocal
goto end

:charat
set char=!num:~%c%,1!
set /a c+=1
if not "%char%" == "-" (
	goto charat
)
set /a c-=1
set "num=!num:~0,%c%!"
goto end

:end