# coding = utf-8
"""
@author: zhou
@time:2019/9/16 11:12
@File: get_data.py
"""

import requests
import time


url_list = [
    'https://events.sports.sina.com.cn/bps/peony/mersh/beitai/fiba/stats/playerdata_order?leagueid=433&ordertype=PointsAverage',
    'https://events.sports.sina.com.cn/bps/peony/mersh/beitai/fiba/stats/playerdata_order?leagueid=433&ordertype=ReboundsAverage',
    'https://events.sports.sina.com.cn/bps/peony/mersh/beitai/fiba/stats/playerdata_order?leagueid=433&ordertype=PlusMinusAverage',
    'https://events.sports.sina.com.cn/bps/peony/mersh/beitai/fiba/stats/playerdata_order?leagueid=433&ordertype=StealsAverage',
    'https://events.sports.sina.com.cn/bps/peony/mersh/beitai/fiba/stats/playerdata_order?leagueid=433&ordertype=AssistsAverage',
    'https://events.sports.sina.com.cn/bps/peony/mersh/beitai/fiba/stats/playerdata_order?leagueid=433&ordertype=BlockedAverage',
    'https://events.sports.sina.com.cn/bps/peony/mersh/beitai/fiba/stats/playerdata_order?leagueid=433&ordertype=TurnoversAverage',
    'https://events.sports.sina.com.cn/bps/peony/mersh/beitai/fiba/stats/playerdata_order?leagueid=433&ordertype=PersonalFoulsAverage',
    'https://events.sports.sina.com.cn/bps/peony/mersh/beitai/fiba/stats/playerdata_order?leagueid=433&ordertype=FieldGoalsAverage'
]


def fire(url):
    file_name = url.split('=')[2]
    res = requests.get(url).json()
    data = res['playerdata_order']
    items = map(get_data, data)
    print('save data')
    save_to_csv(items, file_name)


def get_data(data):
    name = data['CNAlias']
    country = data['TeamCNName']
    points = data['PointsAverage']
    rebounds = data['ReboundsAverage']
    steals = data['StealsAverage']
    assists = data['AssistsAverage']
    fouls = data['PersonalFoulsAverage']
    plus_minus = data['PlusMinusAverage']
    blocked = data['BlockedAverage']
    goals_percentage = data['FieldGoalsPercentage_m']
    turnovers = data['TurnoversAverage']
    result = {
        'name': name,
        'country': country,
        'points': points,
        'rebounds': rebounds,
        'steals': steals,
        'assists': assists,
        'fouls': fouls,
        'plus_minus': plus_minus,
        'blocked': blocked,
        'goals_percentage': goals_percentage,
        'turnovers': turnovers
    }
    return result


def save_to_csv(data, file_name):
    with open(file_name + '_data.csv', 'w', encoding='utf-8') as f:
        f.write('name,country,points,rebounds,steals,assists,fouls,plus_minus,blocked,goals_percentage,turnovers\n')
        for d in data:
            try:
                row = '{},{},{},{},{},{},{},{},{},{},{}'.format(d['name'],
                                                                d['country'],
                                                                d['points'],
                                                                d['rebounds'],
                                                                d['steals'],
                                                                d['assists'],
                                                                d['fouls'],
                                                                d['plus_minus'],
                                                                d['blocked'],
                                                                d['goals_percentage'],
                                                                d['turnovers'])
                f.write(row)
                f.write('\n')
            except:
                continue


if __name__ == '__main__':
    for url in url_list:
        fire(url)
        time.sleep(2)
