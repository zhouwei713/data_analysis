# coding = utf-8
"""
@author: zhou
@time:2019/8/6 13:26
@File: test.py
"""

from bs4 import BeautifulSoup
import os


def deal(html, nopic):
    htmlfile = open(r'html_page/' + html, 'r', encoding='utf-8').read()
    content = BeautifulSoup(htmlfile, 'html.parser')
    div = content.find('div', attrs={"class": 'detail'}).find('div')
    # print(div)
    pic_url = div.find_all('img')
    # print(len(pic_url))
    url_list = []
    for u in pic_url:
        tmp = []
        if u['src'] != nopic:
            tmp.append(u['src'])
            url_list.append(tmp)
    return url_list


if __name__ == '__main__':
    u = deal("806213.html", 'https://img1.qunliao.info/fastdfs3/M00/73/C6/ChOxM1vG51KAc8lHAAWteFNO4iE816.jpg')
    print(u)