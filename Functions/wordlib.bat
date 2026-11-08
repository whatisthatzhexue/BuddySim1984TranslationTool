set dir_name=%1
echo 文本翻译文件转换/记录文件中...
for /f "delims=" %%a in (%PROJECT_DIR%\Workspace\%1文本翻译.txt) do (
	for /f "tokens=1,2 delims=:" %%b in ("%%a") do (
		if "%%b" == "当前文件" (
			echo %%c> Temp\editingfile.tmp
			if exist Temp\LOCKFILE.tmp (
				del Temp\LOCKFILE.tmp
			)
			if exist Temp\text_%%~nc.tmp (
				del Temp\text_%%~nc.tmp
			)
		) else if not "%%b" == "备注" (
			for /f "delims=" %%d in (Temp\editingfile.tmp) do (
				for /f "delims=	" %%e in ("%%a") do (
					echo %%e>> Temp\text_%%~nd.tmp
					if not exist Temp\LOCKFILE.tmp (
						echo %%d>> Temp\allfiles.tmp
						echo;>Temp\LOCKFILE.tmp
					)
				)
			)
		)
	)
)

echo 文本文件转换中...
for /f "delims=" %%a in (%PROJECT_DIR%\Workspace\%1文本.txt) do (
	for /f "tokens=1,2 delims=:" %%b in ("%%a") do (
		if "%%b" == "当前文件" (
			echo %%c> Temp\editingfile.tmp
			if exist Temp\texten_%%~nc.tmp (
				del Temp\texten_%%~nc.tmp
			)
		) else if not "%%b" == "备注" (
			for /f "delims=" %%d in (Temp\editingfile.tmp) do (
				for /f "delims=	" %%e in ("%%a") do echo %%e>> Temp\texten_%%~nd.tmp
			)
		)
	)
)

echo 文本§文本翻译结合中...
for /f "delims=" %%a in (Temp\allfiles.tmp) do (
	echo; > Temp\counter.tmp
	for /f "delims=" %%b in (Temp\text_%%~na.tmp) do (
		echo %%~na>Temp\editingfile.tmp
		echo; > Temp\counter2.tmp
		for /f "delims=" %%c in (Temp\texten_%%~na.tmp) do (
			if not exist Temp\breakloop.tmp (
				for %%d in (Temp\counter.tmp) do (
					for %%e in (Temp\counter2.tmp) do (
						if %%~zd equ %%~ze (
							del Temp\counter2.tmp
						)
					)
				)
				if not exist Temp\counter2.tmp (
					echo %%c§%%b>>Temp\raw_%%~na.tmp
					echo; > Temp\breakloop.tmp
				) else (
					echo; >> Temp\counter2.tmp
				)
			)
		)
		del Temp\breakloop.tmp
		rem 此处counter行数为line数
		echo; >> Temp\counter.tmp
	)
	del Temp\text_%%~na.tmp
	del Temp\texten_%%~na.tmp
	echo 已完成结合:%%~na
)

if not exist %PROJECT_DIR%\WordLib\ (
	md %PROJECT_DIR%\WordLib
)
echo 最终文件转换为词库中...
for /f "delims=" %%a in (Temp\allfiles.tmp) do (
	if exist Temp\raw_%%~na.tmp (
		rem 遍历每一个x(text),y(文本)
		for /f "tokens=1-2 delims=§" %%x in (Temp\raw_%%~na.tmp) do (
			if not "%%x" == "%%y" (
			echo %%x>Temp\TEXT.tmp
			certutil -hashfile "Temp\TEXT.tmp" MD5>Temp\HASH.tmp
			call :HASHCHECK
			)
		)
	)
)

for %%a in (Temp\*.tmp) do (
	del %%a
)
echo 词库更新完毕.
goto end

:HASHCHECK
rem 用%%b获取HASH
for /f "skip=1" %%b in (Temp\HASH.tmp) do (
	if not exist %PROJECT_DIR%\WordLib\%%b (
		echo %%y>%PROJECT_DIR%\WordLib\%%b
		echo %%x翻译到%%y.储存于文件%PROJECT_DIR%\WordLib\%%b.
	)
	goto end
)
goto end

:end