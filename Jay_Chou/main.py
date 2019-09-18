# coding = utf-8
"""
@author: zhou
@time:2019/9/18 9:57
@File: main.py
"""

import requests
import time
import os


def get_data():
    for i in range(0, 100):
        print("正在下载第%s页评论" % i)
        url = 'https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg?format=json&needNewCode=0&cid=205360772&biztype=2&topid=7876962&cmd=8&pagenum=%s&pagesize=50' % i
        res = requests.get(url).json()
        commentlist = res['comment']['commentlist']
        items = map(get_comment, commentlist)
        save_to_csv(items)
        time.sleep(1)


def get_comment(comment):
    comment_content = comment['rootcommentcontent'].strip().replace("\\n", "").replace("\n", "")
    return {"comment": comment_content}


def save_to_csv(data):
    if not os.path.exists(r'Jay_comment_data.csv'):
        with open('Jay_comment_data.csv', 'a+', encoding='utf-8') as f:
            f.write('comment\n')
            for d in data:
                try:
                    row = '{}'.format(d['comment'])
                    f.write(row)
                    f.write('\n')
                except:
                    continue
    else:
        with open('Jay_comment_data.csv', 'a+', encoding='utf-8') as f:
            for d in data:
                try:
                    row = '{}'.format(d['comment'])
                    f.write(row)
                    f.write('\n')
                except:
                    continue


if __name__ == '__main__':
    get_data()
