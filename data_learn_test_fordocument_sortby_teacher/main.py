# coding = utf-8
"""
@author: zhou
@time:2019/1/31 17:42
"""

import os
from util import change_labels, get_data
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib
from sklearn import metrics

model_save_path = r'./model'
d = r'.\text_classification-master\text classification\stop'
txt = os.path.join(d, 'stopword.txt')


class Radish(object):
    def __init__(self, labels=None):
        self.labels = labels
        self.train_vocabulary = None
        self.clf = None
        self.stop_words = [line.strip() for line in open(txt, encoding='utf-8').readlines()]

    def train(self, traindir, labels):
        if not os.path.isdir(traindir):
            raise ValueError('The directory' + traindir + 'does not exist!')

        self.labels = change_labels.change_labels(labels)
        train_labels = change_labels.change_labels(self.labels)
        t_data, t_target = get_data.getdata(traindir, labels, self.stop_words)
        tv = TfidfVectorizer()
        train_data_features = tv.fit_transform(t_data)
        self.train_vocabulary = tv.vocabulary_
        clf = MultinomialNB(alpha=0.001)
        # print(train_data_features)
        print(train_labels)
        clf.fit(train_data_features, t_target)
        self.clf = clf
        save_path_name = os.path.join(model_save_path, "NB" + '.pkl')
        joblib.dump(clf, save_path_name)
        """测试开始"""
        """
        dirt = r'.\text_classification-master\text classification\test'
        test_data, test_target = get_data.gettestdata(dirt, '女性')
        tv = TfidfVectorizer(vocabulary=self.train_vocabulary)
        t_data_features = tv.fit_transform(test_data)
        predicted_label = clf.predict(t_data_features)
        print(metrics.accuracy_score(test_target, predicted_label))
        """
        print('Train finish!')

    def test(self, testdir, label):
        if not os.path.isdir(testdir):
            raise ValueError('The directory' + testdir + 'does not exist!')

        self.labels = change_labels.change_labels(label)
        test_data, test_target = get_data.gettestdata(testdir, label, self.stop_words)
        tv = TfidfVectorizer(sublinear_tf=True, vocabulary=self.train_vocabulary)
        t_data_features = tv.fit_transform(test_data)
        # clf = joblib.load(model_save_path + "NB" + '.pkl')
        clf = self.clf
        predicted_label = clf.predict(t_data_features)
        print("%s准确率：" % label, metrics.accuracy_score(test_target, predicted_label))


if __name__ == "__main__":
    labels = ['女性', '体育', '文学', '校园']
    dirf = r'.\text_classification-master\text classification\train'
    dirt = r'.\text_classification-master\text classification\test'
    r = Radish()
    r.train(dirf, labels)
    r.test(dirt, '女性')
    r.test(dirt, '体育')
    r.test(dirt, '文学')
    r.test(dirt, '校园')

