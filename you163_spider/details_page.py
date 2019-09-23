# coding = utf-8
"""
@author: zhou
@time:2019/8/24 13:01
@File: details_page.py
"""

import requests
import time
from pymongo import MongoClient


conn = MongoClient("mongodb://%s:%s@ds149974.mlab.com:49974/you163" % ('you163', 'you163'))
db = conn.you163
mongo_collection = db.iPhone


def details(product_id):
    url = 'https://you.163.com/xhr/comment/listByItemByTag.json'
    try:
        C_list = []
        for i in range(1, 100):
            query = {
                "itemId": product_id,
                "page": i,
            }
            res = requests.get(url, params=query).json()
            if not res['data']['commentList']:
                break
            print("爬取第 %s 页评论" % i)
            commentList = res['data']['commentList']
            C_list.append(commentList)
            time.sleep(1)
            # save to mongoDB
            try:
                mongo_collection.insert_many(commentList)
            except:
                continue
        return C_list
    except:
        raise


if __name__ == '__main__':
    commentlist = details("1680205")
    print(commentlist)
