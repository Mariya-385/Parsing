# 1)Написать приложение, которое собирает основные новости с сайтов news.mail.ru, lenta.ru, yandex.news
# Для парсинга использовать xpath. Структура данных должна содержать:
# название источника,
# наименование новости,
# ссылку на новость,
# дата публикации
#
# 2)Сложить все новости в БД


from requests import get
from lxml import html
from pymongo import MongoClient

header= {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}


def parsed_inner_body(parsed_body,xpath:str):
    response = parsed_body.xpath(xpath)
    return response


response = get('https://yandex.ru/news', headers = header)
if response.ok:
    parsed_body = html.fromstring(response.text) #проебразует тело документа в DOM
    five_news_Moscow = parsed_inner_body(parsed_body,"//div[@class='stories-set stories-set_main_no stories-set_pos_1']//tr/td[@class='stories-set__item']")
    five_news_Interesnoe = parsed_inner_body(parsed_body,"//div[@class='stories-set stories-set_main_no stories-set_pos_2']//tr/td[@class='stories-set__item']")
    yandex_news = []
    for i in five_news_Moscow:
        news_moscow = {}
        source_name = i.xpath(".//div[@class='story__date']//text()")
        news_name = i.xpath(".//h2[@class='story__title']//text()")
        news_link = i.xpath(".//h2[@class='story__title']/a/@href")
        news_moscow['source_name'] = source_name
        news_moscow['news_name'] = news_name
        news_moscow['news_link'] = news_link
        yandex_news.append(news_moscow)
    for i in five_news_Interesnoe:
        news_Interest = {}
        source_name = i.xpath(".//div[@class='story__date']//text()")
        news_name = i.xpath(".//h2[@class='story__title']//text()")
        news_link = i.xpath(".//h2[@class='story__title']/a/@href")
        news_Interest['source_name'] = source_name
        news_Interest['news_name'] = news_name
        news_Interest['news_link'] = news_link
        yandex_news.append(news_Interest)
else:
    print('Странциа недоступна')




client = MongoClient('localhost', 27017)
db = client['Yandex_news']
news = db.news

def ya_news(news_list):
    news.insert_many(news_list)

ya_news(yandex_news)

def get_inner_parsed_body_mail_ru(main_url, header):
    inner_link = get(main_url+i, headers=header)
    parsed_body = html.fromstring(inner_link.text)
    return parsed_body


def mail_ru_news():
    url = 'https://news.mail.ru'
    responce = get(url=url,headers = header)
    if responce.ok:
        parsed_body = html.fromstring(responce.text)
        link_main_news = parsed_body.xpath("//div[@name='clb20268335']//td[1]//a/@href")
        news = []
        for i in link_main_news:
            parsed_main = get_inner_parsed_body_mail_ru(url,header)
            main = {}
            source_name = parsed_main.xpath("//a[@class='link color_gray breadcrumbs__link']//span[@class='link__text']//text()")
            news_name = parsed_main.xpath("//h1[@class='hdr__inner']//text()")
            date = parsed_main.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")
            main['sorce_name'] = source_name
            main['news_name'] = news_name
            main['news_link'] = url+i
            main['date_time'] = date
            news.append(main)
        second_news_links = parsed_body.xpath("//td[@class]/div[@class='daynews__item']/a/@href")
        for i in second_news_links:
            parsed_news = get_inner_parsed_body_mail_ru(url+i,header)
            second_news = {}
            source_name_second = parsed_news.xpath("//a[@class='link color_gray breadcrumbs__link']//span[@class='link__text']//text()")
            news_name_second = parsed_news.xpath("//h1[@class='hdr__inner']//text()")
            date_second = parsed_news.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")
            second_news['sorce_name'] = source_name_second
            second_news['news_name'] = news_name_second
            second_news['news_link'] = url+i
            second_news['date_time'] = date_second
            news.append(second_news)
        small_news_list = parsed_body.xpath("//ul[@name='clb20268353']/li")
        print(len(small_news_list))
        small_news_6 = small_news_list[2:]
        for i in small_news_6:
            link = i.xpath("./a/@href")
            for i in link:
                parsed_news = get_inner_parsed_body_mail_ru(url,header)
                small_news = {}
                source_name_second = parsed_news.xpath("//a[@class='link color_gray breadcrumbs__link']//span[@class='link__text']//text()")
                news_name_second = parsed_news.xpath("//h1[@class='hdr__inner']//text()")
                date_second = parsed_news.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")
                small_news['sorce_name'] = source_name_second
                small_news['news_name'] = news_name_second
                small_news['news_link'] = link
                small_news['date_time'] = date_second
                news.append(small_news)
        return news
    else:
        print("Страница недоступна")
