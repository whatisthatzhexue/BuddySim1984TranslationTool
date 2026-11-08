set dir_name=%1
for %%a in (%PROJECT_DIR%\Workspace\%1*.txt) do (
	echo %%a
)
:loop
set /p file_=请输入要加载的文件名(不含后缀):
if not exist "%PROJECT_DIR%\Workspace\%file_%.txt" (
	echo %file_%.txt不存在
	goto loop
)

echo 文本文件转换/记录文件中...
for /f "delims=" %%a in (%PROJECT_DIR%\Workspace\%file_%.txt) do (
	for /f "tokens=1,2 delims=:" %%b in ("%%a") do (
		if "%%b" == "当前文件" (
			echo %%c> Temp\editingfile.tmp
			echo %%c>> Temp\allfiles.tmp
			if exist Temp\text_%%~nc.tmp (
				del Temp\text_%%~nc.tmp
			)
		) else if not "%%b" == "备注" (
			for /f "delims=" %%d in (Temp\editingfile.tmp) do (
				for /f "delims=	" %%e in ("%%a") do echo %%e>> Temp\text_%%~nd.tmp
			)
		)
	)
)

echo 行数文件转换中...
for /f "delims=" %%a in (%PROJECT_DIR%\Workspace\行数\%1) do (
	for /f "tokens=1,2 delims=:" %%b in ("%%a") do (
		if "%%b" == "当前文件" (
			echo %%c> Temp\editingfile.tmp
			if exist Temp\numb_%%~nc.tmp (
				del Temp\numb_%%~nc.tmp
			)
		) else (
			for /f "delims=" %%d in (Temp\editingfile.tmp) do (
				echo %%a>> Temp\numb_%%~nd.tmp
			)
		)
	)
)

echo 行数§文字结合中...
for /f "delims=" %%a in (Temp\allfiles.tmp) do (
	echo; > Temp\counter.tmp
	for /f "delims=" %%b in (Temp\text_%%~na.tmp) do (
		echo %%~na>Temp\editingfile.tmp
		echo; > Temp\counter2.tmp
		for /f %%c in (Temp\numb_%%~na.tmp) do (
			if not exist breakloop.tmp (
				for %%d in (Temp\counter.tmp) do (
					for %%e in (Temp\counter2.tmp) do (
						if %%~zd equ %%~ze (
							del Temp\counter2.tmp
						)
					)
				)
				if not exist Temp\counter2.tmp (
					echo %%c§%%b>>Temp\raw_%%~na.tmp
					echo; > breakloop.tmp
				) else (
					echo; >> Temp\counter2.tmp
				)
			)
		)
		del breakloop.tmp
		rem 此处counter行数为line数
		echo; >> Temp\counter.tmp
	)
	del Temp\text_%%~na.tmp
	del Temp\numb_%%~na.tmp
	echo 已完成结合:%%~na
)

if not exist %PROJECT_DIR%\Workspace\%1\ (
	md %PROJECT_DIR%\Workspace\%1
)
echo 最终文件转换为json中...
for /f "delims=" %%a in (Temp\allfiles.tmp) do (
	if exist Temp\raw_%%~na.tmp (
	echo; > Temp\counter.tmp
	echo; > Temp\notechoed.tmp
	set str=%%~na
	(for /f "delims=" %%b in (%%a) do (
		rem 遍历每一个x(numb)y(text)
		if not exist Temp\line.tmp (
			call :getfirstline
			(for /f "skip=1 delims=" %%z in (Temp\raw_%%~na.tmp) do (
				echo %%z
			))>Temp\raw.tmp
			del Temp\raw_%%~na.tmp
			ren Temp\raw.tmp raw_%%~na.tmp
		)
		rem 遍历第一行
		if exist Temp\line.tmp for /f "tokens=1,2 delims=§" %%x in (Temp\line.tmp) do (
			for %%c in (Temp\counter.tmp) do (
				if "%%~zc" == "%%x" (
					del Temp\line.tmp
					del Temp\notechoed.tmp
					rem 有转义符
					for /f tokens^=1^-2^ delims^=^" %%d in ("%%y") do (
						if not "%%e" == "" (
							echo; > Temp\content.tmp
						)
					)
					if not exist Temp\content.tmp (
						for /f tokens^=1^-5^ delims^=^" %%i in ("%%b") do (
							echo %%i"%%j"%%k"%%y"%%m
						)
					) else (
						echo %%y
						del Temp\content.tmp
					)
				)
			)
		)
		if exist Temp\notechoed.tmp (
			echo %%b
		) else (
			echo; > Temp\notechoed.tmp
		)
		echo; >> Temp\counter.tmp
	)) > %PROJECT_DIR%\Workspace\%dir_name%\%%~na.json
	del Temp\notechoed.tmp
	del Temp\raw_%%~na.tmp
	echo 已完成转换:%%~na
	) else (
	echo %%~na未转换.
	)
	
)

for %%a in (Temp\*) do (
	del %%a
)
goto end

:getfirstline
for /f "delims=" %%a in (Temp\raw_%str%.tmp) do (
	echo %%a>Temp\line.tmp
	goto end
)
goto end

:end