set dir_name=%1

if not exist %PROJECT_DIR%\TextLib\ (
	echo 错误.text库不存在.
	goto end
)
if not exist %PROJECT_DIR%\TextMesh\%dir_name%_T\ (
	md %PROJECT_DIR%\TextMesh\%dir_name%_T
)

echo 正在使用text库翻译%dir_name%...
for %%a in (%PROJECT_DIR%\TextMesh\%dir_name%\*.txt) do (
	copy "%%a" Temp\TEMP.tmp>nul
	echo;>Temp\NONEED.tmp
	(for /f "delims=" %%b in (Temp\TEMP.tmp) do (
		for /f "tokens=1-3" %%x in ("%%b") do (
			if "%%z" == "m_Text" (
				echo %%b>Temp\TEXT.tmp
				certutil -hashfile "Temp\TEXT.tmp" MD5>Temp\HASH.tmp
				call :FINDFILE
			) else (
				echo %%b
			)
		)
	))>Temp\Late.tmp
	if not exist Temp\NONEED.tmp (
		copy Temp\Late.tmp "%PROJECT_DIR%\TextMesh\%dir_name%_T\%%~na%%~xa"
		echo 完成翻译:%%~na
	)
)
for %%a in (Temp\*.tmp) do (
	del %%a
)
goto end

:FINDFILE
for /f "skip=1" %%c in (Temp\HASH.tmp) do (
	if not exist %PROJECT_DIR%\TextLib\%%c (
		echo %%b
	) else (
		for /f "delims=" %%d in (%PROJECT_DIR%\TextLib\%%c) do (
			if not "%%b" == "%%d" (
				del Temp\NONEED.tmp
				echo %%d
			)
		)
	)
	goto end
)
goto end

:end