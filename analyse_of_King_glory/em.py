# coding = utf-8
"""
@author: zhou
@time:2019/3/11 18:41
"""

from sklearn.mixture import GaussianMixture
import pandas as pd
import csv
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from pyecharts.charts import Pie

hero_data = pd.read_csv('hero_attr.csv', encoding='gb18030')
feature = ['1级物理攻击', '15级物理攻击', '每级成长',
           '1级生命', '15级生命', '生命成长值', '1级物理防御',
           '15级物理防御', '每级物理防御成长', '攻速成长',
           '1级每5秒回血', '15级每5秒回血', '1级最大法力',
           '15级最大法力', '最大法力成长', '1级每五秒回蓝',
           '15级每5秒回蓝', '近/远程？', '移速', '定位', '个人建议分路']

data = hero_data[feature]

plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

corr = data[feature].corr()

plt.figure(figsize=(14, 14))
sns.heatmap(corr, annot=True)
plt.show()

features_remain = ['15级生命', '15级物理攻击',
                   '15级物理防御', '15级最大法力',
                   '15级每5秒回血', '15级每5秒回蓝', '移速',
                   '攻速成长', '近/远程？']

data_new = hero_data[features_remain]

data_new['近/远程？'] = data_new['近/远程？'].map({'远程': 1, '近程': 0})
ss = StandardScaler()
data_new = ss.fit_transform(data_new)

# 构造 GMM 聚类
gmm = GaussianMixture(n_components=20, covariance_type='full')
gmm.fit(data_new)

# 训练数据
prediction = gmm.predict(data_new)
# print(prediction)

hero_data.insert(0, '分组', prediction)
hero_data.to_csv('hero_out.csv', index=False, sep=',', encoding='gb18030')


df = hero_data[['分组', '名称']]

grouped = df.groupby(['分组'])
k = []
for name, group in grouped:
    k.append({name: list(group['名称'].values)})

kk = []
for i in k:
    for k, v in i.items():
        kk.append(v)

length = []
key = []
for i in kk:
    key.append(str(i))
    length.append(len(i))
pie = Pie('英雄完全属性分类图', title_pos='center')
pie.add("", key, length,
        is_label_show=True, legend_pos="bottom", legend_orient="vertical",)
pie.render()
