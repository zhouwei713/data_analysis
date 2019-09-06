# coding = utf-8
"""
@author: zhou
@time:2019/9/5 14:36
@File: main.py
"""

import requests
from bs4 import BeautifulSoup
import time
import os


def get_data(name, city, code):
    print("正在下载城市%s的数据" % city)
    url = 'http://www.weather.com.cn/weather15d/%s.shtml' % code[2:]
    res = requests.get(url).content.decode()
    content = BeautifulSoup(res, "html.parser")
    weather_list = content.find('ul', attrs={'class': 't clearfix'}).find_all('li')
    items = map(parse_item, weather_list)
    save_to_csv(name, city, items)
    time.sleep(1)


def parse_item(item):
    time = item.find('span', attrs={'class': 'time'}).text
    wea = item.find('span', attrs={'class': 'wea'}).text
    tem = item.find('span', attrs={'class': 'tem'}).text
    wind = item.find('span', attrs={'class': 'wind'}).text
    wind_level = item.find('span', attrs={'class': 'wind1'}).text
    result = {
        "time": time,
        "wea": wea,
        "tem": tem,
        "wind": wind,
        "wind_level": wind_level
    }
    return result


def save_to_csv(name, city, data):
    if not os.path.exists('%s_data.csv' % name):
        with open('%s_data.csv' % name, 'a+', encoding='utf-8') as f:
            f.write('city,time,wea,tem,wind,wind_level\n')
            for d in data:
                try:
                    row = '{},{},{},{},{},{}'.format(city,
                                                     d['time'],
                                                     d['wea'],
                                                     d['tem'],
                                                     d['wind'],
                                                     d['wind_level'])
                    f.write(row)
                    f.write('\n')
                except:
                    continue
    else:
        with open('%s_data.csv' % name, 'a+', encoding='utf-8') as f:
            for d in data:
                try:
                    row = '{},{},{},{},{},{}'.format(city,
                                                     d['time'],
                                                     d['wea'],
                                                     d['tem'],
                                                     d['wind'],
                                                     d['wind_level'])
                    f.write(row)
                    f.write('\n')
                except:
                    continue


if __name__ == '__main__':
    import pandas as pd
    provincial = pd.read_csv('provincial_capital')
    china_city_code = pd.read_csv('china-city-list.csv')
    china_scenic_code = pd.read_csv('china-scenic-list.txt', sep='\t')
    china_scenic_code.columns = ['ID', 'name', 'area', 'provincial']
    attraction = pd.read_csv('attractions')
    provincial_data = pd.DataFrame()
    attraction_data = pd.DataFrame()

    # 省会抓取
    for i in provincial['city'].values.tolist():
        for j in china_city_code['City_CN'].values.tolist():
            if j == i:
                provincial_data = pd.concat([china_city_code[china_city_code['City_CN'] == j], provincial_data])

    for city in provincial_data['City_CN'].values.tolist():
        city_id = provincial_data[provincial_data['City_CN'] == city]['City_ID'].values.tolist()[0]
        get_data('weather', city, city_id)

    # 景点抓取
    for a in attraction['attractions'].values.tolist():
        for c in china_scenic_code['name'].values.tolist():
            if c == a:
                attraction_data = pd.concat([china_scenic_code[china_scenic_code['name'] == c], attraction_data])

    for attrac in attraction_data['name'].values.tolist():
        city_id = attraction_data[attraction_data['name'] == attrac]['ID'].values.tolist()[0]
        get_data('attraction', attrac, city_id)
