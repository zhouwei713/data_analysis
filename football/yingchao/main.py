# coding = utf-8
"""
@author: zhou
@time:2019/10/7 16:49
@File: main.py
"""

import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ChromeOptions
import time
import re
import numpy as np


session = {
        'dqduid': 'eyJpdiI6InF4UGh5aG5wNVQ1aDFvVGZkeTR5eU16aHVJYk5RN1RVVHptU210c3pra0U9IiwidmFsdWUiOiIrcXlQa3pmNGhaSkVHN3RvZ3ZyUVhuT0VBdTdYcEhrQ01EaEFTNW5heFY0QmZod0x0dlwvUFwvczc1TGQ0NERNVERcL21USUdCeDFYT1dQT3R1eTNaVXBiZz09IiwibWFjIjoiMWM2Y2ZmMWU3MDcyMWQwNTEwZGJjM2RlNDkyODMyYjI0ZjY1Y2MwODAxMTVmY2U2YmMwZmQ0MTRlYjMxOWE0YSJ9'}
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win32; x32; rv:54.0) Gecko/20100101 Firefox/54.0', 'Connection': 'keep-alive'}
Chrome_driver = webdriver.Chrome()
options = ChromeOptions()
options.add_argument(r"--user-data-dir=C:\Users\wei.zhou\AppData\Local\Google\Chrome\User Data\Default")


def get_team_data():
    qiudui_url = 'https://www.dongqiudi.com/data?competition=8'
    qiudui_res = requests.get(qiudui_url, headers=header, cookies=session).text
    content = BeautifulSoup(qiudui_res, 'html.parser')
    team_content = content.find('table').find_all('tr')
    team_list = list(map(deal_element_list, team_content[2:]))
    save_to_csv(team_list)
    print('get player data now...')
    for i in team_list:
        print("爬取url：", i[0])
        get_players_urls(i[0])


def get_players_urls(u):
    Chrome_driver = webdriver.Chrome(options=options)
    u = u
    Chrome_driver.get(u)
    ele_div = Chrome_driver.find_element_by_xpath('//*[@id="__layout"]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[2]')
    ele_p = ele_div.find_elements_by_tag_name('p')

    for i in range(1, len(ele_p) + 1):
        data_dict = {}
        if Chrome_driver.find_element_by_xpath(
                '//*[@id="__layout"]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[2]/p[%i]/a/span[1]' % (i)).text != '教练':
            Chrome_driver.find_element_by_xpath(
                '//*[@id="__layout"]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[2]/p[%i]/a/span[1]' % (i)).click()
            time.sleep(3)
            Chrome_driver.switch_to.window(Chrome_driver.window_handles[-1])
            data_dict['姓名'] = Chrome_driver.find_element_by_xpath(
                '//*[@id="__layout"]/div/div[2]/div[2]/div[1]/div[1]/div/p[1]').text
            div = Chrome_driver.find_element_by_xpath('//*[@id="__layout"]/div/div[2]/div[2]/div[1]/div[1]/div/div')
            uls = div.find_elements_by_tag_name('ul')
            for ul in uls:
                lis = ul.find_elements_by_tag_name('li')
                for li in lis:
                    ziduan = re.search(r'(.*?)：', li.find_element_by_tag_name('span').text).group(1)
                    try:
                        data_dict[ziduan] = re.search(r'：(.*)', li.text).group(1)
                    except:
                        data_dict[ziduan] = np.nan
            try:
                div2 = Chrome_driver.find_element_by_xpath('//*[@id="__layout"]/div/div[2]/div[2]/div[2]/div[1]')
                data_dict['综合得分'] = div2.find_element_by_tag_name('p').find_element_by_tag_name('b').text
                div3 = Chrome_driver.find_element_by_xpath('//*[@id="__layout"]/div/div[2]/div[2]/div[2]/div[1]/div[1]')
                divs = div3.find_elements_by_tag_name('div')
                for d in divs[1:]:
                    ziduan = re.search(r'(.*)\s', d.text).group(1)
                    try:
                        data_dict[ziduan] = d.find_element_by_tag_name('span').text
                    except:
                        data_dict[ziduan] = np.nan
            except:
                pass
            print(data_dict)
            Chrome_driver.close()
            Chrome_driver.switch_to.window(Chrome_driver.window_handles[-1])
            save_data_to_csv(data_dict)
    Chrome_driver.close()
    time.sleep(3)


def deal_element_list(ele):
    team_url = ele.find('a')['href']
    team = ele.find_all('td')[1].text.strip()
    win = ele.find_all('td')[3].text
    deuce = ele.find_all('td')[4].text
    loss = ele.find_all('td')[5].text
    goal = ele.find_all('td')[6].text
    loss_goal = ele.find_all('td')[7].text
    goal_diff = ele.find_all('td')[8].text
    return [team_url, team, win, deuce, loss, goal, loss_goal, goal_diff]


def save_to_csv(data):
    if not os.path.exists('yingchao_data.csv'):
        with open('yingchao_data.csv', 'a+', encoding='utf-8') as f:
            f.write('url,team,win,deuce,loss,goal,loss_goal,goal_diff\n')
            for d in data:
                try:
                    row = '{},{},{},{},{},{},{},{}'.format(d[0],
                                                        d[1],
                                                        d[2],
                                                        d[3],
                                                        d[4],
                                                        d[5],
                                                        d[6],
                                                        d[7])
                    f.write(row)
                    f.write('\n')
                except:
                    continue
    else:
        with open('yingchao_data.csv', 'a+', encoding='utf-8') as f:
            for d in data:
                try:
                    row = '{},{},{},{},{},{},{},{}'.format(d[0],
                                                        d[1],
                                                        d[2],
                                                        d[3],
                                                        d[4],
                                                        d[5],
                                                        d[6],
                                                        d[7])
                    f.write(row)
                    f.write('\n')
                except:
                    continue


def save_data_to_csv(d):
    if not os.path.exists('player_data.csv'):
        with open('player_data.csv', 'a+', encoding='utf-8') as f:
            f.write('name,club,nation,height,staff,age,weight,number,birth,foot,score,speed,power,defend,tape,pass,shot\n')
            try:
                row = '{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(
                    d['姓名'],
                    d['俱乐部'],
                    d['国 籍'],
                    d['身 高'],
                    d['位 置'],
                    d['年 龄'],
                    d['体 重'],
                    d['号 码'],
                    d['生 日'],
                    d['惯用脚'],
                    d['综合得分'],
                    d['速度'],
                    d['力量'],
                    d['防守'],
                    d['盘带'],
                    d['传球'],
                    d['射门'])
                f.write(row)
                f.write('\n')
            except:
                pass
    else:
        with open('player_data.csv', 'a+', encoding='utf-8') as f:
            try:
                row = '{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(
                    d['姓名'],
                    d['俱乐部'],
                    d['国 籍'],
                    d['身 高'],
                    d['位 置'],
                    d['年 龄'],
                    d['体 重'],
                    d['号 码'],
                    d['生 日'],
                    d['惯用脚'],
                    d['综合得分'],
                    d['速度'],
                    d['力量'],
                    d['防守'],
                    d['盘带'],
                    d['传球'],
                    d['射门'])
                f.write(row)
                f.write('\n')
            except:
                pass


if __name__ == '__main__':
    get_team_data()
