set path_2=%PROJECT_DIR%\%1

for %%a in (%path_2%\*) do (
	echo %%~na
	copy "%%a" Temp\TEMP.tmp
	for /f "delims=" %%b in (Temp\TEMP.tmp) do (
		rem %%b-每行内容
		for /f "tokens=1-3" %%i in ("%%b") do (
			if "%%k" == "m_Text" (
				echo 	%%b
				echo;
			)
		)
	)
)

del Temp\TEMP.tmp