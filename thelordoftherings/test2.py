# encoding: utf-8

"""
@version: ??
@author: Andy
@file: test.py
@time: 2021/5/16 11:01
"""

import requests
from selenium import webdriver
from selenium.webdriver import ChromeOptions
import time
import json
from fake_useragent import UserAgent

ua = UserAgent()

url1 = 'http://m.maoyan.com/review/v2/comments.json?movieId=1220&offset=105&limit=15&type=2'


accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
cookie = "_lxsdk_cuid=174e91a0eacc8-003ae402fca25c-1b3d6253-13c680-174e91a0eacc8; iuuid=A017B26004A311EB9FC13F116A8E15B29436E6E87551467D94EA92FE0A3D2179; ci=55%2C%E5%8D%97%E4%BA%AC; selectci=; __mta=150183561.1601638633654.1601638633654.1608816516172.2; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1621130789; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; webp=true; featrues=[object Object]; _lxsdk=4F307590B5EB11EB8968CD5407AC3BD588A9F45C39194128B82832F7CEC0C57D; __mta=150183561.1601638633654.1621130807645.1621131875016.8; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1621132292; _lxsdk_s=17972ecc200-203-7a5-93f%7C%7C51"
headers = {"User-Agent": ua.chrome,
           "Cookie": cookie,
           "Accept": accept,
           "Host": "m.maoyan.com",
           "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
           "sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
           "Upgrade-Insecure-Requests": "1",
           "Accept-Encoding": "gzip, deflate, br",
           "Cache-Control": "max-age=0",
           "Connection": "keep-alive",
           "Sec-Fetch-Mode": "navigate",
           "Sec-Fetch-Dest": "document"
           }
res = requests.get(url1, headers=headers).json()
print(res)