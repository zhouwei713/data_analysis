# coding = utf-8
"""
@author: zhou
@time:2019/11/13 15:00
@File: main.py
"""

import pandas as pd
from pyecharts.charts import Scatter
import sklearn.pipeline as pl
import sklearn.linear_model as lm
import sklearn.preprocessing as sp
import matplotlib.pyplot as mp
import numpy as np


gdp = pd.read_csv('GDP_data.csv')
country = pd.read_csv('Country_data.csv')
country_data = country.dropna(subset=['Income_Group'])
country_gdp = pd.merge(country_data, gdp, how='inner')

# 美国GDP
df_usa = country_gdp[country_gdp['Country Name']=='美国']
for i in range(1960, 2019):
    df_usa[str(i)] = df_usa[str(i)].apply(lambda x: x/1000000000000)

# 中国GDP
df_china = country_gdp[country_gdp['Country Name']=='中国']
for i in range(1960, 2019):
    df_china[str(i)] = df_china[str(i)].apply(lambda x: x/1000000000000)

# 日本GDP
df_jpn = country_gdp[country_gdp['Country Name']=='日本']
for i in range(1960, 2019):
    df_jpn[str(i)] = df_jpn[str(i)].apply(lambda x: x/1000000000000)


# 德国GDP
df_de = country_gdp[country_gdp['Country Name']=='德国']
for i in range(1960, 2019):
    df_de[str(i)] = df_de[str(i)].apply(lambda x: x/1000000000000)

# 英国GDP
df_uk = country_gdp[country_gdp['Country Name']=='英国']
for i in range(1960, 2019):
    df_uk[str(i)] = df_uk[str(i)].apply(lambda x: x/1000000000000)

# 处理数据
year_str = [str(i) for i in range(1960, 2019)]

china_gdp = df_china[year_str].values.tolist()[0]
usa_gdp = df_usa[year_str].values.tolist()[0]
jpn_gdp = df_jpn[year_str].values.tolist()[0]
de_gdp = df_de[year_str].values.tolist()[0]
uk_gdp = df_uk[year_str].values.tolist()[0]


# 制作散点图
def scatter_base(choose, values, country) -> Scatter:
    c = (
        Scatter()
        .add_xaxis(choose)
        .add_yaxis("%s历年GDP" % country, values)
        .set_global_opts(title_opts=opts.TitleOpts(title=""),
                        # datazoom_opts=opts.DataZoomOpts(),
                         yaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(formatter="{value} /万亿")
            )
                        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )
    return c


# jupyter notebook
scatter_base(year_str, usa_gdp, '美国').render_notebook()
scatter_base(year_str, china_gdp, '中国').render_notebook()
scatter_base(year_str, jpn_gdp, '日本').render_notebook()
scatter_base(year_str, de_gdp, '德国').render_notebook()
scatter_base(year_str, uk_gdp, '英国').render_notebook()

# 拟合数据-美国
year = [i for i in range(1960, 2019)]
X = np.array(year)
X = X.reshape(-1, 1)
y = usa_gdp
model = pl.make_pipeline(
    sp.PolynomialFeatures(5),  # 多项式特征拓展器
    lm.LinearRegression()  # 线性回归器
)
# 训练模型
model.fit(X, y)
# 求预测值y
pred_y = model.predict(X)

# 绘制多项式回归线
px = np.linspace(X.min(), X.max(), 1000)
px = px.reshape(-1, 1)
pred_py = model.predict(px)

# 绘制图像
mp.figure("美国历年GDP拟合结果", facecolor='lightgray')
mp.title('USA GDP Regression', fontsize=16)
mp.tick_params(labelsize=10)
mp.grid(linestyle=':')
mp.xlabel('x')
mp.ylabel('y')

mp.scatter(X, y, s=60, marker='o', c='dodgerblue', label='Points')
mp.plot(px, pred_py, c='orangered', label='PolyFit Line')
mp.tight_layout()
mp.legend()
mp.show()

# 预测2019年数据
p_year = [i for i in range(1960, 2020)]
p_X = np.array(p_year)
p_X = p_X.reshape(-1, 1)
p_pred_y = model.predict(p_X)

