# -*- coding: utf-8 -*-

# 功能描述：百度翻译的API程序，实现对数据的批量翻译
# 作者：TS
# 时间：2022.5.22

import requests
import random
import json
from hashlib import md5
from time import  sleep
def trans(text):
    sleep(1)
    # Set your own appid/appkey.
    appid = 'appid'
    appkey = 'appKey'

    # For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
    from_lang = 'en'
    to_lang =  'zh'

    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path

    query = text

    # Generate salt and sign
    def make_md5(s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)

    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()
    return result['trans_result'][0]['dst']

if __name__ == '__main__':
    print(trans("I am chinses"))