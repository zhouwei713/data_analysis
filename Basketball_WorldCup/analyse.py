# coding = utf-8
"""
@author: zhou
@time:2019/9/16 15:52
@File: analyse.py
"""

from pyecharts import options as opts
from pyecharts.charts import Bar, Radar
from pyecharts.commons.utils import JsCode
import pandas as pd


points = pd.read_csv('PointsAverage_data.csv')
points_data = points.groupby(['name', 'country'])['points', 'rebounds'].sum().sort_values(by='points', ascending=False)
points_data_index = points_data['points'].index.values.tolist()[:15]
points_data_value = points_data['points'].values.tolist()[:15]
points_data_rebounds_value = points_data['rebounds'].values.tolist()[:15]

# 得分排名
bar = Bar()
bar.add_xaxis(points_data_index)
bar.add_yaxis("", points_data_value, category_gap="60%")
bar.set_global_opts(title_opts=opts.TitleOpts(title='得分排名'),
                   xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-20)),
                   datazoom_opts=opts.DataZoomOpts())
bar.set_series_opts(itemstyle_opts={
            "normal": {
                "color": JsCode("""new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: 'rgba(0, 244, 255, 1)'
                }, {
                    offset: 1,
                    color: 'rgba(0, 77, 167, 1)'
                }], false)"""),
                "barBorderRadius": [30, 30, 30, 30],
                "shadowColor": 'rgb(0, 160, 221)',
            }})
bar.render_notebook()

# 篮板
rebounds_data = points.groupby(['name', 'country'])['points', 'rebounds'].sum().sort_values(by='rebounds', ascending=False)
rebounds_data_index = rebounds_data['rebounds'].index.values.tolist()[:15]
rebounds_data_value = rebounds_data['rebounds'].values.tolist()[:15]
rebounds_data_rebounds_value = rebounds_data['rebounds'].values.tolist()[:15]
bar = Bar()
bar.add_xaxis(rebounds_data_index)
bar.add_yaxis("", rebounds_data_rebounds_value, category_gap="60%")
bar.set_global_opts(title_opts=opts.TitleOpts(title='篮板排名'),
                   xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-20)),
                   datazoom_opts=opts.DataZoomOpts())
bar.set_series_opts(itemstyle_opts={
            "normal": {
                "color": JsCode("""new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: 'rgba(0, 244, 255, 1)'
                }, {
                    offset: 1,
                    color: 'rgba(0, 77, 167, 1)'
                }], false)"""),
                "barBorderRadius": [30, 30, 30, 30],
                "shadowColor": 'rgb(0, 160, 221)',
            }})
bar.render_notebook()

# 球员得分和篮板
bar = Bar()
bar.add_xaxis(points_data_index)
bar.add_yaxis("", points_data_value, gap="0%")
bar.add_yaxis("", points_data_rebounds_value, gap="0%")
bar.set_global_opts(title_opts=opts.TitleOpts(title='得分排名和篮板'),
                   xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-20)),
                   datazoom_opts=opts.DataZoomOpts())
bar.render_notebook()

# 最佳阵容
the_best_lineup = [
    '博格达诺维奇',
    '富尼耶',
    '卢比奥',
    '斯科拉',
    '加索尔'
]
bgdnwq = points[points['name'] == '博格达诺维奇']
fny = points[points['name'] == '富尼耶']
lba = points[points['name'] == '卢比奥']
skl = points[points['name'] == '斯科拉']
jse = points[points['name'] == '加索尔']

bgdnwq_list = [[bgdnwq['points'].values.tolist()[0],
           bgdnwq['rebounds'].values.tolist()[0],
           bgdnwq['assists'].values.tolist()[0],
           bgdnwq['steals'].values.tolist()[0],
           bgdnwq['blocked'].values.tolist()[0],
           bgdnwq['fouls'].values.tolist()[0],
           bgdnwq['turnovers'].values.tolist()[0]]]
fny_list = [[fny['points'].values.tolist()[0],
           fny['rebounds'].values.tolist()[0],
           fny['assists'].values.tolist()[0],
           fny['steals'].values.tolist()[0],
           fny['blocked'].values.tolist()[0],
           fny['fouls'].values.tolist()[0],
           fny['turnovers'].values.tolist()[0]]]
lba_list = [[lba['points'].values.tolist()[0],
           lba['rebounds'].values.tolist()[0],
           lba['assists'].values.tolist()[0],
           lba['steals'].values.tolist()[0],
           lba['blocked'].values.tolist()[0],
           lba['fouls'].values.tolist()[0],
           lba['turnovers'].values.tolist()[0]]]
skl_list = [[skl['points'].values.tolist()[0],
           skl['rebounds'].values.tolist()[0],
           skl['assists'].values.tolist()[0],
           skl['steals'].values.tolist()[0],
           skl['blocked'].values.tolist()[0],
           skl['fouls'].values.tolist()[0],
           skl['turnovers'].values.tolist()[0]]]
