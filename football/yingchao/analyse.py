# coding = utf-8
"""
@author: zhou
@time:2019/10/8 9:58
@File: analyse.py
"""

import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar, Scatter, Radar
from pyecharts.commons.utils import JsCode


# 球队分析
team_df = pd.read_csv('yingchao_data.csv')

goal_data = team_df[['team', 'goal', 'goal_diff']]
data_goal = goal_data.sort_values(by='goal', ascending=False)
goal_data_name = data_goal['team'].values.tolist()
goal_data_num = data_goal['goal'].values.tolist()
goal_data_diff = data_goal['goal_diff'].values.tolist()

bar = Bar()
bar.add_xaxis(goal_data_name)
bar.add_yaxis('', goal_data_num)
bar.add_yaxis('', goal_data_diff)
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
    title_opts=opts.TitleOpts(title="各球队进球数据", subtitle="进球和净胜球"),
    datazoom_opts=opts.DataZoomOpts(),
)
bar.render_notebook()

# 球员数据分析

# 综合得分
player_df = pd.read_csv('player_data.csv')

score_data = player_df[['club', 'score']]
score_mean = score_data.groupby(by = 'club').mean().sort_values(by = 'score', ascending = False)
score_mean.reset_index(inplace = True)
score_name = score_mean['club'].values.tolist()
score_num = score_mean['score'].values.tolist()

bar = Bar()
bar.add_xaxis(score_name)
bar.add_yaxis('', score_num)
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
    title_opts=opts.TitleOpts(title="各球队综合得分", subtitle="各球员综合得分均值"),
    datazoom_opts=opts.DataZoomOpts(),
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
            }},
            label_opts=opts.LabelOpts(is_show=False))
bar.render_notebook()

# 前锋分析
df_vanguard = player_df[player_df['staff'] == '前锋'][['staff', 'club', 'shot', 'speed', 'power']]
df_vanguard = df_vanguard.groupby(by='club').mean()[['shot', 'speed', 'power']]
df_vanguard['size'] = ((df_vanguard['shot'] - df_vanguard['shot'].min()) / (df_vanguard['shot'].max() - df_vanguard['shot'].min()) + 1) * 10
df_vanguard.reset_index(inplace=True)
df_vanguard.sort_values(by='shot', ascending=False, inplace=True)
vanguard_shot = df_vanguard['shot'].values.tolist()
vanguard_speed = df_vanguard['speed'].values.tolist()
vanguard_power = df_vanguard['power'].values.tolist()
vanguard_club = df_vanguard['club'].values.tolist()
vanguard_size = df_vanguard['size'].values.tolist()

bar = Bar()
bar.add_xaxis(vanguard_club)
bar.add_yaxis('', vanguard_shot, gap="0%")
bar.add_yaxis('', vanguard_speed, gap="0%")
bar.add_yaxis('', vanguard_power, gap="0%")
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
    title_opts=opts.TitleOpts(title="各球队前锋数据", subtitle="射术、速度和力量"),
    datazoom_opts=opts.DataZoomOpts(),
)
bar.set_series_opts(
            label_opts=opts.LabelOpts(is_show=False))
bar.render_notebook()

# 锋线散点图
scatter = Scatter()
scatter.add_xaxis(vanguard_club)
scatter.add_yaxis("shot", vanguard_shot, symbol='pin')
scatter.add_yaxis("speed", vanguard_speed, symbol='triangle')
scatter.add_yaxis("power", vanguard_power, symbol='diamond')
scatter.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
            title_opts=opts.TitleOpts(title="各球队前锋数据"),
            visualmap_opts=opts.VisualMapOpts(type_='size', max_=90, min_=60),
        )
scatter.set_series_opts(
            label_opts=opts.LabelOpts(is_show=False))
scatter.render_notebook()

