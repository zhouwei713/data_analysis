# coding = utf-8
"""
@author: zhou
@time:2019/2/15 15:41
"""

from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import pandas as pd


def zuqiu_kmeans(n):
    data = pd.read_csv('data.csv', encoding='gbk')
    # print(data)
    train_x = data[['2019年国际排名', '2018世界杯', '2015亚洲杯']]
    # 初始化KMeans
    kmeans = KMeans(n_clusters=n)
    # 规范化数据
    min_max_scaler = MinMaxScaler()
    train_x = min_max_scaler.fit_transform(train_x)
    kmeans.fit(train_x)
    predict_y = kmeans.predict(train_x)
    # 将结果插回到原数据中
    result = pd.concat((data, pd.DataFrame(predict_y)), axis=1)
    result.rename({0: u'聚类结果'}, axis=1, inplace=True)
    print(result)


if __name__ == "__main__":
    zuqiu_kmeans(4)
