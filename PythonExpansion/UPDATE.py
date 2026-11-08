import os

Game_Path = "C:\\Users\\用户\\Desktop\\Translate\\BS1984-3_2_4\\Buddy Simulator 1984_Data\\"
files = os.listdir(Game_Path)

for file in files:
    file_dir = Game_Path + file
    if os.path.isdir(file_dir):
        continue
    if file[-4:] == '-mod':
        sh = file_dir[:-4]
        os.remove(sh)
        os.rename(file_dir, sh)
        print(file_dir + '已更新为' + sh)