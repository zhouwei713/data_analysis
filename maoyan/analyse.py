# coding = utf-8
"""
@author: zhou
@time:2019/8/29 18:44
@File: analyse.py
"""

from pyecharts.charts import Pie
from pyecharts import options as opts
import pandas as pd
from wordcloud import WordCloud
import jieba
from PIL import Image
import numpy as np

font = r'C:\Windows\Fonts\FZSTK.TTF'
# STOPWORDS = set(map(str.strip, open('stopwords.txt', encoding='utf-8').readlines()))


def comment_wordcloud(data):
    df_list = data['content'].tolist()
    cut_word = "".join(jieba.cut(str(df_list), cut_all=False))
    img = Image.open('ciyun.jpg')
    img_array = np.array(img)
    wc = WordCloud(width=1800, height=1500, background_color='white', font_path=font, mask=img_array)
    wc.generate(cut_word)
    wc.to_file('word.png')


def get_data():
    data = pd.read_csv('maoyan_data.csv', encoding='utf-8')
    return data


def gender_pie(data):
    gender_list = []
    for i, j in enumerate(data['gender'].value_counts()):
        if i == 0:
            i = '未知'
        elif i == 1:
            i = '男'
        else:
            i = '女'
        gender_list.append([i, j])
    pie = Pie()
    pie.add("", gender_list)
    pie.set_global_opts(title_opts=opts.TitleOpts(title="性别分布"))
    pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    pie.render("性别分布.html")


def level_pie(data):
    level_list = [[i, j] for i, j in enumerate(data['userlevel'].value_counts())]
    pie = Pie()
    pie.add("", level_list, radius=["40%", "75%"])
    pie.set_global_opts(
        title_opts=opts.TitleOpts(title="等级分布"),
        legend_opts=opts.LegendOpts(
            orient="vertical", pos_top="15%", pos_left="2%"
        ))
    pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    pie.render("等级分布.html")


def score_pie(data):
    score_list = []
    for i, j in enumerate(data['score'].value_counts()):
        if i == 0:
            i = '0分'  # 当数据项名称为0时，不在图表中展示，这个疑为 echarts 的 bug
        score_list.append([i, j])
    pie = Pie()
    pie.add("", score_list, radius=["30%", "75%"], center=["50%", "50%"], rosetype="radius")
    pie.set_global_opts(
        title_opts=opts.TitleOpts(title="评分分布"),
        legend_opts=opts.LegendOpts(
            orient="vertical", pos_left="10%"
        ))
    pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{c}:{d}%"))
    pie.render("评分分布.html")


if __name__ == '__main__':
    data = get_data()
    # gender_pie(data)
    comment_wordcloud(data)

