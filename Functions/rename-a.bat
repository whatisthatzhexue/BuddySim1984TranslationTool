setlocal enabledelayedexpansion

echo 开始重命名文件%1 \ %2...
set dir_name=%1
set /a count=0
set ex_path=%PROJECT_DIR%\%dir_name%\%2
set ex_path1=%PROJECT_DIR%\%dir_name%\%2_renamed
md %ex_path1%
for %%i in (%ex_path%\*.json) do (
	set num=%%~ni
	set /a c=0
	call :charat
	set dest=%ex_path1%\unnamed asset-%2-!num!.json
	copy %%i "!dest!"
	echo 已将"%%i"复制到"!dest!"
	set /a count+=1
)
echo 重命名完成.共%count%个文件.
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