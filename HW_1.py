#1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

import requests
import json
from pprint import pprint

#link = 'https://api.github.com/users'
#user = 'Mariya-385'

#response = requests.get(f'{link}/{user}/repos')

#for i in response.json():
    #with open ('My_peros.json', 'a') as f:
        #json.dump(i.get("name"),f)

#2.Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
url = 'https://api.openweathermap.org/data/2.5/weather'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'}
city = 'Tenerife'
appid='c9854ed5a8fedcdb4760bc36b2deef14'
params = {
    'q':city,
    'appid':appid
}

resp = requests.get(url, headers = header, params=params)
if resp.ok:
    with open ('Response,json', 'w') as f:
        json.dump(resp.text, f)
