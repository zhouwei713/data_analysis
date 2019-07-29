# -*- coding:utf-8 -*-

import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import io

# 1. 加载停用词表
stop_words_path = './text classification/stop/stopword.txt'
#with open(stop_words_path, 'r', encoding='utf-8') as sw_msg:
#with open(stop_words_path, 'r') as sw_msg:
with io.open(stop_words_path, 'r', errors='ignore') as sw_msg:  # 文档中编码有些问题，所有用errors过滤错误
 
    stop_words = [line.strip() for line in sw_msg.readlines()]
    stop_words[0] = ","     # 修改'\ufeff,' 为 ‘,’
#print(stop_words)
# print(stop_words)

# 2. 对文档进行分词
# 2.1 训练集
train_contents = []
data_list1 = [[1338, '体育'], [955, '女性'], [767, '文学'], [250, '校园']]
for j in data_list1:
    errortimes = 0
    for i in range(1, j[0]):
        path = './text classification/train/' + j[1] + '/' + str(i) + '.txt'
        try:
            #with open(path, 'r') as train_msg0:
            with io.open(path, 'r', errors='ignore') as train_msg0:  # 文档中编码有些问题，所有用errors过滤错误
                train_msg1 = train_msg0.read()
                train_cut_msg0 = jieba.cut(train_msg1)
                train_cut_msg1 = " ".join(train_cut_msg0)
            train_contents.append(train_cut_msg1)
        except Exception:
            errortimes += 1
            print(i, '.txt 文件读取错误')
            # 此处原文件体育  300.txt 读取错误  已经进入原文件删除无关代码"			$LOTOzf$"
    print(j[1], "训练集中,文件读取错误数:", errortimes)
print(train_contents)
print("训练集长度:", len(train_contents))

# 2.2 测试集
test_contents= []
data_list2 = [[1338, 1453, '体育'], [955, 993, '女性'], [767, 798, '文学'], [250, 266, '校园']]
for j in data_list2:
    errortimes = 0
    for i in range(j[0], j[1]):
        path = './text classification/test/' + j[2] + '/' + str(i) + '.txt'
        try:
            #with open(path, 'r') as test_msg0:
            with io.open(path, 'r', errors='ignore') as test_msg0:  # 文档中编码有些问题，所有用errors过滤错误
                test_msg1 = test_msg0.read()
                test_cut_msg0 = jieba.cut(test_msg1)
                test_cut_msg1 = " ".join(test_cut_msg0)
            test_contents.append(test_cut_msg1)
        except Exception:
            errortimes += 1
            print(i, '.txt 文件读取错误')
    print(j[1], "测试集中,文件读取错误数:", errortimes)
print("测试集长度:", len(test_contents))

# 3. 计算单词权重
tf = TfidfVectorizer(stop_words=stop_words, max_df=0.5)
# # 3.1 合并后拟合
# contents = train_contents + test_contents
# features = tf.fit_transform(contents)
# print('特征shape:', features.get_shape())     # (3506, 23742)
# train_features = features[:3306]
# test_features = features[3306:]

# 3.2 分开拟合
print(len(train_contents))
print(len(test_contents))
print('-'*100)
train_features = tf.fit_transform(train_contents)
print('训练集特征shape:', train_features.get_shape())   # (3306, 22893)
# 使用TfidfVectorizer初始化向量空间模型  使用训练集词袋向量
tf_test = TfidfVectorizer(stop_words=stop_words, sublinear_tf=True, max_df=0.5,
                             vocabulary=tf.vocabulary_)
test_features = tf_test.fit_transform(test_contents)
print('测试集特征shape1:', test_features.get_shape())    # (200, 2803)
#text_tf = TfidfVectorizer(stop_words=stop_words, max_df=0.5, vocabulary=tf.vocabulary_)
#test_features1 = tf.fit_transform(test_contents)
#print('测试集特征shape2:', test_features1.get_shape())    # (200, 2803)


# 4 生成分类器
train_labels = ['体育'] * 1337 + ['女性'] * 954 + ['文学'] * 766 + ['校园'] * 249
test_labels = ['体育'] * 115 + ['女性'] * 38 + ['文学'] * 31 + ['校园'] * 16
model = MultinomialNB(alpha=0.001)
model.fit(train_features, train_labels)
print(test_features.get_shape())
predict_labels = model.predict(test_features)
print(predict_labels)
score = accuracy_score(test_labels, predict_labels)
print('准确率:', score)
