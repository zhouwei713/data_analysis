# -*- coding: UTF-8 -*-

import requests
from urllib.parse import unquote
import pandas as pd
import time
import os
import json

session = requests.session()
page = 1500
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'Origin': 'https://jobs.bytedance.com',
    'Referer': f'https://jobs.bytedance.com/experienced/position?keywords=&category=&location=&project=&type=&job_hot_flag=&current=1&limit={page}'
}
data = {
    "portal_entrance": 1
}
url = "https://jobs.bytedance.com/api/v1/csrf/token"
r = session.post(url, headers=headers, data=data)
cookies = session.cookies.get_dict()

url = "https://jobs.bytedance.com/api/v1/search/job/posts"
headers["x-csrf-token"] = unquote(cookies["atsx-csrf-token"])
data = {
    "job_category_id_list": [],
    "keyword": "",
    "limit": page,
    "location_code_list": [],
    "offset": 0,
    "portal_entrance": 1,
    "portal_type": 2,
    "recruitment_id_list": [],
    "subject_id_list": []
}
for i in range(11):
    print(f"准备爬取第{i}页")
    data["offset"] = i*page
    r = None
    while not r:
        try:
            r = session.post(url, headers=headers,
                             data=json.dumps(data), timeout=3)
        except Exception as e:
            print("访问超时！等待5s", e)
            time.sleep(5)
    df = pd.DataFrame(r.json()['data']['job_post_list'])
    if df.shape[0] == 0:
        print("爬取完毕！！！")
        break
    df.city_info = df.city_info.str['name']
    df.recruit_type = df.recruit_type.str['parent'].str['name']
    tmp = []
    for x in df.job_category.values:
        if x['parent']:
            tmp.append(f"{x['parent']['name']}-{x['name']}")
        else:
            tmp.append(x['name'])
    df.job_category = tmp
    df.publish_time = df.publish_time.apply(
        lambda x: pd.Timestamp(x, unit="ms"))
    df.drop(columns=['sub_title', 'job_hot_flag', 'job_subject'], inplace=True)
    df.to_csv("bytedance_jobs.csv", mode="a", header=not os.path.exists("bytedance_jobs.csv"), index=False)
    print(",".join(df.title.head(10)))
# 对结果去重
df = pd.read_csv("bytedance_jobs.csv")
df.drop_duplicates(inplace=True)
df.to_csv("bytedance_jobs.csv", index=False)
print("共爬取", df.shape[0], "行无重复数据")
