# coding = utf-8
"""
@author: zhou
@time:2019/9/5 16:07
@File: analyse.py
"""

from pyecharts import options as opts
from pyecharts.charts import PictorialBar, Line, Bar
from pyecharts.globals import SymbolType
from pyecharts.charts import Geo
from pyecharts.globals import ChartType
from pyecharts.commons.utils import JsCode
import pandas as pd
import re


provincial = pd.read_csv('provincial_capital')  # 读取省会信息
china_city_code = pd.read_csv('china-city-list.csv')  # 读取城市 id 信息
weather = pd.read_csv("weather_data.csv")  # 读取天气信息

# 查看天气总体情况
weather['wea'].value_counts()

# 转换天气变量，数值越多，说明降水概率越大
weather_dict = {
    "snow": 100,
    "rain": 80,
    "cloud": 50,
    "overcast": 60,
    "sun": 20
}

# 提取省会城市 id
provincial_data = pd.DataFrame()
for i in provincial['city'].values.tolist():
    for j in china_city_code['City_CN'].values.tolist():
        if j == i:
            provincial_data = pd.concat([china_city_code[china_city_code['City_CN'] == j], provincial_data])

# 按照城市分组
wea_group = weather.groupby('city').apply(lambda x: x[:])

# 提取中秋节当天天气信息
zhongqiu = wea_group[wea_group['time'] == '周五（13日）']

# 城市信息
zhongqiu_city = zhongqiu['city'].values.tolist()

# 获取温度信息
rege = r'(\d+)℃/(\d+)℃'


def trans_tem(tem):
    tmp_tem = re.match(rege, tem)
    mid_tem = (int(tmp_tem.group(1)) + int(tmp_tem.group(2)))/2
    return mid_tem


# 转换降水信息
def check_weather(wea):
    if wea[-1:] == '晴':
        wea = weather_dict['sun']
    elif wea[-1:] == '云':
        wea = weather_dict['cloud']
    elif wea[-1:] == '雨':
        wea = weather_dict['rain']
    elif wea[-1:] == '阴':
        wea = weather_dict['overcast']
    return wea


# 获取降水和温度信息
weather_data = map(check_weather, zhongqiu['wea'].values.tolist())
weather_data = list(weather_data)
tem_data = map(trans_tem, zhongqiu['tem'].values.tolist())
tem_data = list(tem_data)

# 降水和温度柱状图
pictorialbar = PictorialBar()
pictorialbar.add_xaxis(zhongqiu_city)
pictorialbar.add_yaxis(
    "weather", weather_data,
    label_opts=opts.LabelOpts(is_show=False),
    symbol_size=18,
    symbol_repeat="fixed",
    symbol_offset=[0, 0],
    is_symbol_clip=True,
    symbol=SymbolType.ROUND_RECT
)
pictorialbar.add_yaxis(
    "temperature", tem_data,
    label_opts=opts.LabelOpts(is_show=False),
    symbol_size=18,
    symbol_repeat="fixed",
    symbol_offset=[0, 0],
    is_symbol_clip=True,
    symbol=SymbolType.ARROW
)

# pictorialbar.reversal_axis()
pictorialbar.set_global_opts(
            title_opts=opts.TitleOpts(title="中秋节省会城市降雨和温度情况"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30), is_show=True),
            yaxis_opts=opts.AxisOpts(
                axistick_opts=opts.AxisTickOpts(is_show=False),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(opacity=0)
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value}% 降水概率")
            ),
            datazoom_opts=opts.DataZoomOpts()
)

# 添加折线
# line = Line()
# line.add_xaxis(zhongqiu_city)
# line.add_yaxis("", tem_data)
# line.add_yaxis("", weather_data)
# pictorialbar.overlap(line)
pictorialbar.render_notebook()

