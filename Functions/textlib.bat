set dir_name=%1

if not exist %PROJECT_DIR%\TextLib\ (
	md %PROJECT_DIR%\TextLib
)
for %%a in (%PROJECT_DIR%\TextMesh\%dir_name%\*.txt) do (
	rem %%a代表一个文件
	copy "%%a" Temp\TEMP.tmp
	call :TRANSFER
)

for %%a in (Temp\*.tmp) do (
	del %%a
)
goto end

:TRANSFER
	for /f "delims=" %%c in (Temp\TEMP.tmp) do (
		rem %%c代表一行的内容
		for /f "tokens=1-3" %%x in ("%%c") do (
			if "%%z" == "m_Text" (
				echo %%c>Temp\TEXT.tmp
				certutil -hashfile "Temp\TEXT.tmp" MD5>Temp\HASH2.tmp
				for /f "skip=1" %%d in (Temp\HASH2.tmp) do (
					if not exist %PROJECT_DIR%\TextLib\%%d (
					echo %%c>%PROJECT_DIR%\TextLib\%%d
					echo %%c 已存储.地址.%%d
					echo %%d>>%PROJECT_DIR%\TextMesh\地址.txt
					echo %%c>>%PROJECT_DIR%\TextMesh\地址.txt
					)
					goto end
				)
			)
		)
	)
	goto end

:end