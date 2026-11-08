set dir_name=%1

if not exist %PROJECT_DIR%\WordLib\ (
	echo 错误.词库不存在.
	goto end
)
set /a c_=0
for %%a in (%PROJECT_DIR%\Workspace\%1*.txt) do (
	echo %%a
	set /a c_+=1
)
if not "%c_%" == "1" (
	goto loop
)
set file_=%1文本
goto next
:loop
set /p file_=请输入要加载的文件名(不含后缀):
if not exist "%PROJECT_DIR%\Workspace\%file_%.txt" (
	echo %file_%.txt不存在
	goto loop
)

:next
set new=%PROJECT_DIR%\Workspace\%dir_name%_Translated.txt
if not exist %PROJECT_DIR%\Workspace\%dir_name%文本翻译.txt (
	set new=%PROJECT_DIR%\Workspace\%dir_name%文本翻译.txt
)
echo 正在使用词库翻译%dir_name%...
(for /f "delims=" %%a in (%PROJECT_DIR%\Workspace\%file_%.txt) do (
	rem %%a就是每*一行*内容
	if not exist Temp\NOTECHOED.tmp (
		echo;>Temp\NOTECHOED.tmp
	)
	for /f "delims=:" %%b in ("%%a") do (
		if not "%%b" == "备注" (
		if not "%%b" == "当前文件" (
			for /f tokens^=1^-2^ delims^=^" %%d in ("%%a") do (
				rem 有转义符
				if not "%%e" == "" (
					echo;>Temp\content.tmp
				)
			)
			for /f "delims=	" %%d in ("%%a") do (
				echo %%d>Temp\TEXT.tmp
			)
			certutil -hashfile "Temp\TEXT.tmp" MD5>Temp\HASH.tmp
			call :HASHCHECK
		)
		)
	)
	if exist Temp\NOTECHOED.tmp (
		echo %%a
	)
))>%new%

echo 翻译完毕.
for %%a in (Temp\*.tmp) do (
	del %%a
)
goto end

:HASHCHECK
rem 用%%b获取HASH
for /f "skip=1" %%b in (Temp\HASH.tmp) do (
	if exist %PROJECT_DIR%\WordLib\%%b (
		for /f "delims=" %%c in (%PROJECT_DIR%\WordLib\%%b) do (
			rem %%c就是中文文本.
			if exist Temp\content.tmp (
				echo %%c
				del Temp\content.tmp
			) else (
				echo 	%%c
			)
			del Temp\NOTECHOED.tmp
		)
	)
	goto end
)
goto end

:end