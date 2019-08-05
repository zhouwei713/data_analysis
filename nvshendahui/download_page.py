# coding = utf-8
"""
@author: zhou
@time:2019/8/2 16:21
@File: download_page.py
"""

import config
import requests


class DownloadPage(object):
    def getHtml(self, url):
        html = requests.get(url=url, cookies=config.session, headers=config.header).content
        return html

    def saveHtml(self, file_name, file_content):
        with open('html_page/' + file_name + '.html', 'wb') as f:
            f.write(file_content)
