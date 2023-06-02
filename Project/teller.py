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

import noti

def replyAptData(date_param, user):
    print(user, date_param)
    res_list = noti.getData( date_param )
    msg = ''
    image_path = []
    count = 0
    for idx,r in enumerate(res_list):
        print( str(datetime.now()).split('.')[0], r[0] )
        if count == 0:
            count += 1
            noti.sendMessage(user, f'<      {date_param}        >',None)
        # if len(r[0]+msg)+1>noti.MAX_MSG_LENGTH:
        #     noti.sendMessage( user, msg )
        #     msg = str(idx + 1) + "위 [" + r[0] + ']' +'\n'
        #     image_path.append(r[1])
        # else:
        msg = str(idx + 1) + "위 [" + r[0] + ']' + '\n'
        noti.sendMessage(user, msg,r[1])
        # msg += str(idx + 1) + "위 [" + r[0] + ']' + '\n'
        # image_path.append(r[1])
    if msg:
        noti.sendMessage( user, msg,image_path[0])
    else:
        noti.sendMessage( user, '%s 데이터가 없습니다.'%date_param )

def save( user, loc_param ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    try:
        cursor.execute('INSERT INTO users(user, location) VALUES ("%s", "%s")' % (user, loc_param))
    except sqlite3.IntegrityError:
        noti.sendMessage( user, '이미 해당 정보가 저장되어 있습니다.' )
        return
    else:
        noti.sendMessage( user, '저장되었습니다.' )
        conn.commit()

def check( user ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    cursor.execute('SELECT * from users WHERE user="%s"' % user)
    for data in cursor.fetchall():
        row = 'id:' + str(data[0]) + ', location:' + data[1]
        noti.sendMessage( user, row )

User_List = []
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if chat_id not in User_List:
        User_List.append(chat_id)
        user_list_idfile = open('UserID.txt', 'a')
        user_list_idfile.write(f" {chat_id}")
        user_list_idfile.close()

    print(telepot.glance(msg))
    print(content_type,chat_type,chat_id)
    if content_type != 'text':
        noti.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']
    print(text , f'{type(text)=}') # 거래 202303 11440 type(text)=<class 'str'>
    args = text.split(' ')
    print(f'{args=}') # args=['거래', '202303', '11440']  [영화]
    # 최신영화순위
    if text.startswith('영화'):
        print('영화', args[0]) # 884257593 202303 11440
        replyAptData('영화트렌드', chat_id)
    elif text.startswith('드라마'):
        print('영화', args[0])
        replyAptData('드라마트렌드', chat_id)
    elif text.startswith('저장')  and len(args)>1:
        print('try to 저장', args[1])
        save( chat_id, args[1] )
    elif text.startswith('확인'):
        print('try to 확인')
        check( chat_id )
    else:
        noti.sendMessage(chat_id, '모르는 명령어입니다.\n 영화 또는 드라마 중 하나를 입력하세요.')
def telegram_start():
    today = date.today()
    current_month = today.strftime('%Y%m')

    print( '[',today,']received token :', noti.TOKEN )

    bot = telepot.Bot(noti.TOKEN)
    pprint( bot.getMe() )

    global User_List
    # 전체 메시지를 보내기 위함.
    user_list_idfile = open('UserID.txt', 'r')
    User_List = user_list_idfile.read().split()
    for id in User_List:
        noti.sendMessage(id, '<안녕하세요!>\n"영화" 또는 "드라마" 를 입력하시면 각 트렌드 순위를 보여줍니다!')
    user_list_idfile.close()

    bot.message_loop(handle)

    print('Listening...')