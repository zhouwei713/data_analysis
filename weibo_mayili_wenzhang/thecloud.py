# coding = utf-8
"""
@author: zhou
@time:2019/7/29 15:08
@File: thecloud.py
"""

import jieba
import pandas as pd
from wordcloud import WordCloud
import numpy as np


font = r'C:\Windows\Fonts\FZSTK.TTF'
STOPWORDS = {"回复", }


def wordcloud_m():
    df = pd.read_csv('mayili.csv', usecols=[1])
    df_copy = df.copy()
    df_copy['mayili_comment'] = df_copy['mayili_comment'].apply(lambda x: str(x).split())  # 去掉空格
    df_list = df_copy.values.tolist()
    comment = jieba.cut(str(df_list), cut_all=False)
    words = ' '.join(comment)
    wc = WordCloud(width=2000, height=1800, background_color='white', font_path=font,
                   stopwords=STOPWORDS, contour_width=3, contour_color='steelblue')
    wc.generate(words)
    wc.to_file('m.png')


def wordcloud_w():
    df = pd.read_csv('wenzhang.csv', usecols=[1])
    df_copy = df.copy()
    df_copy['wenzhang_comment'] = df_copy['wenzhang_comment'].apply(lambda x: str(x).split())  # 去掉空格
    df_list = df_copy.values.tolist()
    comment = jieba.cut(str(df_list), cut_all=False)
    words = ' '.join(comment)
    wc = WordCloud(width=2000, height=1800, background_color='white', font_path=font,
                   stopwords=STOPWORDS, contour_width=3, contour_color='steelblue')
    wc.generate(words)
    wc.to_file('w.png')


if __name__ == '__main__':
    wordcloud_m()
    wordcloud_w()

