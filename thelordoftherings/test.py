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

url1 = 'http://m.maoyan.com/review/v2/comments.json?movieId=1220&offset=15&limit=15&type=2'


option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_argument("--disable-blink-features=AutomationControlled")
option.add_argument("user-agent=%s" %ua.chrome)
driver = webdriver.Chrome(options=option)
# driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#     "source": """
#         Object.defineProperty(navigator, 'webdriver', {
#             get: () => undefined
#         })
#     """
# })
with open('stealth.min.js') as f:
    js = f.read()
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": js
})
driver.get(url1)
content = driver.find_element_by_tag_name("pre").text
print(content)
print(type(content))
to_json = json.loads(content)
print(to_json)
print(type(to_json))

time.sleep(1000)
driver.close()