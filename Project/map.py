
from tkinter import *
import threading
import sys
from tkinter import messagebox
# pip install folium
import folium
# pip install cefpython3==66.1
from cefpython3 import cefpython as cef

import requests
import json
import spam
import re

class MAP:
    def callAPI(self):
        self.data = []
#" + spam.getapikey('map')+ "
        for i in range(11):
            url = f"https://openapi.gg.go.kr/MovieTheater?KEY=0026aa7c9348412680cca736f93d737b&pIndex={i + 1}&Type=json"
            response = requests.get(url)
            contents = response.text
            tdata = json.loads(contents)
            result = {(item['REFINE_WGS84_LAT'], item['REFINE_WGS84_LOGT']): item for item in
                      tdata['MovieTheater'][1]['row']}.values()
            self.data += list(result)
        print(self.data)
    def on_select(self,event):
        index = self.listbox.curselection()[0]
        print(self.data[index])
        mData = self.data[index]
        m = folium.Map(location=[mData['REFINE_WGS84_LAT'], mData['REFINE_WGS84_LOGT']], zoom_start=13)
        folium.Marker([mData['REFINE_WGS84_LAT'], mData['REFINE_WGS84_LOGT']], popup=mData['BIZPLC_NM']).add_to(m)
        m.save('map.html')
        if self.browser is not None:
            self.browser.Reload()

    def searchT(self):
        query = self.search_theater.get()
        tempData = []
        for i in range(11):
            url = f"https://openapi.gg.go.kr/MovieTheater?KEY=0026aa7c9348412680cca736f93d737b&pIndex={i + 1}&Type=json"
            response = requests.get(url)
            contents = response.text
            tdata = json.loads(contents)
            result = {(item['REFINE_WGS84_LAT'], item['REFINE_WGS84_LOGT']): item for item in
                      tdata['MovieTheater'][1]['row']}.values()
            tempData += list(result)
        self.listbox.delete(0, END)      # 리스트 박스 요소 모두 제거
        self.search_movie_list = []
        self.data=[]
        for theat in tempData:
            tempStr = str(theat['SIGUN_NM'] + theat['BIZPLC_NM'])
            if query in tempStr:
                self.data += theat

        self.reFreshList()

    def reFreshList(self):
        # 영화관 리스트
        self.listbox = Listbox(self.mapFrame, width=29, height=41)
        self.listbox.place(x=0, y=28)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)

        for i in self.data:
            self.listbox.insert(END, i['SIGUN_NM'] + " " + i['BIZPLC_NM'])

    def __init__(self,window,mapFrame,cefNum):
        self.callAPI()

        self.cefNum = cefNum

        if self.cefNum == 0:
            self.browser = None  # browser 속성을 None으로 초기화


        self.mapFrame = mapFrame
        # 검색창
        self.search_theater = Label(self.mapFrame,text="영화 상영관 목록",bg="orange")
        self.search_theater.place(x=0, y=0)

        self.reFreshList()

        # Button(frame1, text=data['MovieTheater'][1]['row'][0]['SIGUN_NM'], command=self.pressed_1).pack()
        self.mapFrame2 = Frame(self.mapFrame,width=760,height=690)
        self.mapFrame2.place(x=214,y=0)

        self.setup()
        # 브라우저를 위한 쓰레드 생성
        if self.cefNum == 0:
            thread = threading.Thread(target=self.showMap, args=(self.mapFrame2,))
            thread.daemon = True
            thread.start()

        window.mainloop()
    def showMap(self,frame):
        if self.browser is None:
            sys.excepthook = cef.ExceptHook
            window_info = cef.WindowInfo(frame.winfo_id())
            window_info.SetAsChild(frame.winfo_id(), [0,0,760,690])
            cef.Initialize()
            self.browser = cef.CreateBrowserSync(window_info, url='file:///map.html')
            cef.MessageLoop()

    def setup(self):
        # 지도 저장
        # 위도 경도 지정
        m = folium.Map(location=[37.4413298775, 127.1464590420], zoom_start=13)
        # 마커 지정
        folium.Marker([37.4413298775, 127.1464590420], popup='중앙영상아트극장').add_to(m)
        # html 파일로 저장
        m.save('map.html')