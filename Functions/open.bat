if not exist "%PROJECT_DIR%\Workspace\%1文本翻译.txt" (
	copy "%PROJECT_DIR%\Workspace\%1文本.txt" "%PROJECT_DIR%\Workspace\%1文本翻译.txt"
)
"D:\Program Files\Notepad++\notepad++.exe" "%PROJECT_DIR%\Workspace\%1文本翻译.txt"