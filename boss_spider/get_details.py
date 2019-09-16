# coding = utf-8
"""
@author: zhou
@time:2019/9/9 10:21
@File: get_details.py
"""

import requests
from bs4 import BeautifulSoup
import config
from pymongo import MongoClient
import time


header = config.header

job_conn = MongoClient("mongodb://%s:%s@ds151612.mlab.com:51612/boss" % ('boss', 'boss123'))
job_db = job_conn.boss
job_collection = job_db.boss

details_collection = job_db.job_details


def run_main():
    jobs = job_collection.find()
    for job in jobs:
        print('获得工作的uri ', job['uri'])
        get_details(job)
        time.sleep(1)


def get_details(items):
    base_url = config.url
    url = base_url + items['uri']
    company_name = items['name']
    try:
        res = requests.get(url, headers=header).text
        content = BeautifulSoup(res, "html.parser")
        text = content.find('div', attrs={'class': 'text'}).text.strip()
        result = {'name': company_name, 'details': text}
        details_collection.insert_one(result)
    except:
        raise


if __name__ == '__main__':
    run_main()


