from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
from bs4 import BeautifulSoup as bs
from sqlalchemy import create_engine
import re



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

vacancy_name = 'python'
hh_link = 'https://hh.ru'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'}
strs = 39
result = hh_parser(vacancy_name,hh_link,header,39)



from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///hh_vacancy.db',echo=True)
Base = declarative_base()

class Vacancy(Base):
    __tablename__ = 'vacancies'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    job_name = Column(VARCHAR(100))
    salary_min = Column(Integer)
    salary_max = Column(Integer)
    currency = Column(VARCHAR(10))
    link = Column(VARCHAR(255))
    source = Column(VARCHAR(100))

    def __init__(self, job_name, salary_min, salary_max, currency, link, source):
        self.job_name  = job_name
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.currency = currency
        self.link = link
        self.source = source


Base.metadata.create_all(engine)

def SQL_add(vacancy_list):
    Session = sessionmaker(bind=engine)
    session = Session()
    for i in vacancy_list:
        vacancy = Vacancy(i['job_name'], i['slary_min'], i['slary_max'], i['currency'], i['link'], i['source'])
        session.add(vacancy)
    session.commit()
    session.close()

# print(SQL_add(result))
#
# Base.metadata.create_all(engine)
#
# session_db = sessionmaker(bind=engine)
# session = session_db()
# vac = session.query(Vacancy).all()
# print(vac)
# session.close()

def salary_search (salary):
    session_db = sessionmaker(bind=engine)
    session = session_db()
    result = session.query(Vacancy.job_name).filter(Vacancy.salary_min>=salary).all()
    session.close()
    return result
print(salary_search(2000))