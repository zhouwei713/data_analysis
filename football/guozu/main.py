# coding = utf-8
"""
@author: zhou
@time:2019/11/29 10:00
@File: main.py
"""

import pandas as pd
import time
import datetime
from datetime import timedelta
from collections import OrderedDict


# 传入的时间格式"2018-06"
def gen_time(datestart, dateend=None):
    if dateend is None:
        dateend = time.strftime('%Y-%m', time.localtime(time.time()))
    datestart=datetime.datetime.strptime(datestart, '%Y-%m')
    dateend=datetime.datetime.strptime(dateend, '%Y-%m')
    date_list = list(OrderedDict(((datestart + timedelta(_)).strftime(r"%Y-%m"), None) for _ in range((dateend - datestart).days)).keys())
    return date_list


# 获取国足排名
def get_rank(date):
    date_list = gen_time(date)
    rank = []
    print(date_list)
    for d in date_list:
        try:
            print('处理日期', d)
            url = 'http://www.mktcam.com/ziliao/fifarank.html?date=' + d
            rank_data = pd.read_html(url)[0]
            china_rank = rank_data[rank_data['球队'] == '中国']['排名'].values.tolist()[0]
            rank.append([d, china_rank])
        except:
            continue
    return rank


if __name__ == '__main__':
    rank = get_rank('2017-01')
    print(rank)