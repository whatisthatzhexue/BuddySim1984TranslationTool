set dir_name=%1

set /a filenum=0
for %%a in (%PROJECT_DIR%\Json_Collected\%dir_name%\*.json) do (
	set /a filenum+=1
)
echo %1 共%filenum%个json文件

echo 正在输出%1文本.txt...
if not exist Temp\ md Temp
(for %%a in (%PROJECT_DIR%\Json_Collected\%dir_name%\*.json) do (
	echo 当前文件:%%a
	for /f delims^= %%b in (%%a) do (
		for /f "tokens=1,2 delims=\" %%e in ("%%b") do (
			rem 有转义符时
			if not "%%f" == "" (
				echo; > Temp\content.tmp
			)
		)
		if not exist Temp\content.tmp (
			for /f tokens^=1^-4^ delims^=^" %%i in ("%%b") do (
				if "%%j" == "1 UInt8 isBuddy" (
					if exist Temp\notblack.tmp (
					if exist Temp\buddy.tmp (
						if "%%k" == ": 0," (
							echo 备注:	未检测到Buddy消息
							del Temp\buddy.tmp
						)
					) else (
						if "%%k" == ": 1," (
							echo 备注:	检测到Buddy消息
							echo; > Temp\buddy.tmp
						)
					)
					)
				) else for /f %%c in ("%%l") do (
					if not exist Temp\notblack.tmp (
						echo; > Temp\notblack.tmp
					)
					for /f %%d in (黑名单.txt) do (
						if /i "%%c" == "%%d" (
							del Temp\notblack.tmp
						)
					)
					if exist Temp\notblack.tmp (
						if "%%j" == "1 string text" (
							echo 	%%l
							rem :LINE !line!
						) else if "%%j" == "1 string data" (
							echo 	%%l
							rem :LINE !line!
						) else if "%%j" == "1 string targetString" (
							echo 	%%l
							rem :LINE !line!
						) else if "%%j" == "1 string id" (
							echo 备注:%%l
						) else if "%%j" == "1 string otherObjectName" (
							echo 备注:物体名:%%l
						)
					)
				)
			)
		) else (
			echo %%b
			del Temp\content.tmp
		)
	)
	if exist Temp\buddy.tmp del Temp\buddy.tmp
)) > %PROJECT_DIR%\Workspace\%1文本.txt

if not exist %PROJECT_DIR%\Workspace\行数\ (
	md %PROJECT_DIR%\Workspace\行数
)
setlocal enabledelayedexpansion
echo 正在输出行数文件...
(for %%a in (%PROJECT_DIR%\Json_Collected\%dir_name%\*.json) do (
	echo 当前文件:%%a
	set /a line=0
	for /f delims^= %%b in (%%a) do (
		set /a line+=3
		for /f "tokens=1,2 delims=\" %%e in ("%%b") do (
			rem 有转义符时
			if not "%%f" == "" (
				echo; > Temp\content.tmp
			)
		)
		if not exist Temp\content.tmp (
			for /f tokens^=1^-4^ delims^=^" %%i in ("%%b") do (
				for /f %%c in ("%%l") do (
					for /f %%d in (黑名单.txt) do (
						if /i "%%c" == "%%d" (
							del Temp\notblack.tmp
						)
					)
					if exist Temp\notblack.tmp (
						if "%%j" == "1 string text" (
							echo !line!
						) else if "%%j" == "1 string data" (
							echo !line!
						) else if "%%j" == "1 string targetString" (
							echo !line!
						)
					) else (
						echo; > Temp\notblack.tmp
					)
				)
			)
		) else (
			echo !line!
			del Temp\content.tmp
		)
	)
)) > %PROJECT_DIR%\Workspace\行数\%1
endlocal

del Temp\notblack.tmp
echo 完成.