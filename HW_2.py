from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import pandas as pd
import re

# 1) Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы) с сайта superjob.ru и hh.ru.
# Приложение должно анализировать несколько страниц сайта(также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
# *Наименование вакансии
# *Предлагаемую зарплату (отдельно мин. отдельно макс. и отдельно валюту)
# *Ссылку на саму вакансию
# *Сайт откуда собрана вакансия
# По своему желанию можно добавить еще работодателя и расположение. Данная структура должна быть одинаковая для вакансий с
# обоих сайтов.
# Общий результат можно вывести с помощью dataFrame через pandas.


vacancy_name = 'python'
hh_link = 'https://hh.ru'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'}
strs = 39

def hh_parser(vacancy_name, hh_link, header, strs):
    global salary_max, salary_min, salary_currency
    html = requests.get(hh_link+'/search/vacancy?clusters=true&enable_snippets=true&text='+vacancy_name+'&showClusters=true',headers=header).text
    soup = bs(html,'lxml')
    jobs = []
    for i in range(strs):
        hh_block = soup.find('div', {'class': 'vacancy-serp'})
        vacancy_list = hh_block.find_all('div', {'class': 'vacancy-serp-item'})
        for job in vacancy_list:
            jobs_data = {}
            job_name = job.find('span',{'class':'g-user-content'}).getText()
            a = job.find('span', {'class': 'g-user-content'}).findChild()
            link = a['href']
            salary = job.find('div',{'class':'vacancy-serp-item__sidebar'})
            if not salary:
                salary_min = None
                salary_max = None
                salary_currency = None
            else:
                salary = salary.getText().replace(u'\xa0', u'')
                salary = re.split(r'\s|-', salary)
                if len(salary)>1:
                    if salary[0] == 'до':
                        salary_min = None
                        salary_max = int(salary[1])
                        salary_currency = salary[2]
                    elif salary[0] == 'от':
                        salary_min = int(salary[1])
                        salary_max = None
                        salary_currency = salary[2]
                    else:
                        salary_min = int(salary[0])
                        salary_max = int(salary[1])
                        salary_currency = salary[2]
            jobs_data['job_name'] = job_name
            jobs_data['slary_min'] = salary_min
            jobs_data['slary_max'] = salary_max
            jobs_data['currency'] = salary_currency
            jobs_data['link'] = link
            jobs_data['source'] = hh_link
            jobs.append(jobs_data)
        next = soup.find('a',{'class':'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})['href']
        next_link = hh_link+next
        html = requests.get(next_link, headers= header).text
        soup = bs(html, 'lxml')
    return (jobs)

#pprint(hh_parser(vacancy_name, hh_link, header,39))

result = pd.DataFrame(hh_parser(vacancy_name, hh_link, header,39))
print(type(result))
