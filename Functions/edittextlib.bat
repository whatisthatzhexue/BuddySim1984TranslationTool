rem notepad.exe %PROJECT_DIR%\TextMesh\地址.txt
set /p string=请输入地址:
if not exist %PROJECT_DIR%\TextLib\%string% (
	echo 文件%PROJECT_DIR%\TextLib\%string%不存在.
) else (
	for /f "delims=" %%c in (%PROJECT_DIR%\TextLib\%string%) do (
		echo %%c
	)
	notepad.exe %PROJECT_DIR%\TextLib\%string%
	for /f "delims=" %%c in (%PROJECT_DIR%\TextLib\%string%) do (
		echo %%c
	) 
)