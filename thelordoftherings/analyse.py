# coding = utf-8
"""
@author: zhou
@time:2019/8/29 18:44
@File: analyse.py
"""

import pandas as pd
from wordcloud import WordCloud
import jieba
from PIL import Image
import numpy as np

from pyecharts.charts import Bar,Map,Line,Page,Scatter, Pie
from pyecharts import options as opts
from pyecharts.globals import SymbolType,ThemeType
from pyecharts.charts import Grid

font = r'C:\Windows\Fonts\FZSTK.TTF'
# STOPWORDS = set(map(str.strip, open('stopwords.txt', encoding='utf-8').readlines()))


def comment_wordcloud(data, num):
    df_list = data['content'].tolist()
    cut_word = "".join(jieba.cut(str(df_list), cut_all=False))
    img = Image.open('ciyun.jpg')
    img_array = np.array(img)
    wc = WordCloud(width=1800, height=1500, background_color='white', font_path=font, mask=img_array)
    wc.generate(cut_word)
    wc.to_file('word%s.png' % str(num))


def get_data(num):
    data = pd.read_csv('maoyan_data_rings%s.csv' % str(num), encoding='utf-8')
    return data


def gender_pie(data, num):
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
    pie.render("性别分布%s.html" % str(num))


def level_pie(data, num):
    level_list = [[i, j] for i, j in enumerate(data['userlevel'].value_counts())]
    pie = Pie()
    pie.add("", level_list, radius=["40%", "75%"])
    pie.set_global_opts(
        title_opts=opts.TitleOpts(title="等级分布"),
        legend_opts=opts.LegendOpts(
            orient="vertical", pos_top="15%", pos_left="2%"
        ))
    pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    pie.render("等级分布%s.html" % str(num))


def score_pie(data, num):
    index = data['score'].value_counts().index.tolist()
    values = data['score'].value_counts().values.tolist()
    score_list = list(zip(index, values))

    pie = Pie()
    pie.add("", score_list, radius=["30%", "75%"], center=["50%", "50%"], rosetype="radius")
    pie.set_global_opts(
        title_opts=opts.TitleOpts(title="评分分布"),
        legend_opts=opts.LegendOpts(
            orient="vertical", pos_left="10%"
        ))
    pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{c}:{d}%"))
    pie.render("评分分布%s.html" % str(num))


if __name__ == '__main__':
    data = get_data(1)
    gender_pie(data, 1)
    # comment_wordcloud(data,1)
    score_pie(data, 1)
    level_pie(data, 1)

