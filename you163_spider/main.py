
# coding = utf-8
"""
@author: zhou
@time:2019/8/24 11:50
@File: main.py
"""

from search import search_keyword
from details_page import details
import time


def main(name):
    product_id = search_keyword(name)
    for p in product_id:
        print("爬取产品 %s 信息" % p)
        time.sleep(1)
        details(p)


if __name__ == '__main__':
    main("iPhone")
