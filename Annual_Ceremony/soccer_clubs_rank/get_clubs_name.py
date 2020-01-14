# coding = utf-8
"""
@author: zhou
@time:2020/1/13 10:10
@File: get_clubs_name.py
"""

import requests
from bs4 import BeautifulSoup
import os


def get_clubs_name(url):
    res = requests.get(url)
    content = BeautifulSoup(res.text, 'html.parser')
    name_table = content.find('tbody')
    name_list = name_table.find_all('tr')
    list_rank = []
    for name in name_list:
        rank_list = []
        try:
            rank_point = name.find_all('td', attrs={'class': 'rank'})
            rank = rank_point[0].text
            point = rank_point[1].text
            club_info = name.find('td', attrs={'class': 'club text-left'}).find_all('a')
            club_url = club_info[0]['href']
            club_name = club_info[0].find('div', attrs={'class': 'limittext'}).text
            club_country_url = club_info[1]['href']
            club_country_name = club_info[1].text
            rank_list.append([rank, club_name, club_country_name, club_url, club_country_url, point])
            list_rank.append(rank_list)
            save_club_name(rank_list)

        except:
            pass
    return list_rank


def save_club_name(data):
    if not os.path.exists(r'club_data.csv'):
        with open('club_data.csv', 'a+', encoding='utf-8') as f:
            f.write('rank,club_name,club_country_name,club_url,club_country_url,point\n')
            for d in data:
                try:
                    row = '{},{},{},{},{},{}'.format(d[0], d[1], d[2], d[3], d[4], d[5])
                    f.write(row)
                    f.write('\n')
                except:
                    raise
    else:
        with open('club_data.csv', 'a+', encoding='utf-8') as f:
            for d in data:
                try:
                    row = '{},{},{},{},{},{}'.format(d[0], d[1], d[2], d[3], d[4], d[5])
                    f.write(row)
                    f.write('\n')
                except:
                    raise