jse_list = [[jse['points'].values.tolist()[0],
           jse['rebounds'].values.tolist()[0],
           jse['assists'].values.tolist()[0],
           jse['steals'].values.tolist()[0],
           jse['blocked'].values.tolist()[0],
           jse['fouls'].values.tolist()[0],
           jse['turnovers'].values.tolist()[0]]]
radar = Radar()
radar.add_schema(
    schema=[
        opts.RadarIndicatorItem(name='得分', max_=30),
        opts.RadarIndicatorItem(name="篮板", max_=15),
        opts.RadarIndicatorItem(name="助攻", max_=10),
        opts.RadarIndicatorItem(name="抢断", max_=5),
        opts.RadarIndicatorItem(name="封盖", max_=5),
        opts.RadarIndicatorItem(name="犯规", max_=5),
        opts.RadarIndicatorItem(name="失误", max_=5),
    ]
)
radar.add("博格达诺维奇", bgdnwq_list)
radar.add("富尼耶", fny_list)
radar.add("卢比奥", lba_list)
radar.add("斯科拉", skl_list)
radar.add("加索尔", jse_list)
# radar.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
radar.render_notebook()

# 投篮命中率
bgdnwq_goals_percentage = bgdnwq['goals_percentage'].values.tolist()[0]
fny_goals_percentage = fny['goals_percentage'].values.tolist()[0]
lba_goals_percentage = lba['goals_percentage'].values.tolist()[0]
skl_goals_percentage = skl['goals_percentage'].values.tolist()[0]
jse_goals_percentage = jse['goals_percentage'].values.tolist()[0]

data_list = [
bgdnwq_goals_percentage,
fny_goals_percentage,
lba_goals_percentage,
skl_goals_percentage,
jse_goals_percentage ]
bar = Bar()
bar.add_xaxis(the_best_lineup)
bar.add_yaxis("", data_list, category_gap="60%")
bar.set_global_opts(title_opts=opts.TitleOpts(title='最佳阵容投篮命中率'),
                   xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-20)),
                   )
bar.set_series_opts(itemstyle_opts={
            "normal": {
                "color": JsCode("""new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: 'rgba(0, 244, 255, 1)'
                }, {
                    offset: 1,
                    color: 'rgba(0, 77, 167, 1)'
                }], false)"""),
                "barBorderRadius": [30, 30, 30, 30],
                "shadowColor": 'rgb(0, 160, 221)',
            }})
bar.render_notebook()

# 球员正负值
bgdnwq_plus_minus = bgdnwq['plus_minus'].values.tolist()[0]
fny_plus_minus = fny['plus_minus'].values.tolist()[0]
lba_plus_minus = lba['plus_minus'].values.tolist()[0]
skl_plus_minus = skl['plus_minus'].values.tolist()[0]
jse_plus_minus = jse['plus_minus'].values.tolist()[0]

data_list = [bgdnwq_plus_minus,
fny_plus_minus,
lba_plus_minus,
skl_plus_minus,
jse_plus_minus]
bar = Bar()
bar.add_xaxis(the_best_lineup)
bar.add_yaxis("", data_list, category_gap="60%")
bar.set_global_opts(title_opts=opts.TitleOpts(title='最佳阵容投篮正负值'),
                   xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-20)),
                   )
bar.set_series_opts(itemstyle_opts={
            "normal": {
                "color": JsCode("""new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: 'rgba(0, 244, 255, 1)'
                }, {
                    offset: 1,
                    color: 'rgba(0, 77, 167, 1)'
                }], false)"""),
                "barBorderRadius": [30, 30, 30, 30],
                "shadowColor": 'rgb(0, 160, 221)',
            }})
bar.render_notebook()

# yijianlian
alian = points[points['name'] == '易建联']

alian_list = [[alian['points'].values.tolist()[0],
           alian['rebounds'].values.tolist()[0],
           alian['assists'].values.tolist()[0],
           alian['steals'].values.tolist()[0],
           alian['blocked'].values.tolist()[0],
           alian['fouls'].values.tolist()[0],
           alian['turnovers'].values.tolist()[0],
           alian['plus_minus'].values.tolist()[0],
           alian['goals_percentage'].values.tolist()[0]]]
radar = Radar()
radar.add_schema(
    schema=[
        opts.RadarIndicatorItem(name='得分', max_=30),
        opts.RadarIndicatorItem(name="篮板", max_=15),
        opts.RadarIndicatorItem(name="助攻", max_=10),
        opts.RadarIndicatorItem(name="抢断", max_=5),
        opts.RadarIndicatorItem(name="封盖", max_=5),
        opts.RadarIndicatorItem(name="犯规", max_=5),
        opts.RadarIndicatorItem(name="失误", max_=5),
        opts.RadarIndicatorItem(name="正负值", max_=10),
        opts.RadarIndicatorItem(name="命中率", max_=80)
    ]
)
radar.add("易建联", alian_list)

# radar.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
radar.render_notebook()


