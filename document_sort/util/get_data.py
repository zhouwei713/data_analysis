# coding = utf-8
"""
@author: zhou
@time:2019/1/31 17:03
"""
import os
import io
import jieba


directory = "".join(os.getcwd())
dirf = r'..\text_classification-master\text classification\train'
dirt = r'..\text_classification-master\text classification\test'


def change_labels(labels):
    label_indices = {lab: i for i, lab in enumerate(labels)}
    index = []
    for lab in labels:
        index.append(label_indices[lab])
    return label_indices


def getdata(dirname, labels, stopword):
    data_x = []
    data_y = []
    index = change_labels(labels)
    all = open('all.csv', 'a', encoding='gb18030')
    for i in labels:
        files = {filename for filename in os.listdir(dirname + r'\\' + i)}
        for fname in files:
            with io.open(os.path.join(dirname + r'\\' + i) + r'\\' + fname, 'r', encoding='gb18030') as f:
                text = f.read()
                rowcsv = '{},{}'.format(text.strip().replace('\n', '').replace('\r', ''), index[i])
                all.write(rowcsv)
                all.write('\n')
    all.close()
    with open('all.csv', 'r', encoding='gb18030') as f:
        for line in f:
            newline = line.replace('\n', '')
            seglist = jieba.cut(newline[:-2])
            for word in seglist:
                if word not in stopword:
                    feature = ' '.join(seglist)
                    data_x .append(feature)
                    data_y.append(newline[-1])
    return data_x, data_y


def gettestdata(dirname, label, stopword):
    test_data = []
    test_target = []
    labels = ['女性', '体育', '文学', '校园']
    index = change_labels(labels)
    all_test = open('alltest%s.csv' % index[label], 'a', encoding='gb18030')
    files = {filename for filename in os.listdir(dirname + r'\\' + label)}
    for fname in files:
        with io.open(os.path.join(dirname + r'\\' + label) + r'\\' + fname, 'r', encoding='gb18030') as f:
            text = f.read()
            rowcsv = '{},{}'.format(text.strip().replace('\n', '').replace('\r', ''), index[label])
            all_test.write(rowcsv)
            all_test.write('\n')
    all_test.close()
    with open('alltest%s.csv' % index[label], 'r', encoding='gb18030') as f:
        for line in f:
            newline = line.replace('\n', '')
            seglist = jieba.cut(newline[:-2])
            for word in seglist:
                if word not in stopword:
                    test_feature = ' '.join(seglist)
                    test_data .append(test_feature)
                    test_target.append(newline[-1])
    return test_data, test_target


if __name__ == "__main__":
    d = r'..\text_classification-master\text classification\stop'
    txt = os.path.join(d, 'stopword.txt')
    stop = [line.strip() for line in open(txt, encoding='utf-8').readlines()]
    # labels = ['女性', '体育', '文学', '校园']
    labels = ['女性', '体育', '文学', '校园']
    f, l = getdata(dirf, labels, stop)
    print(f)
    print(type(f))
    print(l)
    print(type(l))
