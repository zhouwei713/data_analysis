# coding = utf-8
"""
@author: zhou
@time:2019/8/3 16:29
@File: tools.py
"""


import re
import requests
import os
import time


def get_picture(c, t_list, n_id_p):
    # print("进入get_picture函数:")
    nvshen_l = []
    tmp_prev_id = c.find_all('a', attrs={"target": "_self"})
    for j in tmp_prev_id:
        if '期' in j.string:
            href_list = j['href'].split('/')
            tmp_id = re.findall(r"\d+\.?\d*", href_list[-1])
            if len(tmp_id) == 1:
                prev_nvshen_id = tmp_id[0]
                t_list.append(prev_nvshen_id)
                for n in n_id_p:
                    for k, v in n.items():
                        if k == prev_nvshen_id:
                            t_list.append(v)
                            nvshen_l.append(t_list)
                            # print("get_picture函数结束")
                            return nvshen_l
                        else:
                            pass
            else:
                raise


def save_to_file(nvshen_list, filename):
    with open(filename + '.csv', 'w', encoding='utf-8') as output:
        output.write('name,count,score,weight_score,page_id,picture\n')
        for row in nvshen_list:
            try:
                print("开始下载图片...")
                save_pic(row[-1], row[0])
                time.sleep(2)
                print("图片下载完成")
                weight = int(''.join(list(filter(str.isdigit, row[1])))) / 1000
                weight_2 = float(row[3]) + float('%.2f' % weight)
                weight_score = float('%.2f' % weight_2)
                rowcsv = '{},{},{},{},{},{}'.format(row[0], row[1], row[3], weight_score, row[4], row[5])
                output.write(rowcsv)
                output.write('\n')
            except:
                raise


def save_pic(url, nick_name):
    resp = requests.get(url)
    if not os.path.exists('picture'):
        os.mkdir('picture')
    if resp.status_code == 200:
        with open('picture' + f'/{nick_name}.jpg', 'wb') as f:
            f.write(resp.content)
