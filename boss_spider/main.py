# coding = utf-8
"""
@author: zhou
@time:2019/8/24 14:51
@File: main.py
"""

import requests
from bs4 import BeautifulSoup
import config
import re
from pymongo import MongoClient
import time


header = config.header

rege = r'<p>([\u4e00-\u9fa5 ]+)<em class="vline"></em>([\d+-年]+|[\u4e00-\u9fa5]+)<em class="vline"></em>([\u4e00-\u9fa5]+)'

conn = MongoClient("mongodb://%s:%s@ds151612.mlab.com:51612/boss" % ('boss', 'boss123'))
db = conn.boss
mongo_collection = db.boss


def jobs(page):

    for i in range(1, page + 1):
        job_list = []
        try:
            print("正在抓取第 %s 页数据" % i)
            uri = '/c101010100/?query=python&page=%s' % i
            res = requests.get(config.url + uri, headers=header).text
            content = BeautifulSoup(res, "html.parser")
            ul = content.find_all('ul')
            jobs = ul[12].find_all("li")
            for job in jobs:
                job_dict = {}
                job_details_uri = job.find('h3', attrs={'class': 'name'}).find('a')['href']
                job_company = job.find('div', attrs={'class': 'company-text'}).find('h3', attrs={'class': 'name'}).find(
                    'a').text
                job_salary = job.find('h3', attrs={'class': 'name'}).find('span', attrs={'class': 'red'}).text
                job_details = str(job.find('p'))
                job_rege = re.match(rege, job_details)
                job_dict['name'] = job_company
                job_dict['uri'] = job_details_uri
                job_dict['salary'] = job_salary
                try:
                    job_dict['site'] = job_rege.group(1)
                    job_dict['year'] = job_rege.group(2)
                    job_dict['edu'] = job_rege.group(3)
                except:
                    continue
                job_list.append(job_dict)
            print(job_list)

            # save to mongoDB
            try:
                mongo_collection.insert_many(job_list)
            except:
                continue
            time.sleep(1)
        except:
            continue


if __name__ == '__main__':
    jobs(10)


