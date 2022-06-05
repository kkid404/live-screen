from PIL import Image, ImageDraw, ImageFont
import ctypes
import datetime
from pycoingecko import CoinGeckoAPI
import re
import os
import time
from yaweather import Russia, YaWeather
import configparser

config = configparser.ConfigParser()
config.read("settings.ini")
API = config["YANDEX"]["API"]

while True:
    #получаем погоду
    y = YaWeather(api_key=API)
    res = y.forecast(Russia.Chelyabinsk)

    #получем текущий курс интересующих монет на coingecko
    cg = CoinGeckoAPI()

    btc = str(cg.get_price(ids='bitcoin', vs_currencies='usd'))
    eth = str(cg.get_price(ids='ethereum', vs_currencies='usd'))

    btcprice = [float(s) for s in re.findall(r'-?\d+\.?\d*', btc)]
    ethprice = [float(s) for s in re.findall(r'-?\d+\.?\d*', eth)]

    btcprice = int(btcprice[0])
    ethprice = int(ethprice[0])

    # Получаем дни недели и перевод их в нужный вид
    numday = datetime.datetime.today().isoweekday()
    today = datetime.datetime.now()
    day = today.day
    month = today.month
    hour = today.hour
    minute = today.minute

    def numtoweekday(int):
        if int == 1:
            return "Понедельник"
        elif int == 2:
            return "Вторник"
        elif int == 3:
            return "Среда"
        elif int == 4:
            return "Четверг"
        elif int == 5:
            return "Пятница"
        elif int == 6:
            return "Суббота"
        elif int == 7:
            return "Воскресенье"


    #Получаем размер рабочего стола
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    centerw = screensize[0]
    centerh = screensize[1]

    # Создаем фон изображения
    holst = Image.new("RGB", screensize, '#231F20')


    # Генерируем текст
    fontweek = ImageFont.truetype("Gilroy-Semibold.ttf", size=60)
    fontprice = ImageFont.truetype("Gilroy-Regular.ttf", size=40)
    fontweather = ImageFont.truetype("Gilroy-Regular.ttf", size=25)

    idraw = ImageDraw.Draw(holst)
    idraw.text((centerw / 3, centerh / 2.8), numtoweekday(numday) + " " + str(day) + "."  + str(month), font=fontweek, fill="#A771FE")
    idraw.text((centerw / 3, centerh / 2.05), f'Фактическая погода {res.fact.feels_like} °C', font=fontweather, fill="#A771FE")
    idraw.text((centerw / 1.63, centerh / 2.2), str(hour) + ":" + str(minute), font=fontweek, fill="#A771FE")
    idraw.rectangle((centerw / 3, centerh / 1.87, centerw / 1.3, centerh / 1.86), fill='#A771FE')
    idraw.text((centerw / 3, centerh / 1.8), "BTC/USD: "+ str(btcprice), font=fontprice, fill="#e7f20c")
    idraw.text((centerw / 3, centerh / 1.6), "ETH/USD: "+ str(ethprice), font=fontprice, fill="#e7f20c")
    holst.save("text_pyton.jpg")


    # Устанавливаем картинку на рабочий стол
    folder = r"E:\python\live-screen"
    file_name = r"text_pyton.jpg"
    full_path = os.path.join(folder, file_name)
    wallpaper = bytes(full_path, 'utf-8')
    ctypes.windll.user32.SystemParametersInfoA(20, 0, wallpaper, 3)

    time.sleep(30)