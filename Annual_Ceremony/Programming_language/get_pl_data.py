# coding = utf-8
"""
@author: zhou
@time:2019/12/16 18:57
@File: get_pl_data.py
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import js2xml
import os
import time


def get_pl_list():
    url = 'https://www.tiobe.com/tiobe-index/'
    pl_df = pd.read_html(url)
    top_20 = pl_df[0]['Programming Language'].values.tolist()
    bottom_30 = pl_df[1]['Programming Language'].values.tolist()
    return top_20 + bottom_30


def get_pl_data(name):
    name_lower = [i.lower() for i in name]
    for i in name_lower:
        print("Request ", i)
        if i == 'c#':
            i = 'csharp'
        if i == 'pl/sql':
            i = 'pl-sql'
        if i == 'visual basic .net':
            i = 'visual-basic-dotnet'
        if i == 'delphi/object pascal':
            i = 'delphi-object-pascal'
        if i == 'assembly language':
            i = 'assembly-language'
        if i == 'visual basic':
            i = 'visual-basic'
        if i == 'c++':
            i = 'cplusplus'
        url = 'https://www.tiobe.com/tiobe-index/' + i
        res = requests.get(url).text
        content = BeautifulSoup(res, "html.parser")
        js = content.find_all('script')[9].string
        src_text = js2xml.parse(js)
        src_tree = js2xml.pretty_print(src_text)
        data_tree = BeautifulSoup(src_tree, 'html.parser')
        array_list = data_tree.find_all('array')
        data_list = []
        for array in array_list[3:]:
            array_data = array.find_all('number')
            data_list.append({'date': array_data[0]['value'] + '-' + str(int(array_data[1]['value']) + 1) + '-' + array_data[2]['value'],
                              'value': array_data[3]['value']})

        if i == 'csharp':
            i = 'c#'
        if i == 'pl-sql':
            i = 'pl/sql'
        if i == 'cplusplus':
            i = 'c++'
        save_data(i, data_list)
        time.sleep(2)


def save_data(name, data):
    print('save to pl file')
    if not os.path.exists(r'pl_data.csv'):
        with open('pl_data.csv', 'a+', encoding='utf-8') as f:
            f.write('name,value,date\n')
            for d in data:
                try:
                    row = '{},{},{}'.format(name,
                                            d['value'],
                                            d['date'])
                    f.write(row)
                    f.write('\n')
                except:
                    raise
    else:
        with open('pl_data.csv', 'a+', encoding='utf-8') as f:
            for d in data:
                try:
                    row = '{},{},{}'.format(name,
                                            d['value'],
                                            d['date'])
                    f.write(row)
                    f.write('\n')
                except:
                    raise
    print('save finish!')


if __name__ == '__main__':
    pl_list = get_pl_list()
    get_pl_data(pl_list)
