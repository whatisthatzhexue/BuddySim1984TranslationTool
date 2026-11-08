for /f "tokens=1-2 delims=-" %%a in ("%1") do (
	set M_=%%a
	set N_=%%b
)
for /f "tokens=1-2 delims=-" %%a in ("%2") do (
	set O_=%%a
	set P_=%%b
)
setlocal enabledelayedexpansion
echo 开始level%M_%~%N_%...
set /a count_=%M_%
call :loop1
echo 开始sharedassets%O_%~%P_%...
set /a count_=%O_%
call :loop2
echo 全部完成.
endlocal

goto end

:loop1

call "Functions\clearmono.bat" level!count_!
call "Functions\filter.bat" level!count_!
if not !count_! equ %N_% (
	set /a count_+=1
	goto loop1
)
goto end

:loop2

call "Functions\clearmono.bat" sharedassets!count_!.assets
call "Functions\filter.bat" sharedassets!count_!.assets
if not !count_! == %P_% (
	set /a count_+=1
	goto loop2
)
goto end

:end