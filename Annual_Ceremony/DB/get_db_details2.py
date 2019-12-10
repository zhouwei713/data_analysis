# coding = utf-8
"""
@author: zhou
@time:2019/12/4 16:40
@File: get_db_details.py
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import js2xml
import time
from datetime import timedelta
import datetime
from collections import OrderedDict
import os


def get_db_data():
    url = 'https://db-engines.com/en/ranking_trend/'
    res = requests.get(url)
    content = BeautifulSoup(res.text, "html.parser")
    db_data = content.find_all("script")[2].string
    src_text = js2xml.parse(db_data)
    src_tree = js2xml.pretty_print(src_text)
    data_tree = BeautifulSoup(src_tree, 'html.parser')
    year = data_tree.find_all('number')[:2]
    year_list = []
    for y in year:
        year_list.append(y['value'])

    # date_list = gen_time('%s-%s' % (year_list[0], str(int(year_list[1]) + 1)))

    for i in data_tree.find_all('object'):
        date_list = gen_time('%s-%s' % (year_list[0], str(int(year_list[1]) + 1)))
        data = []
        tmp_list = []
        db_name = i.find('string')
        if i.find('null'):
            null_num = len(i.find_all('null'))
            tmp_list = list(zip(date_list[:null_num], ['0' for i in range(null_num + 1)]))
            date_list = date_list[null_num:]
        for j in i.find_all('number'):
            data.append(j['value'])

        date_value_tmp = list(zip(date_list, data))
        date_value = tmp_list + date_value_tmp
        d_data = zip([db_name.string for i in range(len(date_value))], date_value)
        save_data(d_data)


def save_data(data):
    print('save to json file')
    if not os.path.exists(r'db_data.csv'):
        with open('db_data.csv', 'a+', encoding='utf-8') as f:
            f.write('dbname,date,value\n')
            for d in data:
                try:
                    row = '{},{},{}'.format(d[0],
                                            d[1][0],
                                            d[1][1])
                    f.write(row)
                    f.write('\n')
                except:
                    raise
    else:
        with open('db_data.csv', 'a+', encoding='utf-8') as f:
            for d in data:
                try:
                    row = '{},{},{}'.format(d[0],
                                            d[1][0],
                                            d[1][1])
                    f.write(row)
                    f.write('\n')
                except:
                    raise
    print('save finish!')


def gen_time(datestart, dateend=None):
    if dateend is None:
        dateend = time.strftime('%Y-%m', time.localtime(time.time()))
    datestart=datetime.datetime.strptime(datestart, '%Y-%m')
    dateend=datetime.datetime.strptime(dateend, '%Y-%m')
    date_list = list(OrderedDict(((datestart + timedelta(_)).strftime(r"%Y-%m"), None) for _ in range((dateend - datestart).days)).keys())
    date_list.append('2019-12')
    return date_list


if __name__ == '__main__':
    get_db_data()
