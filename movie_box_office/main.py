# coding = utf-8
"""
@author: zhou
@time:2020/1/7 16:07
@File: main.py
"""

import requests
import datetime
import os
import json


def get_box_office(date):
    url = 'http://piaofang.maoyan.com/second-box?beginDate=%s' % date
    res = requests.get(url).json()
    save_to_json(res)
    save_total_to_csv(res)
    if 'list' in res['data']:
        save_movie_to_csv(res)
    return res


def save_to_json(data):
    if not os.path.exists(r'movie_data.json'):
        with open('movie_data.json', 'a+', encoding='utf-8') as f:
            json.dump(data, f)
    else:
        with open('movie_data.json', 'a+', encoding='utf-8') as f:
            json.dump(data, f)


def save_movie_to_csv(data):
    print('save movie to file')
    if not os.path.exists(r'movie_data.csv'):
        with open('movie_data.csv', 'a+', encoding='utf-8') as f:
            f.write('movieId,movieName,boxInfo,sumBoxInfo,avgShowView,boxRate,showInfo,avgSeatView,date\n')
            for d in data['data']['list']:
                try:
                    row = '{},{},{},{},{},{},{},{},{}'.format(d['movieId'],
                                                              d['movieName'],
                                                              d['boxInfo'],
                                                              d['sumBoxInfo'],
                                                              d['avgShowView'],
                                                              d['boxRate'],
                                                              d['showInfo'],
                                                              d['avgSeatView'],
                                                              data['data']['queryDate'])
                    f.write(row)
                    f.write('\n')
                except:
                    raise
    else:
        with open('movie_data.csv', 'a+', encoding='utf-8') as f:
            for d in data['data']['list']:
                try:
                    row = '{},{},{},{},{},{},{},{},{}'.format(d['movieId'],
                                                              d['movieName'],
                                                              d['boxInfo'],
                                                              d['sumBoxInfo'],
                                                              d['avgShowView'],
                                                              d['boxRate'],
                                                              d['showInfo'],
                                                              d['avgSeatView'],
                                                              data['data']['queryDate'])
                    f.write(row)
                    f.write('\n')
                except:
                    raise
    print('save finish!')


def save_total_to_csv(data):
    print('save total to file')
    if not os.path.exists(r'total_data.csv'):
        with open('total_data.csv', 'a+', encoding='utf-8') as f:
            f.write('totalBox,splitTotalBox,queryDate\n')
            try:
                row = '{},{},{}'.format(data['data']['totalBox'],
                                        data['data']['splitTotalBox'],
                                        data['data']['queryDate'])
                f.write(row)
                f.write('\n')
            except:
                raise
    else:
        with open('total_data.csv', 'a+', encoding='utf-8') as f:
            try:
                row = '{},{},{}'.format(data['data']['totalBox'],
                                        data['data']['splitTotalBox'],
                                        data['data']['queryDate'])
                f.write(row)
                f.write('\n')
            except:
                raise
    print('save finish!')


def getday(begin_date, end_date):
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y%m%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_list


if __name__ == '__main__':
    days = getday('2019-01-01', '2019-12-31')
    for day in days:
        get_box_office(day)