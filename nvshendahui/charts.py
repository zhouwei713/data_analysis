# coding = utf-8
"""
@author: zhou
@time:2019/8/5 14:46
@File: charts.py
"""

from pyecharts.charts import Bar, WordCloud
from pyecharts import options as opts
import pandas as pd
import os
import random
from PIL import Image
import math


def do_charts():
    nvshen = pd.read_csv('nvshen.csv')
    nvshen.sort_values('weight_score', ascending=False, inplace=True)
    bar = Bar()
    count_top = nvshen['count'][0:10].values.tolist()
    count_bottom = nvshen['count'][-10:-1].values.tolist()
    count = [''.join(list(filter(str.isdigit, i))) for i in count_top] + \
            [''.join(list(filter(str.isdigit, i))) for i in count_bottom]
    name_top = nvshen['name'][0:10]
    name_bottom = nvshen['name'][-10:-1]
    name = name_top.values.tolist() + name_bottom.values.tolist()
    score_top = nvshen["weight_score"][0:10]
    score_bottom = nvshen["weight_score"][-10:-1]
    score = score_top.values.tolist() + score_bottom.values.tolist()
    bar.add_xaxis(name)
    bar.add_yaxis("女神得分/百分制", score, gap="0%")
    bar.add_yaxis("打分人数/万", count, gap="0%")
    bar.set_global_opts(title_opts=opts.TitleOpts(title="女神大会", subtitle="女神大排名-top10"),
                        datazoom_opts=opts.DataZoomOpts(is_show=True, orient="vertical"),
                        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
                        toolbox_opts=opts.ToolboxOpts())
    bar.render('女神大排名-top10.html')

    word_name = nvshen['name'].values.tolist()
    word_value = nvshen["weight_score"].values.tolist()
    words = [i for i in zip(word_name, word_value)]
    wordcloud = WordCloud()
    wordcloud.add("", words, word_size_range=[10, 40], shape='circle')
    wordcloud.render("女神词云.html")


def do_baidu_charts():
    nvshen = pd.read_csv('nvshen_new.csv')
    nvshen.sort_values('aip_score', ascending=False, inplace=True)
    bar = Bar()
    name_top = nvshen['name'][0:10]
    name_bottom = nvshen['name'][-10:-1]
    name = name_top.values.tolist() + name_bottom.values.tolist()
    score_top = nvshen["aip_score"][0:10]
    score_bottom = nvshen["aip_score"][-10:-1]
    score = score_top.values.tolist() + score_bottom.values.tolist()
    bar.add_xaxis(name)
    bar.add_yaxis("女神新得分/百分制", score)
    bar.set_global_opts(datazoom_opts=opts.DataZoomOpts(is_show=True, orient="vertical"),
                        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
                        toolbox_opts=opts.ToolboxOpts())
    bar.render('女神新排名.html')


def pic_wall():
    x = 0
    y = 0
    imgs = os.listdir("picture")
    random.shuffle(imgs)
    # 创建640*640的图片用于填充各小图片
    newImg = Image.new('RGBA', (2048, 2048))
    # 以640*640来拼接图片，math.sqrt()开平方根计算每张小图片的宽高，
    width = int(math.sqrt(2048 * 2048 / len(imgs)))
    # 每行图片数
    numLine = int(2048 / width)

    for i in imgs:
        if not i.endswith('jpg'):
            continue
        img = Image.open("picture/" + i)
        # 缩小图片
        img = img.resize((width, width), Image.ANTIALIAS)
        # 拼接图片，一行排满，换行拼接
        newImg.paste(img, (x * width, y * width))
        x += 1
        if x >= numLine:
            x = 0
            y += 1
    newImg.save("all.png")


if __name__ == '__main__':
    pic_wall()
    do_charts()
    do_baidu_charts()

