set dir_=%PROJECT_DIR%\MonoBehaviour_All\%1
setlocal enabledelayedexpansion
for /f delims^= %%a in (清除名单.txt) do (
	rem %%a就是SpriteLayerInfo, etc
	set /a count=0
	for %%b in (%dir_%\*) do (
		rem %%b就是每*一个*文件名
		for /f "tokens=1-2 delims=-" %%c in ("%%b") do (
			if "%%d" == "%%a" (
				del %%b
				set /a count+=1
			)
		)
	)
	echo 已清除 %1 中!count!个%%a.
)
endlocal