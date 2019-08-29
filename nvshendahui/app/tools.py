# coding = utf-8
"""
@author: zhou
@time:2019/8/6 11:38
@File: tools.py
"""

import pandas as pd
from bs4 import BeautifulSoup


def deal_data():
    data = pd.read_csv(r'data/nvshen.csv')
    nvshen_list = []
    for d in data.values.tolist():
        tmp = []
        name = d[0]
        page_id = d[4]
        tmp.append(name)
        tmp.append(page_id)
        nvshen_list.append(tmp)
    return nvshen_list


def deal_html(html, nopic):
    htmlfile = open(r'../html_page/' + html, 'r', encoding='utf-8').read()
    content = BeautifulSoup(htmlfile, 'html.parser')
    div = content.find('div', attrs={"class": 'detail'}).find('div')
    pic_url = div.find_all('img')
    url_list = []
    for u in pic_url[:-1]:
        if u['src'] not in nopic:
            url_list.append(u['src'])
    return url_list

