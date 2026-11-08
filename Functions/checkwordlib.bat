set /p string=输入英文文本:
echo %string%>Temp\TEXT.tmp
certutil -hashfile "Temp\TEXT.tmp" MD5>Temp\HASH.tmp
call :HASHCHECK

for %%a in (Temp\*.tmp) do (
	del %%a
)
goto end

:HASHCHECK
rem 用%%b获取HASH
for /f "skip=1" %%b in (Temp\HASH.tmp) do (
	if not exist %PROJECT_DIR%\WordLib\%%b (
		echo 文件%PROJECT_DIR%\WordLib\%%b不存在.
	) else (
		rem notepad.exe %PROJECT_DIR%\WordLib\%%b
		for /f "delims=" %%c in (%PROJECT_DIR%\WordLib\%%b) do (
			echo "%%c"
		) 
	)
	goto end
)
goto end

:end