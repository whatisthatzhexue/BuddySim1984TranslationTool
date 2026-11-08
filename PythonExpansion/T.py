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

query = sys.argv[2]
print(query + " -> " + get_translated(query))