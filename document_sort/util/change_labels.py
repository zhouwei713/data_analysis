# coding = utf-8
"""
@author: zhou
@time:2019/1/31 18:44
"""


labels = ['女性', '体育', '文学', '校园']


def change_labels(labels):
    label_indices = {lab: i for i, lab in enumerate(labels)}
    index = []
    for lab in labels:
        index.append(label_indices[lab])
    return label_indices


if __name__ == "__main__":
    c = change_labels(labels)
    print(c)
