# coding = utf-8
"""
@author: zhou
@time:2019/12/4 16:40
@File: get_db_details.py
"""

import requests
from bs4 import BeautifulSoup
import js2xml


def get_db_data(db_type):
    url = 'https://db-engines.com/en/ranking_trend/%s' % db_type
    res = requests.get(url)
    content = BeautifulSoup(res.text, "html.parser")
    db_data = content.find_all("script")[2].string
    src_text = js2xml.parse(db_data)
    src_tree = js2xml.pretty_print(src_text)
    data_tree = BeautifulSoup(src_tree, 'html.parser')
    db_name = data_tree.find_all('string')
    print(db_name)
    name_list = []
    for i in db_name:
        name_list.append(i.string)

    save_data(db_type, name_list)


def save_data(db_type, data):
    print('save to json file')
    with open('%s_data.csv' % db_type, 'w', encoding='utf-8') as f:
        f.write('dbname\n')
        for d in data[:-3]:
            try:
                row = '{}'.format(d)
                f.write(row)
                f.write('\n')
            except:
                raise
    print('save finish!')


if __name__ == '__main__':
    db_type = ['relational+dbms', 'key-value+store', 'document+store', 'graph+dbms', 'time+series+dbms', 'search+engine']
    for i in db_type:
        get_db_data(i)
