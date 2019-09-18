# coding = utf-8
"""
@author: zhou
@time:2019/9/18 10:19
@File: analyse.py
"""

import jieba
from pyecharts.globals import SymbolType
from pyecharts.charts import Bar, WordCloud
import jieba.posseg as pseg
import pandas as pd
import re
from collections import Counter


df = pd.read_csv("Jay_comment_data.csv")
thecomment = df['comment'].values.tolist()

word_dict = {}
for line in thecomment:
    words = jieba.cut(line)
    for w in words:
        if w not in word_dict:
            word_dict[w] = 1
        else:
            word_dict[w] += 1

stop = pd.read_csv("Chinese_Stopwords.txt", encoding='utf-8', header=None)
stop.columns = ['word']
stop = [' '] + list(stop.word)

for i in range(len(stop)):
    if stop[i] in word_dict:
        word_dict.pop(stop[i])
word_dict_sort = sorted(word_dict.items(), key=lambda x:x[1])
words = word_dict_sort[-100:]

wordcloud = WordCloud()
wordcloud.add("", words, word_size_range=[20, 100], shape='circle')
wordcloud.render_notebook()


def speech_cut(speech):
    word_list = []
    for word in word_dict_sort:
        words = pseg.cut(word[0])
        for w, flag in words:
            if flag == speech:
                word_list.append(word)
    return word_list


verb_word = speech_cut('v')
wordcloud = WordCloud()
wordcloud.add("", verb_word[-100:], word_size_range=[20, 100], shape='circle')
wordcloud.render_notebook()

noun_word = speech_cut('n')
wordcloud = WordCloud()
wordcloud.add("", noun_word[-100:], word_size_range=[20, 100], shape='circle')
wordcloud.render_notebook()


# 表情分析
def get_emoji(content):
    pattern = re.compile(u"[\U00010000-\U0010ffff]")
    result = re.findall(pattern, content)
    return result


df['emojis_list'] = df['comment'].apply(get_emoji)
emojis = df['emojis_list'].values.tolist()

emojis_list = sum(emojis, [])
counter = Counter(emojis_list)
y_emojis, x_counts = zip(*counter.most_common())
bar = Bar()
bar.add_xaxis(y_emojis[:20])
bar.add_yaxis("", x_counts[:20])
bar.render_notebook()

