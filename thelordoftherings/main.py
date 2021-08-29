# coding = utf-8
"""
@author: zhou
@time:2019/8/29 17:43
@File: main.py
"""

import requests
import re
import time
import os
import json
from fake_useragent import UserAgent

ua = UserAgent()


emoji_pattern = re.compile("["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                       "]+", flags=re.UNICODE)

accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
cookie = "_lxsdk_cuid=174e91a0eacc8-003ae402fca25c-1b3d6253-13c680-174e91a0eacc8; iuuid=A017B26004A311EB9FC13F116A8E15B29436E6E87551467D94EA92FE0A3D2179; ci=55%2C%E5%8D%97%E4%BA%AC; selectci=; __mta=150183561.1601638633654.1601638633654.1608816516172.2; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1621130789; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; webp=true; featrues=[object Object]; _lxsdk=4F307590B5EB11EB8968CD5407AC3BD588A9F45C39194128B82832F7CEC0C57D; __mta=150183561.1601638633654.1621130807645.1621131875016.8; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1621132292; _lxsdk_s=17972ecc200-203-7a5-93f%7C%7C51"
headers = {"User-Agent": ua.random,
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


def fire(num):
    page = 0
    for i in range(15, 135, 15):
        print("开始爬取第 %s 页" % page)
        headers["User-Agent"] = ua.random
        url1 = 'http://m.maoyan.com/review/v2/comments.json?movieId=1220&offset={}&limit=15&type=2'.format(
            i)  # rings 1
        url2 = 'http://m.maoyan.com/review/v2/comments.json?movieId=1221&offset={}&limit=15&type=2'.format(
            i)  # rings 2
        url3 = 'http://m.maoyan.com/review/v2/comments.json?movieId=428&offset={}&limit=15&type=2'.format(
            i)  # rings 3
        try:
            if num == 1:
                print(url1)
                res = requests.get(url1, headers=headers).json()
            elif num == 2:
                print(url2)
                res = requests.get(url2, headers=headers).json()
            else:
                print(url3)
                res = requests.get(url3, headers=headers).json()
        except Exception as e:
            print(e)
            time.sleep(120)
            # continue
        # if not to_json['paging']['hasMore']:
        if not res['paging']['hasMore']:
            print("爬取完成")
            # driver.close()
            break
        data = get_json(res)
        # data = get_json(to_json)
        save_to_csv(data, num)
        time.sleep(20)
        page += 1


def get_json(res):
    data_list = []
    data = res['data']['comments']
    for d in data:
        content = d['content'].replace('\n', '').strip().replace(',', '，')
        content = emoji_pattern.sub(r'', content)
        gender = d['gender']
        userLevel = d['userLevel']
        score = d['score']
        ticket = 0
        try:
            if len(d['tagList']) == 0:
                ticket = 0
            elif len(d['tagList']) == 1:
                if d['tagList'][0]['id'] == 4:
                    ticket = 1
                else:
                    ticket = 0
            elif len(d['tagList']) == 2:
                ticket = 1
            else:
                ticket = 0
        except:
            ticket = 0
        tmp = [content, gender, userLevel, score, ticket]
        data_list.append(tmp)
    return data_list


def save_to_csv(data, num):
    if not os.path.exists(r'maoyan_data_rings%s.csv' % str(num)):
        with open('maoyan_data_rings%s.csv' % str(num), 'a+', encoding='utf-8') as f:
            f.write('content,gender,userlevel,score,ticket\n')
            for d in data:
                try:
                    row = '{},{},{},{},{}'.format(d[0], d[1], d[2], d[3], d[4])
                    f.write(row)
                    f.write('\n')
                except:
                    continue
    else:
        with open('maoyan_data_rings%s.csv' % str(num), 'a+', encoding='utf-8') as f:
            for d in data:
                try:
                    row = '{},{},{},{},{}'.format(d[0], d[1], d[2], d[3], d[4])
                    f.write(row)
                    f.write('\n')
                except:
                    continue


if __name__ == '__main__':
    for i in range(2, 4):
        print("get rings %s data" % str(i))
        fire(i)

