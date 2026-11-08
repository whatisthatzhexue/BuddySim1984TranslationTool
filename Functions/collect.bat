setlocal enabledelayedexpansion

echo 开始收集文件%1...
set dir_name=%1
set /a count=0
set /a success=0
set txt_path=%PROJECT_DIR%\MonoBehaviour\%dir_name%
set json_path=%PROJECT_DIR%\Json\%dir_name%
set ex_path=%PROJECT_DIR%\Json_Collected\%dir_name%
md %ex_path%
for %%i in (%txt_path%\*.txt) do (
	set num=%%~ni
	set /a c=0
	call :charat
	set source=%json_path%\unnamed asset-%dir_name%-!num!.json
	set dest=%ex_path%\%%~ni.json
	if exist "!source!" (
		copy "!source!" "!dest!"
		set /a success+=1
	) else (
		echo !dest!>>Temp\notfound.tmp
	)
	set /a count+=1
)
echo 复制完成.应复制%count%个文件.
if %success% equ %count% (
	echo 所有文件全部成功复制.
) else (
	echo %success%/%count%.缺少文件.丢失的文件为.
	for /f delims^= %%a in (Temp\notfound.tmp) do (
		echo %%a
	)
)
del Temp\notfound.tmp
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