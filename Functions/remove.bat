if "%1" == "" (
	(echo 无效的输入)
	goto end
)
set /a count=0
set dir_name=%PROJECT_DIR%\Workspace\%1\
if not exist %dir_name% (
	(echo 不存在%dir_name%的文件夹.)
	goto end
)
for %%a in (%dir_name%*) do (
	del %%a
	set /a count+=1
)
echo 已清除%1 的 %count%个文件.

:end