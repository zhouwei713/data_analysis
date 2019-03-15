# coding = utf-8
"""
@author: zhou
@time:2019/3/4 14:34
"""


import requests
from bs4 import BeautifulSoup


def get_hero_url():
    print('start to get hero urls')
    url = 'http://db.18183.com/'
    url_list = []
    res = requests.get(url + 'wzry').text
    content = BeautifulSoup(res, "html.parser")
    ul = content.find('ul', attrs={'class': "mod-iconlist"})
    hero_url = ul.find_all('a')
    for i in hero_url:
        url_list.append(i['href'])
    print('finish get hero urls')
    return url_list


def get_details(url):
    print('start to get details')
    base_url = 'http://db.18183.com/'
    detail_list = []
    for i in url:
        # print(i)
        res = requests.get(base_url + i).text
        content = BeautifulSoup(res, "html.parser")
        name_box = content.find('div', attrs={'class': 'name-box'})
        name = name_box.h1.text
        hero_attr = content.find('div', attrs={'class': 'attr-list'})
        attr_star = hero_attr.find_all('span')
        survivability = attr_star[0]['class'][1].split('-')[1]
        attack_damage = attr_star[1]['class'][1].split('-')[1]
        skill_effect = attr_star[2]['class'][1].split('-')[1]
        getting_started = attr_star[3]['class'][1].split('-')[1]
        details = content.find('div', attrs={'class': 'otherinfo-datapanel'})
        # print(details)
        attrs = details.find_all('p')
        attr_list = []
        for attr in attrs:
            attr_list.append(attr.text.split('：')[1].strip())
        detail_list.append([name, survivability, attack_damage,
                            skill_effect, getting_started, attr_list])
    print('finish get details')
    return detail_list


def save_tocsv(details):
    print('start save to csv')
    with open('all_hero_init_attr.csv', 'w', encoding='gb18030') as f:
        f.write('英雄名字,生存能力,攻击伤害,技能效果,上手难度,最大生命,最大法力,物理攻击,'
                '法术攻击,物理防御,物理减伤率,法术防御,法术减伤率,移速,物理护甲穿透,法术护甲穿透,攻速加成,暴击几率,'
                '暴击效果,物理吸血,法术吸血,冷却缩减,攻击范围,韧性,生命回复,法力回复\n')
        for i in details:
            try:
                rowcsv = '{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(
                    i[0], i[1], i[2], i[3], i[4], i[5][0], i[5][1], i[5][2], i[5][3], i[5][4], i[5][5],
                    i[5][6], i[5][7], i[5][8], i[5][9], i[5][10], i[5][11], i[5][12], i[5][13], i[5][14], i[5][15],
                    i[5][16], i[5][17], i[5][18], i[5][19], i[5][20]
                )
                f.write(rowcsv)
                f.write('\n')
            except:
                continue
    print('finish save to csv')


if __name__ == "__main__":
    get_hero_url()
    hero_url = get_hero_url()
    # hero_url = ['/wzry/hero/16076.html', '/wzry/hero/16045.html', '/wzry/hero/13004.html']
    details = get_details(hero_url)
    save_tocsv(details)
