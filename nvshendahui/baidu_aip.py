# coding = utf-8
"""
@author: zhou
@time:2019/8/5 17:15
@File: baidu_aip.py
"""

from config import API_KEY, APP_ID, SECRET_KEY, log_level
from aip import AipFace
import pandas as pd
import time

f_client = AipFace(APP_ID, API_KEY, SECRET_KEY)

image_type = "URL"

data = pd.read_csv('nvshen.csv', )


def baidu_api():
    nvshen_total = []
    for row in data.itertuples(index=True):
        print("检验", row)
        nvshenlist = [getattr(row, "name"), getattr(row, "picture")]
        image = nvshenlist[1]
        options = {}
        options["face_field"] = "age,beauty"
        f = f_client.detect(image, image_type, options)
        time.sleep(2)
        score = f['result']['face_list'][0]['beauty']
        nvshenlist.append(score)
        nvshen_total.append(nvshenlist)
    with open('nvshen_new.csv', 'w', encoding='utf-8') as f:
        f.write('name,aip_score\n')
        for row in nvshen_total:
            rowcsv = '{},{}'.format(row[0], row[2])
            f.write(rowcsv)
            f.write('\n')


if __name__ == '__main__':
    baidu_api()
