# coding = utf-8
"""
@author: zhouluobo
"""

import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import time


Headers = {'Cookie': 'SINAGLOBAL=4979979695709.662.1540896279940; SUB=_2AkMrYbTuf8PxqwJRmPkVyG_nb45wwwHEieKdPUU1JRMxHRl-yT83qnI9tRB6AOGaAcavhZVIZBiCoxtgPDNVspj9jtju; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5d4hHnVEbZCn4G2L775Qe1; _s_tentry=-; Apache=1711120851984.973.1564019682028; ULV=1564019682040:7:2:1:1711120851984.973.1564019682028:1563525180101; login_sid_t=8e1b73050dedb94d4996a67f8d74e464; cross_origin_proto=SSL; Ugrow-G0=140ad66ad7317901fc818d7fd7743564; YF-V5-G0=95d69db6bf5dfdb71f82a9b7f3eb261a; WBStorage=edfd723f2928ec64|undefined; UOR=bbs.51testing.com,widget.weibo.com,www.baidu.com; wb_view_log=1366*7681; WBtopGlobal_register_version=307744aa77dd5677; YF-Page-G0=580fe01acc9791e17cca20c5fa377d00|1564363890|1564363890'}


def mayili(page):
    mayili = []
    for i in range(0, page):
        print("page: ", i)
        url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id=4399042567665659&page=%s' % int(i)
        req = requests.get(url, headers=Headers).text
        html = json.loads(req)['data']['html']
        content = BeautifulSoup(html, "html.parser")
        # comment = content.find_all('div', attrs={'class': 'list_li S_line1 clearfix'})
        comment_text = content.find_all('div', attrs={'class': 'WB_text'})
        for c in comment_text:
            mayili_text = c.text.split("：")[1]
            mayili.append(mayili_text)
        time.sleep(5)

    return mayili


def wenzhang(page):
    wenzhang = []
    for i in range(0, page):
        print("page: ", i)
        url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id=4399042089738682&page=%s' % int(i)
        req = requests.get(url, headers=Headers).text
        html = json.loads(req)['data']['html']
        content = BeautifulSoup(html, "html.parser")
        # comment = content.find_all('div', attrs={'class': 'list_li S_line1 clearfix'})
        comment_text = content.find_all('div', attrs={'class': 'WB_text'})
        for c in comment_text:
            wenzhang_text = c.text.split("：")[1]
            wenzhang.append(wenzhang_text)
        time.sleep(5)

    return wenzhang


if __name__ == '__main__':
    print("start")
    ma_comment = mayili(1000)
    mayili_pd = pd.DataFrame(columns=['mayili_comment'], data=ma_comment)
    mayili_pd.to_csv('mayili.csv', encoding='utf-8')

    wen_comment = wenzhang(1000)
    wenzhang_pd = pd.DataFrame(columns=['wenzhang_comment'], data=wen_comment)
    wenzhang_pd.to_csv('wenzhang.csv', encoding='utf-8')
