# encoding: utf-8

"""
@version: ??
@author: Andy
@file: auto_appium.py
@time: 20/2/21 11:49
"""

from appium import webdriver
import time


desired_caps = {
                "platformName": "Android",
                "deviceName": "V1838A",
                "appPackage": "com.bbk.appstore",
                "appActivity": "com.bbk.appstore.ui.AppStore",
                "noReset": "true",
                "fullReset": "false"
}
server = 'http://localhost:4723/wd/hub'
driver = webdriver.Remote(server, desired_caps)
time.sleep(4)

# 点击搜索框
search_page = driver.find_element_by_id('com.bbk.appstore:id/search_box').click()
time.sleep(1)
search_ele = driver.find_element_by_id('com.bbk.appstore:id/search_input')
time.sleep(1)
# 输入搜索字段
search_ele.send_keys(u'dingding')
time.sleep(1)
# 点击钉钉 app
driver.find_element_by_xpath('(//android.widget.ImageView[@content-desc="应用商店"])[1]').click()
time.sleep(1)
# 点击"更多"
driver.find_element_by_id('com.bbk.appstore:id/appstore_detail_explicit_comment_more').click()
time.sleep(4)

point1 = '[48,957][1032,1047]'

point2 = '[48,1353][1032,1946]'

point3 = '[48,1947][1032,2181]'

print('use swipe')
driver.swipe(48, 1947, 48, 350)
time.sleep(1)
# driver.swipe(48, 1353, 48, 957)


# while True:
#     driver.swipe(48, 1947, 48, 957, 500)
#     break

time.sleep(5)

star1 = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[1]/android.widget.FrameLayout/android.widget.LinearLayout[1]/android.widget.RelativeLayout[2]/android.support.v4.view.ViewPager/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.LinearLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout'
star2 = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[1]/android.widget.FrameLayout/android.widget.LinearLayout[1]/android.widget.RelativeLayout[2]/android.support.v4.view.ViewPager/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.LinearLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout'
star3 = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[1]/android.widget.FrameLayout/android.widget.LinearLayout[1]/android.widget.RelativeLayout[2]/android.support.v4.view.ViewPager/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.LinearLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout'