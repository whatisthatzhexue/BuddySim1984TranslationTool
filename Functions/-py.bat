if exist PythonExpansion\%1.py (
	set /p INPUT=参数:
) else (
	echo 可用的指令:
	for %%i in (PythonExpansion\*.py) do (
		echo "-py %%~ni"
	)
	goto end
)
python PythonExpansion\%1.py "%PROJECT_DIR%" "%INPUT%"
goto end

:end