# 中场
df_midfield = player_df[player_df['staff'] == '中场'][['staff', 'club', 'pass', 'speed', 'tape']]
df_midfield = df_midfield.groupby(by = 'club').mean()[['pass', 'speed', 'tape']]
df_midfield['size'] = ((df_midfield['tape'] - df_midfield['tape'].min()) / (df_midfield['tape'].max() - df_midfield['tape'].min()) + 1) * 10
df_midfield.reset_index(inplace = True)
df_midfield.sort_values(by = 'pass', ascending = False, inplace = True)
midfield_pass = df_midfield['pass'].values.tolist()
midfield_speed = df_midfield['speed'].values.tolist()
midfield_tape = df_midfield['tape'].values.tolist()
midfield_club = df_midfield['club'].values.tolist()
midfield_size = df_midfield['size'].values.tolist()

bar = Bar()
bar.add_xaxis(midfield_club)
bar.add_yaxis('', midfield_pass, gap="0%")
bar.add_yaxis('', midfield_speed, gap="0%")
bar.add_yaxis('', midfield_tape, gap="0%")
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
    title_opts=opts.TitleOpts(title="各球队中场数据", subtitle="传球、速度和盘带"),
    datazoom_opts=opts.DataZoomOpts(),
)
bar.set_series_opts(
            label_opts=opts.LabelOpts(is_show=False))
bar.render_notebook()

# 后卫
df_guard = player_df[player_df['staff'] == '后卫'][['staff', 'club', 'pass', 'defend', 'power']]
df_guard = df_guard.groupby(by = 'club').mean()[['pass', 'defend', 'power']]
df_guard['size'] = ((df_guard['defend'] - df_guard['defend'].min()) / (df_guard['defend'].max() - df_guard['defend'].min()) + 1) * 10
df_guard.reset_index(inplace = True)
df_guard.sort_values(by = 'defend', ascending = False, inplace = True)
guard_pass = df_guard['pass'].values.tolist()
guard_defend = df_guard['defend'].values.tolist()
guard_power = df_guard['power'].values.tolist()
guard_club = df_guard['club'].values.tolist()
guard_size = df_guard['size'].values.tolist()

bar = Bar()
bar.add_xaxis(midfield_club)
bar.add_yaxis('', midfield_pass, gap="0%")
bar.add_yaxis('', midfield_speed, gap="0%")
bar.add_yaxis('', midfield_tape, gap="0%")
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
    title_opts=opts.TitleOpts(title="各球队后卫数据", subtitle="传球、防守和力量"),
    datazoom_opts=opts.DataZoomOpts(),
)
bar.set_series_opts(
            label_opts=opts.LabelOpts(is_show=False))
bar.render_notebook()

# 英超五强
team = player_df.groupby(by='club').mean()
team.reset_index(inplace = True)

liwupu_score = team[team['club'] == '利物浦']['score'].values.tolist()
liwupu_speed = team[team['club'] == '利物浦']['speed'].values.tolist()
liwupu_power = team[team['club'] == '利物浦']['power'].values.tolist()
liwupu_defend = team[team['club'] == '利物浦']['defend'].values.tolist()
liwupu_tape = team[team['club'] == '利物浦']['tape'].values.tolist()
liwupu_pass = team[team['club'] == '利物浦']['pass'].values.tolist()
liwupu_shot = team[team['club'] == '利物浦']['shot'].values.tolist()
liwupu_data = []
liwupu_tmp_data = [int(liwupu_score[0]), int(liwupu_speed[0]), int(liwupu_power[0]), int(liwupu_defend[0]), int(liwupu_tape[0]),
int(liwupu_pass[0]), int(liwupu_shot[0])]
liwupu_data.append(liwupu_tmp_data)

mancheng_score = team[team['club'] == '曼城']['score'].values.tolist()
mancheng_speed = team[team['club'] == '曼城']['speed'].values.tolist()
mancheng_power = team[team['club'] == '曼城']['power'].values.tolist()
mancheng_defend = team[team['club'] == '曼城']['defend'].values.tolist()
mancheng_tape = team[team['club'] == '曼城']['tape'].values.tolist()
mancheng_pass = team[team['club'] == '曼城']['pass'].values.tolist()
mancheng_shot = team[team['club'] == '曼城']['shot'].values.tolist()
mancheng_data = []
mancheng_tmp_data = [int(mancheng_score[0]), int(mancheng_speed[0]), int(mancheng_power[0]), int(mancheng_defend[0]), int(mancheng_tape[0]),
int(mancheng_pass[0]), int(mancheng_shot[0])]
mancheng_data.append(mancheng_tmp_data)

