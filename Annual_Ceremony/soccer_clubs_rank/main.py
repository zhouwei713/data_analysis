# coding = utf-8
"""
@author: zhou
@time:2020/1/13 10:10
@File: main.py
"""

from get_clubs_name import get_clubs_name
from get_clubs_rank_his import get_clubs_rank_his


if __name__ == '__main__':
    for i in range(1, 5):
        # url = 'https://footballdatabase.com/ranking/world/%s' % str(i)
        # url = 'https://footballdatabase.com/ranking/asia/%s' % str(i)
        # url = 'https://footballdatabase.com/ranking/africa/%s' % str(i)
        url = 'https://footballdatabase.com/ranking/south-america/%s' % str(i)

        print('fire url %s' % url)
        clubs_name = get_clubs_name(url)
        get_clubs_rank_his(clubs_name)
