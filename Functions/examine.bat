set /a count=0
set /a succeed=0
for %%a in (%PROJECT_DIR%\Workspace\%1\*) do (
	set /a count+=1
)
fc %PROJECT_DIR%\Workspace\%1\* %PROJECT_DIR%\Json_Collected\%1\* >Temp\fc_.tmp
for /f "tokens=1,2 delims=:" %%a in (Temp\fc_.tmp) do (
	if not "%%b" == "" (
		if "%%b" == " no differences encountered" set /a succeed+=1
	)
)
del Temp\fc_.tmp
if %count% equ %succeed% (
echo 全部%count%个文件通过测试.
) else (
echo 完成.总检查数%count%.通过数%succeed%.
)