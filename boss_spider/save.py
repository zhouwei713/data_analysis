# coding = utf-8
"""
@author: zhou
@time:2019/10/24 14:27
@File: save.py
"""
import os


def save_to_csv(data, file_name):
    filename = file_name + '_data.csv'
    if not os.path.exists(filename):
        with open(filename, 'a+', encoding='utf-8') as f:
            f.write('company_name,uri,salary,site,year,edu,job_name,city,job_type\n')
            try:
                row = '{},{},{},{},{},{},{},{},{}'.format(data['company_name'],
                                                           data['uri'],
                                                           data['salary'],
                                                           data['site'],
                                                           data['year'],
                                                           data['edu'],
                                                           data['job_name'],
                                                           data['city'],
                                                           data['job_type'])
                f.write(row)
                f.write('\n')
            except:
                pass
    else:
        with open(filename, 'a+', encoding='utf-8') as f:
            try:
                row = '{},{},{},{},{},{},{},{},{}'.format(data['company_name'],
                                                          data['uri'],
                                                          data['salary'],
                                                          data['site'],
                                                          data['year'],
                                                          data['edu'],
                                                          data['job_name'],
                                                          data['city'],
                                                          data['job_type'])
                f.write(row)
                f.write('\n')
            except:
                pass