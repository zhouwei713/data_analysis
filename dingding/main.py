# encoding: utf-8

"""
@version: ??
@author: Andy
@file: main.py
@time: 20/2/19 12:58
"""


from selenium import webdriver
from selenium.webdriver import ChromeOptions
import time
import os



options = ChromeOptions()
# options.add_argument(r"--user-data-dir=C:\Users\wei.zhou\AppData\Local\Google\Chrome\User Data\Default")
url = 'https://apps.apple.com/cn/app/%E9%92%89%E9%92%89/id930368978#see-all/reviews'


def get_data():
    Chrome_driver = webdriver.Chrome(options=options)
    try:
        Chrome_driver.get(url)
        time.sleep(5)
        print('start scroll')
        step = 0
        while True:
            if step <= 500:
                print('step:', step)
                Chrome_driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                time.sleep(5)
            else:
                break
            step += 1
        print('end scroll')
        print('start to save data!')
        for i in range(1, 20000):
            comment_dict = {}
            message_div = Chrome_driver.find_element_by_xpath('/html/body/div[4]/div/main/div/div/div/section/div[2]/div[%s]' % i)
            inner_message = message_div.find_element_by_css_selector('.we-customer-review.lockup.ember-view')
            score = inner_message.find_element_by_tag_name('figure').get_attribute('aria-label')
            user_info = inner_message.find_element_by_css_selector('.we-customer-review__header.we-customer-review__header--user')
            username = user_info.find_element_by_css_selector('.we-truncate.we-truncate--single-line.ember-view.we-customer-review__user').text
            uptime = user_info.find_element_by_tag_name('time').text
            title = inner_message.find_element_by_tag_name('h3').text
            content = inner_message.find_element_by_tag_name('blockquote').find_element_by_tag_name('div').find_element_by_tag_name('p').text
            comment_dict['score'] = score
            comment_dict['username'] = username
            comment_dict['time'] = uptime
            comment_dict['title'] = title
            comment_dict['content'] = content
            print('score', score)
            print('userName', username)
            print('time', uptime)
            print('title', title)
            print('content', content)
            save_data_to_csv(comment_dict)
        Chrome_driver.close()
    except Exception as e:
        print(e)
        Chrome_driver.close()


def save_data_to_csv(d):
    if not os.path.exists('appstore_data1.csv'):
        with open('appstore_data1.csv', 'a+', encoding='utf-8') as f:
            f.write('score|username|time|title|content\n')
            try:
                row = '{}|{}|{}|{}|{}'.format(
                    d['score'],
                    d['username'],
                    d['time'],
                    d['title'],
                    d['content'])
                f.write(row)
                f.write('\n')
            except:
                pass
    else:
        with open('appstore_data1.csv', 'a+', encoding='utf-8') as f:
            try:
                row = '{}|{}|{}|{}|{}'.format(
                    d['score'],
                    d['username'],
                    d['time'],
                    d['title'],
                    d['content'])
                f.write(row)
                f.write('\n')
            except:
                pass


if __name__ == '__main__':
    get_data()
