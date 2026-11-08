for /f "tokens=1-2 delims=-" %%a in ("%1") do (
	set M_=%%a
	set N_=%%b
)
for /f "tokens=1-2 delims=-" %%a in ("%2") do (
	set O_=%%a
	set P_=%%b
)
(echo 开始level%M_%~%N_%...
set /a count_=%M_%
call :loop1
echo 开始sharedassets%O_%~%P_%...
set /a count_=%O_%
call :loop2)>文本们.txt
echo 全部完成.

goto end

:loop1

rem call "Functions\save.bat" level%count_%
rem call "Functions\usewordlib.bat" level%count_%
python PythonExpansion\TL.py "%PROJECT_DIR%" level%count_%
if not %count_% equ %N_% (
	set /a count_+=1
	goto loop1
)
goto end

:loop2

rem call "Functions\save.bat" sharedassets%count_%.assets
rem call "Functions\usewordlib.bat" sharedassets%count_%.assets
python PythonExpansion\TL.py "%PROJECT_DIR%" sharedassets%count_%.assets
if not %count_% == %P_% (
	set /a count_+=1
	goto loop2
)
goto end

:end