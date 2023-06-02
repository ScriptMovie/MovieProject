#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback
import requests
import spam

api_key = spam.getapikey('tmdb')
language = 'ko_KR'
TOKEN = '5416557016:AAGhgrDUeW14PAp9GzTgTlYTgbc7e59PgWQ'
MAX_MSG_LENGTH = 300
baseurl = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query=querymovie&language={language}'
bot = telepot.Bot(TOKEN)

telegram_Movie_Trand = [] # 텔레그램으로 보낼 트렌드 데이터 리스트
telegram_TV_Trand = []

def getData(data):
    res_list = []
    if data == '영화트렌드':
        for movie in telegram_Movie_Trand:
            res_list.append([movie['title'],movie["poster_path"]])
    elif data == '드라마트렌드':
        for TV in telegram_TV_Trand:
            res_list.append([TV['name'],TV["poster_path"]])
    return res_list

def send_photo_from_url(chat_id, photo_url, bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"

    data = {"chat_id": chat_id, "photo": photo_url}

    response = requests.post(url, data=data)
    response.raise_for_status()

    print("Photo sent successfully!")

def sendMessage(user, msg,imagepath=None):
    try:
        bot.sendMessage(user, msg)
        if imagepath:
            # bot.sendPhoto(user,f"https://image.tmdb.org/t/p/w200/{imagepath}")
            send_photo_from_url(user, f"https://image.tmdb.org/t/p/w200/{imagepath}", TOKEN)
    except:
        traceback.print_exc(file=sys.stdout)

# def send_photo_from_url(chat_id, photo_url, bot_token):
#     url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
#
#     data = {"chat_id": chat_id, "photo": photo_url}
#
#     response = requests.post(url, data=data)
#     response.raise_for_status()
#
#     print("Photo sent successfully!")
#
#
# # 사용 예시
# chat_id = "123456789"  # 대상 채팅 ID
# photo_url = "https://image.tmdb.org/t/p/w500/p2l6hOlyx1ZP6jt9wagthliVg9h.jpg"  # 링크된 이미지 URL
# bot_token = "your_bot_token"  # 텔레그램 봇 토큰
#
# send_photo_from_url(chat_id, photo_url, bot_token)


def run(date_param, param='11710'):
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS logs( user TEXT, log TEXT, PRIMARY KEY(user, log) )')
    conn.commit()

    user_cursor = sqlite3.connect('users.db').cursor()
    user_cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    user_cursor.execute('SELECT * from users')

    for data in user_cursor.fetchall():
        user, param = data[0], data[1]
        print(user, date_param, param)
        res_list = getData( param, date_param )
        msg = ''
        for r in res_list:
            try:
                cursor.execute('INSERT INTO logs (user,log) VALUES ("%s", "%s")'%(user,r))
            except sqlite3.IntegrityError:
                # 이미 해당 데이터가 있다는 것을 의미합니다.
                pass
            else:
                print( str(datetime.now()).split('.')[0], r )
                if len(r+msg)+1>MAX_MSG_LENGTH:
                    sendMessage( user, msg )
                    msg = r+'\n'
                else:
                    msg += r+'\n'
        if msg:
            sendMessage( user, msg )
    conn.commit()

if __name__=='__main__':
    today = date.today()
    current_month = today.strftime('%Y%m')

    print( '[',today,']received token :', TOKEN )

    pprint( bot.getMe() )

    run(current_month)
