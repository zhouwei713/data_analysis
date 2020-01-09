# coding = utf-8
"""
@author: zhou
@time:2020/1/7 10:50
@File: main.py
"""

from fontTools.ttLib import TTFont


font = TTFont('727b43f14df462a976ff249736eb28282276.woff')  # 打开当前目录的 .woff 文件
font.saveXML('font1.xml')  # 另存为 xml

font = TTFont('292e237c7d76c1c462ed99a8384721d22280.woff')  # 打开当前目录的 .woff 文件
font.saveXML('font2.xml')  # 另存为 xml