# 在双轴图中查看
bar = Bar()
bar.add_xaxis(zhongqiu_city)
bar.add_yaxis("", weather_data)
bar.extend_axis(
    yaxis=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(formatter="{value} °C"), interval=5
            )
)
bar.set_global_opts(
            title_opts=opts.TitleOpts(title="中秋节省会城市降雨和温度情况"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30), is_show=True),
            yaxis_opts=opts.AxisOpts(
                axistick_opts=opts.AxisTickOpts(is_show=False),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(opacity=0)
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value}% 降水概率")
            ),
            datazoom_opts=opts.DataZoomOpts()
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
line = Line().add_xaxis(zhongqiu_city).add_yaxis("", tem_data, yaxis_index=1)
bar.overlap(line)
bar.render_notebook()

# 矢量图位置信息
rain = 'path://M596.48 972.8a34.133333 34.133333 0 0 1-34.133333-34.133333v-85.333334a34.133333 34.133333 0 0 1 68.266666 0v85.333334a34.133333 34.133333 0 0 1-34.133333 34.133333z m-170.666667 0a34.133333 34.133333 0 0 1-34.133333-34.133333v-85.333334a34.133333 34.133333 0 0 1 68.266667 0v85.333334a34.133333 34.133333 0 0 1-34.133334 34.133333z m256-170.666667a34.133333 34.133333 0 0 1-34.133333-34.133333v-85.333333a34.133333 34.133333 0 0 1 68.266667 0v85.333333a34.133333 34.133333 0 0 1-34.133334 34.133333zM512 802.133333a34.133333 34.133333 0 0 1-34.133333-34.133333v-85.333333a34.133333 34.133333 0 0 1 68.266666 0v85.333333a34.133333 34.133333 0 0 1-34.133333 34.133333z m-171.52 0a34.133333 34.133333 0 0 1-34.133333-34.133333v-85.333333a34.133333 34.133333 0 0 1 68.266666 0v85.333333a34.133333 34.133333 0 0 1-34.133333 34.133333zM768 614.4H213.333333c-39.8336 0-74.325333-14.318933-102.519466-42.5472C82.5856 543.6416 68.266667 509.1328 68.266667 469.333333s14.318933-74.2912 42.5472-102.519466S173.533867 324.266667 213.333333 324.266667c8.942933 0 17.6128 0.7168 25.9584 2.116266 3.3792-68.625067 30.1568-128.443733 79.7184-178.0224C372.1728 95.214933 437.0944 68.266667 512 68.266667c74.922667 0 139.8272 26.948267 192.9728 80.093866 26.88 26.897067 47.3088 57.326933 60.859733 90.589867L768 238.933333c51.626667 0 96.426667 18.295467 133.137067 54.391467C937.437867 330.257067 955.733333 375.04 955.733333 426.666667c0 51.677867-18.3296 96.221867-54.493866 132.386133C864.546133 595.780267 819.712 614.4 768 614.4zM213.333333 358.4c-30.856533 0-56.490667 10.6496-78.3872 32.546133S102.4 438.4768 102.4 469.333333s10.6496 56.490667 32.546133 78.3872C156.8256 569.617067 182.459733 580.266667 213.333333 580.266667H768c42.939733 0 78.609067-14.830933 109.1072-45.346134C907.042133 504.968533 921.6 469.5552 921.6 426.666667c0-42.9568-14.574933-78.677333-44.5952-109.2096C846.677333 287.6416 810.973867 273.066667 768 273.066667a97.28 97.28 0 0 0-11.5712 0.7168 17.2032 17.2032 0 0 1-18.193067-11.3152c-11.605333-33.194667-30.907733-63.470933-57.3952-89.975467C633.668267 125.320533 578.4576 102.4 512 102.4s-121.668267 22.920533-168.840533 70.0928S273.066667 274.875733 273.066667 341.333333v6.826667a17.066667 17.066667 0 0 1-22.6816 16.110933A112.6912 112.6912 0 0 0 213.333333 358.4z'
wind = 'path://M990.71072 106.976l-9.856-9.536c-18.816-22.176-47.744-33.408-86.016-33.408-43.424 0-92.608 14.176-132.096 25.568a1426.56 1426.56 0 0 1-23.04 6.528 1262.976 1262.976 0 0 0-251.232 97.504c-94.848 48.832-208.192 121.216-242.816 248.96-16.896 63.168 8.96 203.936 25.92 282.4 2.368 10.816 6.4 20.992 11.68 30.336-65.856 101.184-146.944 147.392-248.768 139.84a31.808 31.808 0 0 0-34.304 29.504 32 32 0 0 0 29.504 34.272c8.96 0.672 17.728 1.024 26.464 1.024 110.496 0 202.624-54.624 274.944-161.28 7.424 3.36 15.104 6.112 23.072 7.68 55.168 11.52 158.56 30.816 231.232 30.816 22.496 0 40.32-1.856 54.464-5.6 129.568-33.856 203.008-145.536 252.48-238.976a1243.36 1243.36 0 0 0 99.2-247.456c2.016-7.232 4.32-15.136 6.784-23.488 21.088-71.52 49.92-169.44-7.616-214.688z m-652.8 614.72a44.992 44.992 0 0 1-3.84-10.368c-25.504-118.176-35.968-217.184-26.656-252.064 27.936-102.912 121.984-163.264 210.336-208.704a1197.696 1197.696 0 0 1 238.56-92.608c7.424-2.016 15.552-4.384 24.192-6.848C816.08672 140.8 860.47072 128 894.80672 128c18.688 0 31.168 3.712 37.312 11.008-41.216 58.56-96.096 115.68-143.424 161.984a176.672 176.672 0 0 1-42.56-92.608 16 16 0 0 0-31.68 4.288 208.224 208.224 0 0 0 51.296 110.464l-126.176 120.48c-45.152-42.528-74.112-100.896-81.504-166.4a16 16 0 0 0-31.84 3.584c8.224 72.448 40.16 137.28 90.08 184.864a12220.608 12220.608 0 0 1-124.352 117.056c-52.32-47.136-84.64-109.28-91.008-176.896a15.936 15.936 0 0 0-17.44-14.4 16 16 0 0 0-14.4 17.408c7.04 74.752 42.304 143.488 99.328 195.712-46.4 42.816-89.6 81.536-130.56 117.12z m599.04-418.144a1253.76 1253.76 0 0 0-7.04 24.48 1177.824 1177.824 0 0 1-94.08 234.592c-46.08 87.04-107.296 179.648-212.256 207.072-5.952 1.6-17.44 3.488-38.176 3.488-69.44 0-175.68-20.608-218.56-29.536-1.344-0.288-2.528-0.96-3.84-1.376a5963.392 5963.392 0 0 0 130.336-117.056c31.744 24.064 67.52 42.848 107.04 55.328 27.072 8.576 55.456 14.912 84.288 18.816a16 16 0 0 0 4.32-31.712c-27.04-3.648-53.568-9.6-78.944-17.632a320.64 320.64 0 0 1-92.96-46.944 12602.368 12602.368 0 0 0 124.064-116.8 302.688 302.688 0 0 0 150.24 59.84c5.44 0.672 11.232 1.344 17.024 1.696l0.96 0.032a16 16 0 0 0 0.96-31.968 242.656 242.656 0 0 1-15.168-1.536 271.68 271.68 0 0 1-130.432-50.432l123.744-118.144c19.84 16.512 42.4 29.312 67.68 37.76a16 16 0 0 0 10.112-30.4 176.32 176.32 0 0 1-54.72-29.664c46.688-45.696 100.8-101.856 142.88-160.384 15.328 28.256-5.536 99.968-17.472 140.48z'
sun = 'path://M512 256q69.674667 0 128.512 34.346667t93.184 93.184 34.346667 128.512-34.346667 128.512-93.184 93.184-128.512 34.346667-128.512-34.346667-93.184-93.184-34.346667-128.512 34.346667-128.512 93.184-93.184 128.512-34.346667zM240.682667 740.650667q17.664 0 30.165333 12.672t12.501333 30.336q0 17.322667-12.672 29.994667l-60.330667 60.330667q-12.672 12.672-29.994667 12.672-17.664 0-30.165333-12.501333t-12.501333-30.165333q0-18.005333 12.330667-30.336l60.330667-60.330667q12.672-12.672 30.336-12.672zM512 853.333333q17.664 0 30.165333 12.501333t12.501333 30.165333l0 85.333333q0 17.664-12.501333 30.165333t-30.165333 12.501333-30.165333-12.501333-12.501333-30.165333l0-85.333333q0-17.664 12.501333-30.165333t30.165333-12.501333zM42.666667 469.333333l85.333333 0q17.664 0 30.165333 12.501333t12.501333 30.165333-12.501333 30.165333-30.165333 12.501333l-85.333333 0q-17.664 0-30.165333-12.501333t-12.501333-30.165333 12.501333-30.165333 30.165333-12.501333zM512 341.333333q-70.656 0-120.661333 50.005333t-50.005333 120.661333 50.005333 120.661333 120.661333 50.005333 120.661333-50.005333 50.005333-120.661333-50.005333-120.661333-120.661333-50.005333zM783.658667 740.650667q17.322667 0 29.994667 12.672l60.330667 60.330667q12.672 12.672 12.672 30.336 0 17.322667-12.672 29.994667t-29.994667 12.672q-17.664 0-30.336-12.672l-60.330667-60.330667q-12.330667-12.330667-12.330667-29.994667t12.501333-30.336 30.165333-12.672zM180.352 137.344q17.322667 0 29.994667 12.672l60.330667 60.330667q12.672 12.672 12.672 29.994667 0 17.664-12.501333 30.165333t-30.165333 12.501333q-18.005333 0-30.336-12.330667l-60.330667-60.330667q-12.330667-12.330667-12.330667-30.336 0-17.664 12.501333-30.165333t30.165333-12.501333zM512 0q17.664 0 30.165333 12.501333t12.501333 30.165333l0 85.333333q0 17.664-12.501333 30.165333t-30.165333 12.501333-30.165333-12.501333-12.501333-30.165333l0-85.333333q0-17.664 12.501333-30.165333t30.165333-12.501333zM896 469.333333l85.333333 0q17.664 0 30.165333 12.501333t12.501333 30.165333-12.501333 30.165333-30.165333 12.501333l-85.333333 0q-17.664 0-30.165333-12.501333t-12.501333-30.165333 12.501333-30.165333 30.165333-12.501333zM843.989333 137.344q17.322667 0 29.994667 12.672t12.672 29.994667q0 17.664-12.672 30.336l-60.330667 60.330667q-12.330667 12.330667-29.994667 12.330667-18.346667 0-30.506667-12.16t-12.16-30.506667q0-17.664 12.330667-29.994667l60.330667-60.330667q12.672-12.672 30.336-12.672z'
cloud = 'path://M640 128q78.00832 0 149.17632 30.49472t122.49088 81.83808 81.83808 122.49088 30.49472 149.17632-30.49472 149.17632-81.83808 122.49088-122.49088 81.83808-149.17632 30.49472l-384 0q-69.67296 0-128.49152-34.32448t-93.16352-93.16352-34.32448-128.49152 34.32448-128.49152 93.16352-93.16352 128.49152-34.32448l21.99552 0q26.33728-74.3424 79.33952-132.15744t126.83264-90.8288 155.83232-32.99328zM640 213.34016q-55.33696 0-106.496 19.82464t-90.0096 53.84192-65.00352 81.32608-33.83296 101.00736l-88.65792 0q-70.67648 0-120.66816 49.99168t-49.99168 120.66816 49.99168 120.66816 120.66816 49.99168l384 0q60.66176 0 115.99872-23.67488t95.3344-63.67232 63.67232-95.3344 23.67488-115.99872-23.67488-115.99872-63.67232-95.3344-95.3344-63.67232-115.99872-23.67488z'
overcast = 'path://M507.252829 804.165818a31.650909 31.650909 0 0 1 31.232 27.089455l0.372364 4.701091v156.253091a31.650909 31.650909 0 0 1-31.604364 31.790545 31.650909 31.650909 0 0 1-31.185454-27.089455l-0.372364-4.70109V835.956364a31.650909 31.650909 0 0 1 31.557818-31.790546z m-240.733091-88.436363a31.976727 31.976727 0 0 1 2.978909 41.05309l-3.397818 3.909819-111.336727 110.126545a31.418182 31.418182 0 0 1-44.683637-0.418909 31.976727 31.976727 0 0 1-2.932363-41.053091l3.351273-3.909818 111.383272-110.126546a31.418182 31.418182 0 0 1 44.683637 0.465455zM755.433193 233.425455c148.340364 0 268.567273 119.621818 268.567272 267.170909 0 147.502545-120.226909 267.124364-268.567272 267.124363a268.660364 268.660364 0 0 1-119.761455-27.973818 264.424727 264.424727 0 0 1-119.808 28.485818c-146.385455 0-265.216-118.225455-265.216-264.238545 0-146.013091 118.830545-264.238545 265.216-264.238546 40.448 0 78.754909 9.029818 113.058909 25.134546a267.915636 267.915636 0 0 1 126.510546-31.464727z m-239.569455 69.957818c-111.709091 0-202.053818 89.925818-202.053818 200.610909 0 110.685091 90.391273 200.610909 202.053818 200.610909 19.828364 0 38.958545-2.792727 57.064727-8.098909a265.634909 265.634909 0 0 1-86.10909-195.956364c0-74.612364 30.813091-142.103273 80.430545-190.603636a201.774545 201.774545 0 0 0-51.386182-6.562909z m-327.214545 171.706182a31.650909 31.650909 0 0 1 31.557818 31.790545 31.744 31.744 0 0 1-26.903273 31.464727l-4.654545 0.325818H31.558284A31.650909 31.650909 0 0 1 0.000465 506.88c0-15.965091 11.682909-29.184 26.903273-31.464727l4.654546-0.325818h157.090909z m-61.765818-338.85091a31.418182 31.418182 0 0 1 44.683636-0.279272L282.903738 246.690909c12.427636 12.334545 12.567273 32.442182 0.279273 44.962909a31.418182 31.418182 0 0 1-44.637091 0.279273l-111.336727-110.778182a31.976727 31.976727 0 0 1-0.325818-44.962909zM507.252829 0a31.650909 31.650909 0 0 1 31.232 27.089455l0.372364 4.70109V188.043636a31.650909 31.650909 0 0 1-31.604364 31.790546 31.650909 31.650909 0 0 1-31.185454-27.089455l-0.372364-4.701091V31.790545A31.650909 31.650909 0 0 1 507.252829 0z'
tem = 'path://M554.666667 646.4 554.666667 384c0-23.466667-19.2-42.666667-42.666667-42.666667s-42.666667 19.2-42.666667 42.666667l0 262.4c-49.066667 17.066667-85.333333 64-85.333333 121.6 0 70.4 57.6 128 128 128s128-57.6 128-128C640 712.533333 603.733333 665.6 554.666667 646.4zM640 597.333333 640 170.666667c0-70.4-57.6-128-128-128s-128 57.6-128 128l0 426.666667c-51.2 38.4-85.333333 100.266667-85.333333 170.666667 0 117.333333 96 213.333333 213.333333 213.333333 117.333333 0 213.333333-96 213.333333-213.333333C725.333333 697.6 691.2 635.733333 640 597.333333zM512 938.666667c-93.866667 0-170.666667-76.8-170.666667-170.666667 0-64 34.133333-117.333333 85.333333-147.2L426.666667 170.666667c0-46.933333 38.4-85.333333 85.333333-85.333333s85.333333 38.4 85.333333 85.333333l0 450.133333c51.2 29.866667 85.333333 85.333333 85.333333 147.2C682.666667 861.866667 605.866667 938.666667 512 938.666667z'

