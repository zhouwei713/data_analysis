# coding = utf-8
"""
@author: zhou
@time:2019/10/24 13:51
@File: test.py
"""
from pymongo import MongoClient


conn = MongoClient("mongodb://%s:%s@ds339348.mlab.com:39348/boss_job_details" % ('boss', 'Boss123'))
db = conn.boss_job_details
print(db)
py_collection = db.py_job
# print(py_collection)
job_list = [{
    'a': 123,
    'b': 345
},
    {
        'k': 3333,
        'j': 456
    }]
py_collection.insert_many(job_list)
