# coding = utf-8
"""
@author: zhou
@time:2019/3/12 19:47
"""


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
from pyecharts import Pie
from collections import Counter

plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
data = pd.read_csv('all_hero_init_attr.csv', encoding='gb18030')

feature = ['英雄名字', '生存能力', '攻击伤害', '技能效果',
           '上手难度', '最大生命', '最大法力', '物理攻击',
           '法术攻击', '物理防御', '物理减伤率', '法术防御',
           '法术减伤率', '移速', '物理护甲穿透', '法术护甲穿透',
           '攻速加成', '暴击几率', '暴击效果', '物理吸血', '法术吸血',
           '冷却缩减', '攻击范围', '韧性', '生命回复', '法力回复']


data_init = data[feature]

# 把空值设置为0
data_init = data_init.fillna(0)
# print(data_init.isnull().sum())

'''
正则匹配包含%%的数据
p = r'(%%)'
a = data_init['物理减伤率'].astype("object").str.extract(p)
print(a)
'''

# corr = data_init[feature].corr()
# plt.figure(figsize=(14, 14))
# sns.heatmap(corr, annot=True)
# plt.show()


features_remain = ['生存能力', '攻击伤害', '技能效果',
                    '上手难度', '最大生命', '最大法力', '物理攻击',
                    '法术攻击', '物理防御', '物理减伤率', '移速', '攻击范围', '生命回复', '法力回复']

data_init = data_init[features_remain]

data_init['物理减伤率'] = data_init['物理减伤率'].apply(lambda x: float(x.strip('%'))/100)

data_init['攻击范围'] = data_init['攻击范围'].map({'远程': 1, '近程': 0})

# print(data_init)

ss = StandardScaler()
data_init = ss.fit_transform(data_init)

gmm = GaussianMixture(n_components=20, covariance_type='full')
gmm.fit(data_init)

prediction = gmm.predict(data_init)
# print(prediction)
data.insert(0, '分组', prediction)
data.to_csv('all_hero_init_attr_our.csv', index=False, sep=',', encoding='gb18030')


df = data[['分组', '英雄名字']]  # 获取需要的两列

grouped = df.groupby(['分组'])  # 以”分组“列来进行分组
k = []

# 获取分组后的 组和值，保存为字典，放到列表中
for name, group in grouped:
    k.append({name: list(group['英雄名字'].values)})

kk = []
for i in k:
    for k, v in i.items():
        kk.append(v)

length = []
key = []
for i in kk:
    key.append(str(i))
    length.append(len(i))

pie = Pie('英雄初始属性分类图', title_pos='center')
pie.add("", key, length,
        is_label_show=True, legend_pos="bottom", legend_orient="vertical",)
pie.render()


def generate_all_hero():
    pass


if __name__ == '__main__':
    generate_all_hero()
