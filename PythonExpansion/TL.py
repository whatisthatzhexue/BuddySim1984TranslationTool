# -*- coding: utf-8 -*-

# This code shows an example of text translation from English to Simplified-Chinese.
# This code runs on Python 2.7.x and Python 3.x.
# You may install `requests` to run this code: pip install requests
# Please refer to `https://api.fanyi.baidu.com/doc/21` for complete api document
import sys
import os

import requests
import random
import json
from hashlib import md5

# For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`

app_installed = False
app = []
# Generate salt and sign
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()

def get_app():
    # Set your own appid/appkey.
    if not os.path.isfile("PythonExpansion\\APIs\\BaiduAPI.txt"):
        print("找不到API。")
        return False
    with open("PythonExpansion\\APIs\\BaiduAPI.txt") as f:
        content = json.load(f)
    global app
    app = [content["APPID"], content["APPKEY"]]
    return True

def get_translated(query, from_lang='en', to_lang='zh', url='http://api.fanyi.baidu.com/api/trans/vip/translate'):
    search = "PythonExpansion\\Translated\\" + make_md5(query)
    if os.path.isfile(search):
        print("找到翻译记录:")
        with open(search) as f:
            content = f.read()
        return content
    #试图获取一次appid,appkey
    global app_installed
    global app
    if not app_installed:
        app_installed = True
        if not get_app():
            return ""
    else:
        if len(app) == 0:
            return ""
    appid = app[0]
    appkey = app[1]
    #salt,sign
    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)

    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()

    # Show response
    result = json.dumps(result, indent=4, ensure_ascii=False)
    result = json.loads(result)
    
    # Get dest
    newline = False
    dst_ = ""
    for tr in result["trans_result"]:
        if newline:
            dst_ += "\n"
        else:
            newline = True
        dst_ += tr["dst"]
    
    #Save
    if not os.path.isdir("PythonExpansion\\Translated\\"):
        os.makedirs(os.getcwd() + "\\PythonExpansion\\Translated")
    query_md5 = make_md5(query)
    with open("PythonExpansion\\Translated\\" + query_md5, 'w') as f:
        f.write(dst_)
    with open("PythonExpansion\\Translated\\地址.txt", 'a') as f:
        f.write(query_md5)
        f.write(query + " -> " + dst_)
    print("翻译结果已保存.")
    
    return dst_

#正文
level = sys.argv[2]
path = sys.argv[1] + "\\Workspace\\" + level

def loopfor(key, banlist2):
    global ckey
    global bkey
    success = False
    for ban in banlist2:
        #查找
        ckey = key[:len(ban)]
        if ckey.lower() == ban:
            bkey = key[len(ban):]
            success = True
            if len(bkey) != 0:
                akey = bkey[0]
                if akey == ".":
                    break
                if akey == ",":
                    break
                if akey == "!":
                    break
                if akey == "?":
                    break
                if akey == ":":
                    break
                if akey == ";":
                    break
                if akey == ")":
                    break
                if akey == "(":
                    break
                if akey == "-":
                    break
                if akey == "'":
                    break
                if akey == "’":
                    break
                if akey == "‘":
                    break
                success = False
            if success: break
    return success

with open(path + "文本翻译.txt", encoding="utf-8") as f:
    content = f.read()
#接下来就是对content进行分析+翻译+恢复
content = content.split("\n")
with open(path + "文本翻译_baidu.txt", "w", encoding="utf-8") as f:
    for line in content:
        cantrans = False
        for line_ in line.split(":"):
            if line_ == "当前文件":
                break
            if line_ == "备注":
                break
            #确定是否要翻译
            rm = line.replace(" ","")
            if len(rm)!=0:
                if len(rm) >= 2:
                    if rm[(len(rm) - 2):] == "\",":
                        break
                rm = rm[len(rm) - 1]
            else:
                break
            if rm == ".":
                cantrans = True
                break
            if rm == ",":
                cantrans = True
                break
            if rm == "!":
                cantrans = True
                break
            if rm == "?":
                cantrans = True
                break
            if rm == ":":
                cantrans = True
                break
            if rm == ";":
                cantrans = True
                break
            if rm == ")":
                cantrans = True
                break
            if rm == "(":
                cantrans = True
                break
            if rm == "-":
                cantrans = True
                break
            break
        if cantrans:
            line = line.replace("\t","")
            oldline = line
            #§
            list_ = []
            index = line.find("[")
            while index != -1:
                index_ = line.find("]")
                if index_ == -1:
                    break
                key = line[index:(index_ + 1)]
                list_.append(key)
                line = line.replace(key, "§", 1)
                index = line.find("[")
            #人名 + '!' + ''' +
            split_ = line.split(" ")
            banlist = ["Lloyds", "Numbly", "Sherb", "Squirt", "William", "Plappo", "Numbley", "Jane", "John", "Levi", "Barry", "Jonny", "Bronkh", "Urp", "Gwandma", "Bimmy", "Shelly", "Later", "Rebus", "Lardo", "Larzo", "Larno", "Larvo", "Larpo", "Ginny", "Clyde", "Darold", "Googan", "De", "Jo", "Bra", "Vi", "Sa", "Joe", "Tom", "Tim", "Jack", "Novak", "Crank", "Bana", "Groncho", "Buddy", "Owen", "Raffs", "Blug", "Skulk", "Phoney", "Lenox", "Skewer", "Morton", "Arbor", "France", "Milo", "Bean", "Scroobert", "Raff", "Isla", "Blugs", "Tortley", "Toot", "Rudy", "Botley", "Grin", "Reginald", "Ella", "Menopea", "Snoodlewonker", "Bonklegrogs", "Cauldron", "Dundee", "Lloyd"]
            banlist2 = ["Shape Gang", "Ella Menopea", "Sheriff Sherb", "William Knot", "That Guy", "Dead Gwandma", "Captain Chunk", "Captain Googan", "Dejo bravisa", "Bimmy Bardo", "Later Mcgater", "Tiny Joe", "King Raff"]
            list2 = []
            
            for element in range(len(banlist)):
                banlist[element] = banlist[element].lower()
            for element in range(len(banlist2)):
                banlist2[element] = banlist2[element].lower()
            
            line = ""
            tex = 0
            while tex < len(split_):
                #处理key
                #1.直接相等
                if tex != (len(split_) - 1):
                    key = (split_[tex] + " " + split_[tex + 1])
                    if loopfor(key, banlist2):
                        #bkey为后缀
                        list2.append(ckey)
                        line += "√" + bkey
                        del split_[tex + 1]
                        if tex != (len(split_) - 1): line += " "
                        tex += 1
                        continue
                key = split_[tex]
                if loopfor(key, banlist):
                    list2.append(ckey)
                    line += "√" + bkey
                else:
                    line += key
                if tex != (len(split_) - 1): line += " "
                tex += 1
            
            #"...", ":)", ":(", 
            banlist = ["...", ":)", ":("]
            list3 = [""] * len(line)
            for ban in banlist:
                index_ = line.find(ban)
                while index_ != -1:
                    list3[index_] = ban
                    line = line.replace(ban, "■", 1)
                    index_ = line.find(ban)
            #翻译
            line = get_translated(line)
            for element in list_:
                line = line.replace("§", element, 1)
            for element in list2:
                line = line.replace("√", element, 1)
            for element in list3:
                if len(element) == 0: continue
                line = line.replace("■", element, 1)
            f.write("\t")
            f.write(line)
            print(oldline + " -> " + line)
        else:
            f.write(line)
        f.write("\n")