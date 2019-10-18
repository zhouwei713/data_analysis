# coding = utf-8
"""
@author: zhou
@time:2019/10/18 20:59
@File: analyse.py
"""

import pandas as pd
from pyecharts.charts import Bar, Pie
from pyecharts import options as opts


data = pd.read_csv("weichat_data.csv")


def get_yuanchuang(d):
    yuanchuang = d.split(r'/')[0]
    return yuanchuang


def get_fawen(d):
    fawen = d.split(r'/')[1]
    return fawen

# 数据处理
data.loc[0, 'toutiao_read'] = 100001
data.loc[1, 'toutiao_read'] = 100001
data.loc[2, 'toutiao_read'] = 100001
# 原创数量
data['yuanchuang'] = data['yuanchuanghefawen'].apply(get_yuanchuang)
data['fawen'] = data['yuanchuanghefawen'].apply(get_fawen)
data['toutiao_read'] = data['toutiao_read'].astype('int')
data['seeing'] = data['seeing'].astype('int')

# 次幂指数
index_data = data[['name', 'index']]
index_data_sort = index_data.sort_values(by='index', ascending=False)

bar = Bar()
bar.add_xaxis(index_data_sort['name'].values.tolist())
bar.add_yaxis("", index_data_sort['index'].values.tolist())
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
    title_opts=opts.TitleOpts(title="次幂指数"),
    datazoom_opts=opts.DataZoomOpts(),
)
bar.render_notebook()

# 阅读量
read_data = data[['name', 'toutiao_read']]
read_data_sort = read_data.sort_values(by='toutiao_read', ascending=False)

bar = Bar()
bar.add_xaxis(read_data_sort['name'].values.tolist())
bar.add_yaxis("", read_data_sort['toutiao_read'].values.tolist())
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
    title_opts=opts.TitleOpts(title="头条平均阅读量"),
    datazoom_opts=opts.DataZoomOpts(),
)
bar.render_notebook()

# 在看数量
seeing_data = data[['name', 'seeing']]
seeing_data_sort = seeing_data.sort_values(by='seeing', ascending=False)

bar = Bar()
bar.add_xaxis(seeing_data_sort['name'].values.tolist())
bar.add_yaxis("", seeing_data_sort['seeing'].values.tolist())
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
    title_opts=opts.TitleOpts(title="在看数量"),
    datazoom_opts=opts.DataZoomOpts(),
)
bar.render_notebook()

# 原创和发文
yuanchuang_data = data[['name', 'yuanchuang', 'fawen']]
yuanchuang_data_sort = yuanchuang_data.sort_values(by='yuanchuang', ascending=False)
fawen_data_sort = yuanchuang_data.sort_values(by='fawen', ascending=False)

bar = Bar()
bar.add_xaxis(yuanchuang_data_sort['name'].values.tolist())
bar.add_yaxis("发文数量", yuanchuang_data_sort['fawen'].values.tolist())
bar.add_yaxis("原创数量", yuanchuang_data_sort['yuanchuang'].values.tolist())
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
    title_opts=opts.TitleOpts(title="原创vs发文"),
    datazoom_opts=opts.DataZoomOpts(),
)
bar.render_notebook()

bar = Bar()
bar.add_xaxis(yuanchuang_data_sort['name'].values.tolist())
bar.add_yaxis("发文数量", fawen_data_sort['fawen'].values.tolist())
bar.add_yaxis("原创数量", fawen_data_sort['yuanchuang'].values.tolist())
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
    title_opts=opts.TitleOpts(title="原创vs发文"),
    datazoom_opts=opts.DataZoomOpts(),
)
bar.render_notebook()

yuanchuang_data['rate'] = yuanchuang_data['yuanchuang']/yuanchuang_data['fawen']
rate_data = yuanchuang_data.sort_values(by='rate', ascending=False)

bar = Bar()
bar.add_xaxis(rate_data['name'].values.tolist())
bar.add_yaxis("", rate_data['rate'].values.tolist())
# bar.add_yaxis("原创数量", fawen_data_sort['yuanchuang'].values.tolist())
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
    title_opts=opts.TitleOpts(title="原创与发文数量比例"),
    datazoom_opts=opts.DataZoomOpts(),
)
bar.render_notebook()

# 十万
wudi_df = data[0:3]

bar = Bar()
bar.add_xaxis(wudi_df['name'].values.tolist())
bar.add_yaxis("头条平均阅读", wudi_df['toutiao_read'].values.tolist())
bar.add_yaxis("次条平均阅读", wudi_df['citiao_read'].values.tolist())
bar.add_yaxis("在看数量", wudi_df['seeing'].values.tolist())
bar.add_yaxis("次幂指数", wudi_df['index'].values.tolist())
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
    title_opts=opts.TitleOpts(title="十万+整体数据"),
    # datazoom_opts=opts.DataZoomOpts(),
)
bar.render_notebook()

bar = Bar()
bar.add_xaxis(wudi_df['name'].values.tolist())
bar.add_yaxis("发文数量", wudi_df['fawen'].values.tolist())
bar.add_yaxis("原创数量", wudi_df['yuanchuang'].values.tolist())
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
    title_opts=opts.TitleOpts(title="十万+整体数据"),
    # datazoom_opts=opts.DataZoomOpts(),
)
bar.render_notebook()

