set dir_name=%1
set path_1=%PROJECT_DIR%\MonoBehaviour_All\%dir_name%
set path_2=%PROJECT_DIR%\MonoBehaviour\%dir_name%

if not exist %path_2%\ (
	md %path_2%\
)
set /a previous_count=0
for %%a in (%path_1%\*.txt) do (
	set /a previous_count+=1
)
echo 即将对%path_1%\进行过滤.当前文件数%previous_count%.

setlocal enabledelayedexpansion
set /a count=0
for %%a in (%path_1%\*.txt) do (
	set /a count+=1
	set file_p=%%a
	call :check
	if exist Temp\test.tmp (
		del Temp\test.tmp
		echo 进度!count!/%previous_count%.%%~na通过检查.
		copy "%path_1%\%%~na.txt" "%path_2%\%%~na.txt"
	) else (
		echo 进度!count!/%previous_count%.%%~na未通过.
	)
)
endlocal

set /a count=0
for %%a in (%path_2%\*.txt) do (
	set /a count+=1
)
echo 过滤完成.得到文件数%count%.先前为%previous_count%.

for %%a in (Temp\*) do (
	del %%a
)
goto end

:check
for /f delims^= %%b in (!file_p!) do (
	for /f tokens^=1^-2^ delims^=^	^" %%i in ("%%b") do (
		for /f %%c in ("%%j") do (
			for /f %%d in (黑名单.txt) do (
				if /i "%%c" == "%%d" (
					del Temp\notblack.tmp
				)
			)
			if exist Temp\notblack.tmp (
				if "%%i" == "string text = " (
					echo; >Temp\test.tmp
					goto end
				) else if "%%i" == "string data = " (
					echo; >Temp\test.tmp
					goto end
				) else if "%%i" == "string targetString = " (
					echo; >Temp\test.tmp
					goto end
				)
			) else (
				echo; > Temp\notblack.tmp
			)
		)
	)
)
goto end

:end