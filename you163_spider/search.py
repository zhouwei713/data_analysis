# coding = utf-8
"""
@author: zhou
@time:2019/8/24 12:46
@File: search.py
"""

import requests


def search_keyword(keyword):
    uri = 'https://you.163.com/xhr/search/search.json'
    query = {
        "keyword": keyword,
        "page": 1
    }
    try:
        res = requests.get(uri, params=query).json()
        result = res['data']['directly']['searcherResult']['result']
        product_id = []
        for r in result:
            product_id.append(r['id'])
        return product_id
    except:
        raise


if __name__ == '__main__':
    result = search_keyword("胸罩")
    print(result)
