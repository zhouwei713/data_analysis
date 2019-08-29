# coding = utf-8
"""
@author: zhou
@time:2019/8/24 10:40
@File: main.py
"""

from selenium import webdriver
import time

url = 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.34.52492beaOFMybH&id=584463337905&skuId=3946055512563&user_id=196993935&cat_id=2&is_b=1&rn=6a5950121999b109beea9dd17a7dd0d4'

option = webdriver.ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])

browser = webdriver.Chrome(options=option)
browser.get(url)
print(browser)
browser.implicitly_wait(30)
time.sleep(5)
iframe = browser.find_element_by_class_name("sufei-dialog-content")
print(iframe)
browser.switch_to.frame(0)
print(browser)
# browser.switch_to.frame("sufei-dialog-content")
close_ele = browser.find_element_by_class_name("sufei-dialog-close")
print(close_ele)
# browser.find_element_by_class_name('sufei-dialog-content').find_element_by_class_name('sufei-dialog-close').click()


if __name__ == '__main__':
    pass
