# coding = utf-8
"""
@author: zhou
@time:2019/2/14 11:10
"""

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_digits
from sklearn.neighbors import  KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from matplotlib.pylab import plt


def load_data():
    digits = load_digits()
    data = digits.data
    """
    展示图片
    plt.gray()
    plt.imshow(digits.images[13])
    plt.show()
    """
    train_x, test_x, train_y, test_y = train_test_split(data, digits.target, test_size=0.2, random_state=33)
    ss = StandardScaler()
    train_ss_x = ss.fit_transform(train_x)
    test_ss_x = ss.fit_transform(test_x)
    mm = MinMaxScaler()
    train_mm_x = mm.fit_transform(train_x)
    test_mm_x = mm.fit_transform(test_x)
    return train_ss_x, train_mm_x, train_y, test_ss_x, test_mm_x, test_y


def knn_predict(train_x, train_y, test_x, test_y, k=5):
    knn = KNeighborsClassifier(k)
    knn.fit(train_x, train_y)
    knn_predict_y = knn.predict(test_x)
    print("KNN准确率：", accuracy_score(knn_predict_y, test_y))


def svm_predict(train_x, train_y, test_x, test_y):
    svm = SVC()
    svm.fit(train_x, train_y)
    svm_predict_y = svm.predict(test_x)
    print("SVM准确率：", accuracy_score(svm_predict_y, test_y))


def nb_predict(train_x, train_y, test_x, test_y):
    nb = MultinomialNB()
    nb.fit(train_x, train_y)
    nb_predict_y = nb.predict(test_x)
    print("NB准确率：", accuracy_score(nb_predict_y, test_y))


def dtc_predict(train_x, train_y, test_x, test_y):
    dtc = DecisionTreeClassifier()
    dtc.fit(train_x, train_y)
    dtc_predict_y = dtc.predict(test_x)
    print("CART准确率：", accuracy_score(dtc_predict_y, test_y))


if __name__ == "__main__":
    train_ss_x, train_mm_x, train_y, test_ss_x, test_mm_x, test_y = load_data()
    knn_predict(train_ss_x, train_y, test_ss_x, test_y, 6)
    svm_predict(train_ss_x, train_y, test_ss_x, test_y)
    nb_predict(train_mm_x, train_y, test_mm_x, test_y)
    dtc_predict(train_mm_x, train_y, test_mm_x, test_y)
