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


emoji_pattern = re.compile("["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                       "]+", flags=re.UNICODE)


def fire():
    page = 0
    for i in range(15, 1200, 15):
        print("开始爬取第 %s 页" % page)
        url = 'http://m.maoyan.com/review/v2/comments.json?movieId=343473&offset={}&limit=15&type=2'.format(i)
        res = requests.get(url).json()
        if not res['paging']['hasMore']:
            print("爬取完成")
            break
        data = get_json(res)
        save_to_csv(data)
        time.sleep(1)
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
                ticket == 1
            else:
                ticket = 0
        except:
            ticket = 0
        tmp = [content, gender, userLevel, score, ticket]
        data_list.append(tmp)
    return data_list


def save_to_csv(data):
    if not os.path.exists(r'maoyan_data.csv'):
        with open('maoyan_data.csv', 'a+', encoding='utf-8') as f:
            f.write('content,gender,userlevel,score,ticket\n')
            for d in data:
                try:
                    row = '{},{},{},{},{}'.format(d[0], d[1], d[2], d[3], d[4])
                    f.write(row)
                    f.write('\n')
                except:
                    continue
    else:
        with open('maoyan_data.csv', 'a+', encoding='utf-8') as f:
            for d in data:
                try:
                    row = '{},{},{},{},{}'.format(d[0], d[1], d[2], d[3], d[4])
                    f.write(row)
                    f.write('\n')
                except:
                    continue


if __name__ == '__main__':
    fire()
