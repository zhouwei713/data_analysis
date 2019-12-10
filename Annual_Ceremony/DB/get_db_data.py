# coding = utf-8
"""
@author: zhou
@time:2019/12/4 15:29
@File: get_db_data.py
"""

import pandas as pd


mystr = ' Detailed vendor-provided information available'


def set_column3(column3):
    if mystr in column3:
        column3 = column3.split(mystr)[0]
    return column3


url = 'https://db-engines.com/en/ranking'
tb = pd.read_html(url)
db_tb = tb[3].drop(index=[0, 1, 2])[[0, 1, 2, 3, 4, 5, 6, 7]]

# 处理数据
db_tb[3] = db_tb[3].apply(set_column3)

# 保存数据
db_tb.to_csv('db_tb.csv')
