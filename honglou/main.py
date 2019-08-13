# coding = utf-8
"""
@author: zhou
@time:2019/8/12 16:51
@File: main.py
"""

import pandas as pd
from pyecharts.charts import Graph
from pyecharts import options as opts
import jieba
import jieba.posseg as pseg


def deal_data():
    with open("红楼梦.txt", encoding='gb18030') as f:
        honglou = f.readlines()
    jieba.load_userdict("renwu_forcut")
    renwu_data = pd.read_csv("renwu_forcut", header=-1)
    mylist = [k[0].split(" ")[0] for k in renwu_data.values.tolist()]
    tmpNames = []
    names = {}
    relationships = {}
    for h in honglou:
        h.replace("贾妃", "元春")
        h.replace("李宫裁", "李纨")
        poss = pseg.cut(h)
        tmpNames.append([])
        for w in poss:
            if w.flag != 'nr' or len(w.word) != 2 or w.word not in mylist:
                continue
            tmpNames[-1].append(w.word)
            if names.get(w.word) is None:
                names[w.word] = 0
            relationships[w.word] = {}
            names[w.word] += 1
    print(relationships)
    print(tmpNames)
    for name, times in names.items():
        print(name, times)

    for name in tmpNames:
        for name1 in name:
            for name2 in name:
                if name1 == name2:
                    continue
                if relationships[name1].get(name2) is None:
                    relationships[name1][name2] = 1
                else:
                    relationships[name1][name2] += 1
    print(relationships)
    with open("relationship.csv", "w", encoding='utf-8') as f:
        f.write("Source,Target,Weight\n")
        for name, edges in relationships.items():
            for v, w in edges.items():
                f.write(name + "," + v + "," + str(w) + "\n")

    with open("NameNode.csv", "w", encoding='utf-8') as f:
        f.write("ID,Label,Weight\n")
        for name, times in names.items():
            f.write(name + "," + name + "," + str(times) + "\n")


def deal_graph():
    relationship_data = pd.read_csv('relationship.csv')
    namenode_data = pd.read_csv('NameNode.csv')
    relationship_data_list = relationship_data.values.tolist()
    namenode_data_list = namenode_data.values.tolist()

    nodes = []
    for node in namenode_data_list:
        if node[0] == "宝玉":
            node[2] = node[2]/3
        nodes.append({"name": node[0], "symbolSize": node[2]/30})
    links = []
    for link in relationship_data_list:
        links.append({"source": link[0], "target": link[1], "value": link[2]})

    g = (
        Graph()
        .add("", nodes, links, repulsion=8000)
        .set_global_opts(title_opts=opts.TitleOpts(title="红楼人物关系"))
    )
    return g


if __name__ == '__main__':
    deal_data()
    g = deal_graph()
    g.render()
