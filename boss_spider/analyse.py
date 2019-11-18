# coding = utf-8
"""
@author: zhou
@time:2019/10/11 15:40
@File: analyse.py
"""

from pymongo import MongoClient
import pandas as pd
from pyecharts.charts import Bar
from pyecharts import options as opts
from wordcloud import WordCloud
import jieba
from PIL import Image
import numpy as np


job_conn = MongoClient("mongodb://%s:%s@ds151612.mlab.com:51612/boss" % ('boss', 'boss123'))
job_db = job_conn.boss
job_collection = job_db.boss
details_collection = job_db.job_details

job = pd.DataFrame(list(job_collection.find()))
job.to_csv("job.csv", encoding='utf-8')

job_detail = pd.DataFrame(list(details_collection.find()))
job_detail.to_csv('job_detail.csv', encoding='utf-8')

# 薪资水平
salary_distribute = job['salary'].value_counts()
bar = Bar()
bar.add_xaxis(salary_distribute.index.values.tolist()[:10])
bar.add_yaxis("", salary_distribute.values.tolist()[:10])
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
    title_opts=opts.TitleOpts(title="薪资分布", subtitle="薪资分布前10"),
)
bar.render_notebook()

# 高薪企业
height_salary = job[job['salary'] == '30-60K']
height_salary_year_edu = height_salary[['name', 'salary', 'year', 'edu']]

# 职位要求
height_salary_index = height_salary.index.values.tolist()
details = []
for index in height_salary_index:
    detail = job_detail[job_detail.index == index]['details']
    details.append(detail.values.tolist()[0])
print(details)


# 词云
stopworld = ('职位', '描述', '岗位职责', '岗位', '任职', '要求', '分项')
font = r'C:\Windows\Fonts\FZSTK.TTF'
def gen_wordcloud(data, pic, world_pic):
    tmpstr = ''
    for i in range(len(data) - 1):
        tmpstr += data[i]
    pseg = jieba.lcut(tmpstr)
    cut_word = ''
    for i in pseg:
        if i not in stopworld:
            cut_word += i
    img = Image.open(pic)
    img_array = np.array(img)
    wc = WordCloud(width=1800, height=1500, background_color='white', font_path=font, mask=img_array)
    wc.generate(cut_word)
    wc.to_file(world_pic)


gen_wordcloud(details, 'money.jpg', 'money_wc.png')

# 工作年限
year_distribute = job['year'].value_counts()
bar = Bar()
bar.add_xaxis(year_distribute.index.values.tolist()[:10])
bar.add_yaxis("", year_distribute.values.tolist()[:10])
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
    title_opts=opts.TitleOpts(title="工龄分布"),
    # datazoom_opts=opts.DataZoomOpts(),
)
bar.render_notebook()

# 学历要求
edu_distribute = job['edu'].value_counts()
bar = Bar()
bar.add_xaxis(edu_distribute.index.values.tolist()[:10])
bar.add_yaxis("", edu_distribute.values.tolist()[:10])
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
    title_opts=opts.TitleOpts(title="学历分布"),
    # datazoom_opts=opts.DataZoomOpts(),
)
bar.render_notebook()


# 招生硕士企业
height_edu = job[job['edu'] == '硕士']
height_edu = height_edu[['name', 'salary', 'year', 'edu']]

# 所有工作描述词云
all_job_detail = job_detail['details'].values.tolist()
gen_wordcloud(all_job_detail, 'job.jpg', 'fulljob_wc.png')