asenna_score = team[team['club'] == '阿森纳']['score'].values.tolist()
asenna_speed = team[team['club'] == '阿森纳']['speed'].values.tolist()
asenna_power = team[team['club'] == '阿森纳']['power'].values.tolist()
asenna_defend = team[team['club'] == '阿森纳']['defend'].values.tolist()
asenna_tape = team[team['club'] == '阿森纳']['tape'].values.tolist()
asenna_pass = team[team['club'] == '阿森纳']['pass'].values.tolist()
asenna_shot = team[team['club'] == '阿森纳']['shot'].values.tolist()
asenna_data = []
asenna_tmp_data = [int(asenna_score[0]), int(asenna_speed[0]), int(asenna_power[0]), int(asenna_defend[0]), int(asenna_tape[0]),
int(asenna_pass[0]), int(asenna_shot[0])]
asenna_data.append(asenna_tmp_data)

manlian_score = team[team['club'] == '曼联']['score'].values.tolist()
manlian_speed = team[team['club'] == '曼联']['speed'].values.tolist()
manlian_power = team[team['club'] == '曼联']['power'].values.tolist()
manlian_defend = team[team['club'] == '曼联']['defend'].values.tolist()
manlian_tape = team[team['club'] == '曼联']['tape'].values.tolist()
manlian_pass = team[team['club'] == '曼联']['pass'].values.tolist()
manlian_shot = team[team['club'] == '曼联']['shot'].values.tolist()
manlian_data = []
manlian_tmp_data = [int(manlian_score[0]), int(manlian_speed[0]), int(manlian_power[0]), int(manlian_defend[0]), int(manlian_tape[0]),
int(manlian_pass[0]), int(manlian_shot[0])]
manlian_data.append(manlian_tmp_data)

qieerxi_score = team[team['club'] == '切尔西']['score'].values.tolist()
qieerxi_speed = team[team['club'] == '切尔西']['speed'].values.tolist()
qieerxi_power = team[team['club'] == '切尔西']['power'].values.tolist()
qieerxi_defend = team[team['club'] == '切尔西']['defend'].values.tolist()
qieerxi_tape = team[team['club'] == '切尔西']['tape'].values.tolist()
qieerxi_pass = team[team['club'] == '切尔西']['pass'].values.tolist()
qieerxi_shot = team[team['club'] == '切尔西']['shot'].values.tolist()
qieerxi_data = []
qieerxi_tmp_data = [int(qieerxi_score[0]), int(qieerxi_speed[0]), int(qieerxi_power[0]), int(qieerxi_defend[0]), int(qieerxi_tape[0]),
int(qieerxi_pass[0]), int(qieerxi_shot[0])]
qieerxi_data.append(qieerxi_tmp_data)

radar = Radar()
radar.add_schema(
            schema=[
                opts.RadarIndicatorItem(name='综合得分', max_=100),
                opts.RadarIndicatorItem(name='速度', max_=100),
                opts.RadarIndicatorItem(name='力量', max_=100),
                opts.RadarIndicatorItem(name='防守', max_=100),
                opts.RadarIndicatorItem(name='盘带', max_=100),
                opts.RadarIndicatorItem(name='传球', max_=100),
                opts.RadarIndicatorItem(name='射术', max_=100)
            ]
)
radar.add('利物浦', liwupu_data, color="#f9713c")
radar.add('曼城', mancheng_data, color="#30ff00")
radar.add('阿森纳', asenna_data, color="#9400D3")
radar.add('曼联', manlian_data, color="#141414")
radar.add('切尔西', qieerxi_data, color="#00F5FF")
radar.render_notebook()


