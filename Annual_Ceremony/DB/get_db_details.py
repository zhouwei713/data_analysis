# coding = utf-8
"""
@author: zhou
@time:2019/12/4 16:40
@File: get_db_details.py
"""

import pandas as pd
import asyncio
import aiohttp
import aiofiles
from bs4 import BeautifulSoup
import js2xml
import time
from datetime import timedelta
import datetime
from collections import OrderedDict
import os


async def fetch(session, url):
    async with session.get(url) as response:

        return await response.text()


async def get_db_data(db_name):
    url = 'https://db-engines.com/en/ranking_trend/system/%s' % db_name

    async with aiohttp.ClientSession() as session:
        res = await fetch(session, url)
        content = BeautifulSoup(res, "html.parser")
        content.find_all("script")
        db_data = content.find_all("script")[2].string
        src_text = js2xml.parse(db_data)
        src_tree = js2xml.pretty_print(src_text)
        data_tree = BeautifulSoup(src_tree, 'html.parser')
        data_tree.find_all('number')
        data = []
        for i in data_tree.find_all('number'):
            data.append(i['value'])

        date_list = gen_time('%s-%s' % (data[0], str(int(data[1]) + 1)))
        date_value = list(zip(date_list, data[3:]))
        d_data = zip([db_name for i in range(len(date_value))], date_value)

        await save_data(d_data)


async def save_data(data):
    print('save to json file')
    if not os.path.exists(r'db_data.csv'):
        async with aiofiles.open('db_data.csv', 'a+', encoding='utf-8') as f:
            await f.write('dbname,date,value\n')
            for d in data:
                try:
                    row = '{},{},{}'.format(d[0],
                                            d[1][0],
                                            d[1][1])
                    await f.write(row)
                    await f.write('\n')
                except:
                    continue
    else:
        async with aiofiles.open('db_data.csv', 'a+', encoding='utf-8') as f:
            for d in data:
                try:
                    row = '{},{},{}'.format(d[0],
                                            d[1][0],
                                            d[1][1])
                    await f.write(row)
                    await f.write('\n')
                except:
                    continue
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
    # date_list = gen_time('2012-11')
    db_tb = pd.read_csv('db_tb.csv')
    db_name = db_tb['3'].values.tolist()
    loop = asyncio.get_event_loop()
    tasks = [get_db_data(name) for name in db_name]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
