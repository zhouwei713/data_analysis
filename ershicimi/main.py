# coding = utf-8
"""
@author: zhou
@time:2019/10/17 17:25
@File: main.py
"""

# coding = utf-8
"""
@author: zhou
@time:2019/10/7 16:49
@File: main.py
"""

import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ChromeOptions
import time
import re
import numpy as np


session = {
        'dqduid': 'eyJpdiI6InF4UGh5aG5wNVQ1aDFvVGZkeTR5eU16aHVJYk5RN1RVVHptU210c3pra0U9IiwidmFsdWUiOiIrcXlQa3pmNGhaSkVHN3RvZ3ZyUVhuT0VBdTdYcEhrQ01EaEFTNW5heFY0QmZod0x0dlwvUFwvczc1TGQ0NERNVERcL21USUdCeDFYT1dQT3R1eTNaVXBiZz09IiwibWFjIjoiMWM2Y2ZmMWU3MDcyMWQwNTEwZGJjM2RlNDkyODMyYjI0ZjY1Y2MwODAxMTVmY2U2YmMwZmQ0MTRlYjMxOWE0YSJ9'}
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win32; x32; rv:54.0) Gecko/20100101 Firefox/54.0', 'Connection': 'keep-alive'}
Chrome_driver = webdriver.Chrome()
options = ChromeOptions()
options.add_argument(r"--user-data-dir=C:\Users\wei.zhou\AppData\Local\Google\Chrome\User Data\Default")


def get_players_urls(u):
    Chrome_driver = webdriver.Chrome(options=options)
    u = u
    Chrome_driver.get(u)
    time.sleep(2)
    ele_content = Chrome_driver.find_element_by_class_name("layui-table-body")
    ele_content_l = ele_content.find_element_by_tag_name('table').find_element_by_tag_name('tbody')
    ele_tr_l = ele_content_l.find_elements_by_tag_name('tr')
    for i in range(1, len(ele_tr_l) + 1):
        tmp = {}
        data = Chrome_driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/table/tbody/tr[%i]' % i).text.strip()
        split_data = data.split('\n')
        rank = split_data[0]
        name = split_data[1]
        yuanchuanghefawen = split_data[2]
        toutiao_read = split_data[3]
        citiao_read = split_data[4]
        seeing = split_data[5]
        appreciate = split_data[6]
        index = split_data[7]
        tmp['rank'] = rank
        tmp['name'] = name
        tmp['yuanchuanghefawen'] = yuanchuanghefawen
        tmp['toutiao_read'] = toutiao_read
        tmp['citiao_read'] = citiao_read
        tmp['seeing'] = seeing
        tmp['appreciate'] = appreciate
        tmp['index'] = index
        print(tmp)
        print('save to csv')
        save_to_csv(tmp)

    Chrome_driver.close()
    time.sleep(3)


def save_to_csv(data):
    if not os.path.exists('weichat_data.csv'):
        with open('weichat_data.csv', 'a+', encoding='utf-8') as f:
            f.write('rank,name,yuanchuanghefawen,toutiao_read,citiao_read,seeing,appreciate,index\n')
            try:
                row = '{},{},{},{},{},{},{},{}'.format(data['rank'],
                                                       data['name'],
                                                       data['yuanchuanghefawen'],
                                                       data['toutiao_read'],
                                                       data['citiao_read'],
                                                       data['seeing'],
                                                       data['appreciate'],
                                                       data['index'])
                f.write(row)
                f.write('\n')
            except:
                pass
    else:
        with open('weichat_data.csv', 'a+', encoding='utf-8') as f:
            try:
                row = '{},{},{},{},{},{},{},{}'.format(data['rank'],
                                                       data['name'],
                                                       data['yuanchuanghefawen'],
                                                       data['toutiao_read'],
                                                       data['citiao_read'],
                                                       data['seeing'],
                                                       data['appreciate'],
                                                       data['index'])
                f.write(row)
                f.write('\n')
            except:
                pass


if __name__ == '__main__':
    get_players_urls('https://www.ershicimi.com/rank/category/2?weekIndex=2')
    print("第二页")
    get_players_urls('https://www.ershicimi.com/rank/category/22?weekIndex=2')

