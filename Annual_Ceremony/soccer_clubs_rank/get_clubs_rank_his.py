# coding = utf-8
"""
@author: zhou
@time:2020/1/13 10:42
@File: get_clubs_rank_his.py
"""


import requests
from bs4 import BeautifulSoup
import js2xml
import os


month_map = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5,
             'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10,
             'November': 11, 'December': 12}


def get_clubs_rank_his(data_list):
    base_url = 'https://footballdatabase.com'
    his_rank_list = []
    for data in data_list:
        print(data)
        url = data[0][3]
        his_res = requests.get(base_url + url)
        his_content = BeautifulSoup(his_res.text, "html.parser")
        js = his_content.find_all('script')[1].string
        src_text = js2xml.parse(js)
        src_tree = js2xml.pretty_print(src_text)
        data_tree = BeautifulSoup(src_tree, 'html.parser')
        array_list = data_tree.find_all('array')
        club_name = data[0][1]
        for array in array_list[2:-2]:
            his_rank_list = []
            array_date = array.find('string').text
            date = array_date
            try:
                month = month_map[array_date.split(' ')[0]]
                year = array_date.split(' ')[1]
                date = str(year) + '-' + str(month)
            except:
                pass
            array_data = array.find_all('number')
            try:
                point = array_data[0]['value']
                rank = array_data[1]['value']
                his_rank_list.append([rank, point, date])
                save_his_data(club_name, his_rank_list)
            except:
                raise
    return his_rank_list


def save_his_data(name, data):
    if not os.path.exists(r'rank_his_data.csv'):
        with open('rank_his_data.csv', 'a+', encoding='utf-8') as f:
            f.write('name,rank,point,date\n')
            for d in data:
                try:
                    row = '{},{},{},{}'.format(name, d[0], d[1], d[2])
                    f.write(row)
                    f.write('\n')
                except:
                    raise
    else:
        with open('rank_his_data.csv', 'a+', encoding='utf-8') as f:
            for d in data:
                try:
                    row = '{},{},{},{}'.format(name, d[0], d[1], d[2])
                    f.write(row)
                    f.write('\n')
                except:
                    raise

