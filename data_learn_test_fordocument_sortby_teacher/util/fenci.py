# coding = utf-8
"""
@author: zhou
@time:2019/2/1 11:00
"""


import jieba
import os

text = r'..\text_classification-master\text classification\train\女性\1.txt'
d = r'.\text_classification-master\text classification\stop'
txt = os.path.join(d, 'stopword.txt')


def seg_text(text):
    stop = [line.strip() for line in open(txt, encoding='utf-8').readlines()]
    text_segd = jieba.cut(text.strip())
    seg_list = []
    for word in text_segd:
        if word not in stop:
            newstr = ' '.join(word)
            seg_list.append(newstr)
    return seg_list


if __name__ == "__main__":
    text = open(text, encoding='gb18030').read()
    s = seg_text(text)
    print(s)
