#1) Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные о письмах
# в базу данных (от кого, дата отправки, тема письма, текст письма полный).vЛогин тестового ящика: study.ai_172@mail.ru
#Пароль тестового ящика: NewPassword172


from selenium import webdriver
import time
import json
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient


driver = webdriver.Chrome()
driver.get('https://mail.ru/?from=login')
assert 'Mail.ru: почта, поиск в интернете, новости, игры' in driver.title
auth_insert = driver.find_element_by_id('mailbox:login')
auth_insert.send_keys('study.ai_172@mail.ru')
button = driver.find_element_by_class_name('mailbox__icon_next')
button.click()
auth_insert = driver.find_element_by_id('mailbox:password')
auth_insert.send_keys('NewPassword172')
button = driver.find_element_by_id('mailbox:submit')
button.click()
time.sleep(20)
body = driver.find_element_by_id('app-canvas')
letters_elements = body.find_elements_by_class_name('js-letter-list-item')
mails_links = []
for i in letters_elements:
    link = i.get_attribute('href')
    mails_links.append(link)
mails_data_list = []
for i in mails_links:
    mail_data = {}
    driver.get(i)
    print(f'Я перешел по ссылке{i} в письмо')
    time.sleep(10)
    app_canva = driver.find_element_by_id('app-canvas')
    mail_subject = app_canva.find_element_by_tag_name('h2').text
    date = app_canva.find_element_by_class_name('letter__date').text
    from_who = app_canva.find_element_by_class_name('letter-contact').text
    mail_text = app_canva.find_element_by_class_name('letter-body__body-content').text
    mail_data['from who'] = from_who
    mail_data['date'] = date
    mail_data['mail_subject'] = mail_subject
    mail_data['mail_text'] = mail_text
    mails_data_list.append(mail_data)

client = MongoClient('localhost', 27017)
db = client['Mails_mail_ru']
mails = db.mails

mails.insert_many(mails_data_list)


#2. Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД.
chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.mvideo.ru/')
assert 'М.Видео' in driver.title
body = driver.find_element_by_class_name('page-content')
time.sleep(10)
all_blocks = body.find_elements_by_class_name('gallery-layout')
sales_hits_block = all_blocks[4]
products = []
button = sales_hits_block.find_element_by_class_name('sel-hits-button-next')
while True:
    products_list = sales_hits_block.find_elements_by_tag_name('li')
    for i in products_list[:4]:
         product = {}
         description = i.find_element_by_tag_name('a').get_attribute('data-product-info')
         description = json.loads(description)
         product['product_name'] = description.get('productName')
         product['price'] = description.get('productPriceLocal')
         products.append(product)
    if button.get_attribute('class') != 'next-btn sel-hits-button-next disabled':
         actions = ActionChains(driver)
         actions.move_to_element(button).click().perform()
         time.sleep(7)
    else:
        break
for i in products:
    print(i)

client = MongoClient('localhost', 27017)
db = client['M_video']
product_list = db.product_list

product_list.insert_many(products)