# 著名景区分析
attraction = pd.read_csv("attraction_data.csv")
attrac_group = attraction.groupby('city').apply(lambda x: x[:])
attrac_zhongqiu = attrac_group[attrac_group['time'] == '周五（13日）']
zhongqiu_attrac_city = attrac_zhongqiu['city'].values.tolist()
tem_attrac = map(trans_tem, attrac_zhongqiu['tem'].values.tolist())
wea_attrac = map(check_weather, attrac_zhongqiu['wea'].values.tolist())
tem_attrac_list = list(tem_attrac)
wea_attrac_list = list(wea_attrac)

# 景区降水情况
pictorialbar = PictorialBar()
pictorialbar.add_xaxis(zhongqiu_attrac_city)
pictorialbar.add_yaxis(
    "weather", wea_attrac_list,
    label_opts=opts.LabelOpts(is_show=False),
    symbol_size=18,
    symbol_repeat="fixed",
    symbol_offset=[0, 0],
    is_symbol_clip=True,
    symbol=rain
)

pictorialbar.set_global_opts(
            title_opts=opts.TitleOpts(title="中秋节著名景区降雨情况"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30), is_show=True),
            yaxis_opts=opts.AxisOpts(
                axistick_opts=opts.AxisTickOpts(is_show=False),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(opacity=0)
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value}% 降水概率")
            ),
            datazoom_opts=opts.DataZoomOpts()
)
line = Line()
line.add_xaxis(zhongqiu_attrac_city)
line.add_yaxis("", wea_attrac_list)
pictorialbar.overlap(line)
pictorialbar.render_notebook()

