set p="C:\Users\用户\Desktop\Translate\Buddy Simulator 1984-test\Buddy Simulator 1984_Data\data1.unity3d"
set q="C:\Users\用户\Desktop\Translate\Buddy Simulator 1984-test\Buddy Simulator 1984_Data\data.unity3d"
if not exist %p% (
	echo data1不存在
	goto end
)
del %q%
ren %p% data.unity3d
echo 已将data1更新为data
:end