# 五万以上
data_above_5 = data[data['toutiao_read'] > 50000]
data_above_5.drop(index=[0,1,2], inplace=True)

bar = Bar()
bar.add_xaxis(data_above_5['name'].values.tolist())
bar.add_yaxis("头条平均阅读", data_above_5['toutiao_read'].values.tolist())
bar.add_yaxis("次条平均阅读", data_above_5['citiao_read'].values.tolist())
bar.add_yaxis("在看数量", data_above_5['seeing'].values.tolist())
bar.add_yaxis("次幂指数", data_above_5['index'].values.tolist())
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
    title_opts=opts.TitleOpts(title="大于5万阅读数据"),
    # datazoom_opts=opts.DataZoomOpts(),
)
bar.render_notebook()

bar = Bar()
bar.add_xaxis(data_above_5['name'].values.tolist())
bar.add_yaxis("发文数量", data_above_5['fawen'].values.tolist())
bar.add_yaxis("原创数量", data_above_5['yuanchuang'].values.tolist())
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
    title_opts=opts.TitleOpts(title="大于5万阅读数据"),
    # datazoom_opts=opts.DataZoomOpts(),
)
bar.render_notebook()

# 五万到一万
data_between_5w_1w = data[data['toutiao_read'] > 10000]
data_between_5w_1w = data_between_5w_1w[data_between_5w_1w['toutiao_read'] < 50000]

bar = Bar()
bar.add_xaxis(data_between_5w_1w['name'].values.tolist())
bar.add_yaxis("头条平均阅读", data_between_5w_1w['toutiao_read'].values.tolist())
bar.add_yaxis("次条平均阅读", data_between_5w_1w['citiao_read'].values.tolist())
bar.add_yaxis("在看数量", data_between_5w_1w['seeing'].values.tolist())
bar.add_yaxis("次幂指数", data_between_5w_1w['index'].values.tolist())
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
    title_opts=opts.TitleOpts(title="阅读数在1万到5万数据"),
    datazoom_opts=opts.DataZoomOpts(),
)
bar.render_notebook()

bar = Bar()
bar.add_xaxis(data_between_5w_1w['name'].values.tolist())
bar.add_yaxis("发文数量", data_between_5w_1w['fawen'].values.tolist())
bar.add_yaxis("原创数量", data_between_5w_1w['yuanchuang'].values.tolist())
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
    title_opts=opts.TitleOpts(title="阅读数在1万到5万数据"),
    datazoom_opts=opts.DataZoomOpts(),
)
bar.render_notebook()

# 五千到1万
data_between_5k_1w = data[data['toutiao_read'] < 10000]
data_between_5k_1w = data_between_5k_1w[data_between_5k_1w['toutiao_read'] > 5000]

bar = Bar()
bar.add_xaxis(data_between_5k_1w['name'].values.tolist())
bar.add_yaxis("头条平均阅读", data_between_5k_1w['toutiao_read'].values.tolist())
bar.add_yaxis("次条平均阅读", data_between_5k_1w['citiao_read'].values.tolist())
bar.add_yaxis("在看数量", data_between_5k_1w['seeing'].values.tolist())
bar.add_yaxis("次幂指数", data_between_5k_1w['index'].values.tolist())
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
    title_opts=opts.TitleOpts(title="阅读数在5千到1万数据"),
    datazoom_opts=opts.DataZoomOpts(),
)
bar.render_notebook()

bar = Bar()
bar.add_xaxis(data_between_5k_1w['name'].values.tolist())
bar.add_yaxis("发文数量", data_between_5k_1w['fawen'].values.tolist())
bar.add_yaxis("原创数量", data_between_5k_1w['yuanchuang'].values.tolist())
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
    title_opts=opts.TitleOpts(title="阅读数在5千到1万数据"),
    datazoom_opts=opts.DataZoomOpts(),
)
bar.render_notebook()

# 五千以下
data_below_5k = data[data['toutiao_read'] < 5000]

bar = Bar()
bar.add_xaxis(data_below_5k['name'].values.tolist())
bar.add_yaxis("头条平均阅读", data_below_5k['toutiao_read'].values.tolist())
bar.add_yaxis("次条平均阅读", data_below_5k['citiao_read'].values.tolist())
bar.add_yaxis("在看数量", data_below_5k['seeing'].values.tolist())
bar.add_yaxis("次幂指数", data_below_5k['index'].values.tolist())
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
    title_opts=opts.TitleOpts(title="阅读数在5千以下数据"),
    datazoom_opts=opts.DataZoomOpts(),
)
bar.render_notebook()

bar = Bar()
bar.add_xaxis(data_below_5k['name'].values.tolist())
bar.add_yaxis("发文数量", data_below_5k['fawen'].values.tolist())
bar.add_yaxis("原创数量", data_below_5k['yuanchuang'].values.tolist())
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
    title_opts=opts.TitleOpts(title="阅读数在5千一下数据"),
    datazoom_opts=opts.DataZoomOpts(),
)
bar.render_notebook()

