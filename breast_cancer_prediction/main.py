# coding = utf-8
"""
@author: zhou
@time:2019/2/11 14:03
"""


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import svm
from sklearn import metrics


data = pd.read_csv("./breast_cancer_data-master/data.csv")
pd.set_option('display.max_columns', None)

# 分组特征字段
feature_mean = list(data.columns[2:12])
feature_se = list(data.columns[12:22])
feature_worst = list(data.columns[22:32])

# 删除ID列
data.drop("id", axis=1, inplace=True)
# 将B 良性替换为0， M恶性替换为1
data['diagnosis'] = data['diagnosis'].map({'M': 1, 'B': 0})

# 特征字段筛选
"""
sns.countplot(data['diagnosis'], label="Count")
plt.show()
# corr函数用来计算两列值的相关系数
corr = data[feature_mean].corr()
plt.figure(figsize=(14, 14))
sns.heatmap(corr, annot=True)
plt.show()
# 在热力图中，颜色越浅，代表相关性越大
# 故radius_mean、 perimeter_mean和area_mean相关性大
# compachness_mean、 concavity_mean 和 concave_points_mean相关性大
# 根据以上，做特征选择如下：
"""
# 特征选择
features_remain = ['radius_mean', 'texture_mean', 'smoothness_mean',
                   'compactness_mean', 'symmetry_mean', 'fractal_dimension_mean']

# 抽取训练集和测试集
train, test = train_test_split(data, test_size=0.3)
# 抽取特征值和分类标识
train_X = train[features_remain]
train_Y = train['diagnosis']
test_X = test[features_remain]
test_Y = test['diagnosis']

# 对数据进行规范化，保证数据在同一个量级上
# 采用Z-Score规范化数据
ss = StandardScaler()
train_X = ss.fit_transform(train_X)
test_X = ss.fit_transform(test_X)
# 使用SVM做训练，并预测
# 创建SVM分类器
model = svm.SVC()
# 训练
model.fit(train_X, train_Y)
# 预测
prediction = model.predict(test_X)
print("准确率：", metrics.accuracy_score(prediction, test_Y))


