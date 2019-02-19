# coding = utf-8
"""
@author: zhou
@time:2019/2/19 14:20
"""

from PIL import Image
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from sklearn.cluster import KMeans
from skimage import color


def load_data(filepath):
    f = open(filepath, 'rb')
    data = []
    img = Image.open(f)
    width, height = img.size
    for x in range(width):
        for y in range(height):
            c1, c2, c3 = img.getpixel((x, y))  # 获取每个点的像素值，即RGB值
            data.append([c1, c2, c3])
    f.close()
    mm = MinMaxScaler()
    data = mm.fit_transform(data)
    return np.mat(data), width, height


def KMeans_pic():
    img, width, height = load_data('baby.jpg')
    kmeans = KMeans(n_clusters=2)
    kmeans.fit(img)
    label = kmeans.predict(img)
    print("1", label)
    label = label.reshape([width, height])  # 将图像的聚类结果转化成图像尺寸的矩阵
    print("2", label)
    # 创建一个新图像 pic_mark， 用来保存图像聚类的结果，并设置不同的灰度值
    pic_mark = Image.new("L", (width, height))  # 创建单通道的同大小图像
    for x in range(width):
        for y in range(height):
            pic_mark.putpixel((x, y), int(256/(label[x][y]+1))-1)  # 类别为0的灰度值设置为255，1的设置为127
    pic_mark.save("new_mark.jpg", "JPEG")


def KMeans_pic16():
    img, width, height = load_data('baby.jpg')
    kmeans = KMeans(n_clusters=16)
    kmeans.fit(img)
    label = kmeans.predict(img)
    print("1", label)
    label = label.reshape([width, height])
    label_color = (color.label2rgb(label)*255).astype(np.uint8)
    label_color = label_color.transpose(1, 0, 2)
    images = Image.fromarray(label_color)
    images.save('color_mark.jpg')


if __name__ == "__main__":
    KMeans_pic16()