# 降水和温度
bar = Bar()
bar.add_xaxis(zhongqiu_attrac_city)
bar.add_yaxis("", wea_attrac_list)
bar.extend_axis(
    yaxis=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(formatter="{value} °C"), interval=5
            )
)
bar.set_global_opts(
            title_opts=opts.TitleOpts(title="中秋节著名景区降雨和温度情况"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30), is_show=True),
            yaxis_opts=opts.AxisOpts(
                axistick_opts=opts.AxisTickOpts(is_show=False),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(opacity=0)
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value}% 降水概率")
            ),
            datazoom_opts=opts.DataZoomOpts()
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
line = Line().add_xaxis(zhongqiu_attrac_city).add_yaxis("", tem_attrac_list, yaxis_index=1)
bar.overlap(line)
bar.render_notebook()

# 降水分布图
provincial_list = provincial['provincial'].values.tolist()
geo = Geo()
geo.add_schema(maptype='china')
geo.add(
    "降水分布图",
    [list(z) for z in zip(provincial_list, weather_data_list)],
    type_=ChartType.HEATMAP
)
geo.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
geo.set_global_opts(
            visualmap_opts=opts.VisualMapOpts(range_color=['#7FFFAA', '#006400']),
            title_opts=opts.TitleOpts(title="Geo-HeatMap"),
        )
geo.render_notebook()

# 温度分布
provincial_list = provincial['provincial'].values.tolist()
geo = Geo()
geo.add_schema(maptype='china')
geo.add(
    "温度分布图",
    [list(z) for z in zip(provincial_list, tem_data)],
    type_=ChartType.HEATMAP
)
geo.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
geo.set_global_opts(
            visualmap_opts=opts.VisualMapOpts(max_=30),
            title_opts=opts.TitleOpts(title="Geo-HeatMap"),
        )
geo.render_notebook()

