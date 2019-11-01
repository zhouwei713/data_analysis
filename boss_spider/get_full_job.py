# coding = utf-8
"""
@author: zhou
@time:2019/10/24 10:36
@File: get_full_job.py
"""

# coding = utf-8
"""
@author: zhou
@time:2019/8/24 14:51
@File: main.py
"""

import re
import config
import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from save import save_to_csv

rege = r'<p>([\u4e00-\u9fa5 ]+)<em class="vline"></em>([\d+-年]+|[\u4e00-\u9fa5]+)<em class="vline"></em>([\u4e00-\u9fa5]+)'


city_code = config.city_code
Chrome_driver = webdriver.Chrome()
options = ChromeOptions()
options.add_argument(r"--user-data-dir=C:\Users\wei.zhou\AppData\Local\Google\Chrome\User Data\Default")
options.add_experimental_option('excludeSwitches', ['enable-automation'])


def get_jobs(page, city, job_type):

    Chrome_driver = webdriver.Chrome(options=options)
    c_code = city_code[city]
    for i in range(1, page + 1):

        try:
            print("正在抓取第 %s 页数据" % i)
            uri = '/%s/?query=%s&page=%s' % (c_code, job_type, i)
            Chrome_driver.get(config.url + uri)
            time.sleep(2)
            job_dict = {}
            if i == 1:
                jobs = Chrome_driver.find_element_by_xpath('//*[@id="main"]/div/div[3]/ul')
                jobs_list = jobs.find_elements_by_tag_name('li')
                for job in range(1, len(jobs_list) + 1):
                    job_details = Chrome_driver.find_element_by_xpath(
                        '//*[@id="main"]/div/div[3]/ul/li[%i]/div/div[1]/h3' % job)
                    job_details_uri = job_details.find_element_by_tag_name('a').get_attribute('href')
                    job_details_name = job_details.find_element_by_xpath(
                        '//*[@id="main"]/div/div[3]/ul/li[%i]/div/div[1]/h3/a/div[1]' % job).text
                    job_details_salary = job_details.find_element_by_xpath(
                        '//*[@id="main"]/div/div[3]/ul/li[%i]/div/div[1]/h3/a/span' % job).text

                    job_company = Chrome_driver.find_element_by_xpath(
                        '//*[@id="main"]/div/div[3]/ul/li[%i]/div/div[2]/div/h3' % job).text
                    details = Chrome_driver.find_element_by_xpath(
                        '//*[@id="main"]/div/div[3]/ul/li[%i]/div/div[1]/p' % job).get_attribute('outerHTML')
                    job_rege = re.match(rege, details)
                    job_dict['company_name'] = job_company
                    job_dict['uri'] = job_details_uri
                    job_dict['salary'] = job_details_salary
                    try:
                        job_dict['site'] = job_rege.group(1)
                        job_dict['year'] = job_rege.group(2)
                        job_dict['edu'] = job_rege.group(3)
                    except:
                        continue
                    job_dict['job_name'] = job_details_name
                    job_dict['city'] = city
                    job_dict['job_type'] = job_type

                    # save data
                    try:
                        save_to_csv(job_dict, city)
                    except:
                        raise
                    time.sleep(1)
                    print(job_dict)
            else:
                jobs = Chrome_driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/ul')
                jobs_list = jobs.find_elements_by_tag_name('li')
                for job in range(1, len(jobs_list) + 1):
                    job_details = Chrome_driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/ul/li[%i]/div/div[1]/h3' % job)
                    job_details_uri = job_details.find_element_by_tag_name('a').get_attribute('href')
                    job_details_name = job_details.find_element_by_xpath('//*[@id="main"]/div/div[2]/ul/li[%i]/div/div[1]/h3/a/div[1]' % job).text
                    job_details_salary = job_details.find_element_by_xpath('//*[@id="main"]/div/div[2]/ul/li[%i]/div/div[1]/h3/a/span' % job).text

                    job_company = Chrome_driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/ul/li[%i]/div/div[2]/div/h3' % job).text
                    details = Chrome_driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/ul/li[%i]/div/div[1]/p' % job).get_attribute('outerHTML')
                    job_rege = re.match(rege, details)
                    job_dict['company_name'] = job_company
                    job_dict['uri'] = job_details_uri
                    job_dict['salary'] = job_details_salary
                    try:
                        job_dict['site'] = job_rege.group(1)
                        job_dict['year'] = job_rege.group(2)
                        job_dict['edu'] = job_rege.group(3)
                    except:
                        continue
                    job_dict['job_name'] = job_details_name

                    job_dict['city'] = city
                    job_dict['job_type'] = job_type

                    # save data
                    try:
                        save_to_csv(job_dict, city)
                    except:
                        raise
                    time.sleep(1)
                    print(job_dict)
        except:
            raise
    Chrome_driver.close()
    time.sleep(3)


if __name__ == '__main__':
    for i in city_code.keys():
        get_jobs(10, i, 'python')
        get_jobs(10, i, 'java')
        get_jobs(10, i, '数据分析')
        get_jobs(10, i, '产品经理')



