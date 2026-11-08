set path_=Projects\%1
if not exist %path_%\ (
	echo 无效路径.
	goto end
)
echo %path_%>当前项目.txt
set PROJECT_DIR=%path_%
echo 当前工作目录:%path_%\

goto end
:end