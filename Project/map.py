
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

url = "https://openapi.gg.go.kr/MovieTheater?KEY=" + spam.getapikey('map')+ "&pIndex=2&Type=json"

response = requests.get(url)
contents = response.text

data = json.loads(contents)
result = {(item['REFINE_WGS84_LAT'], item['REFINE_WGS84_LOGT']): item for item in data['MovieTheater'][1]['row']}.values()

data = list(result)
print(data)
class MAP:
    def on_select(self,event):
        index = self.listbox.curselection()[0]
        print(data[index])
        mData = data[index]
        m = folium.Map(location=[mData['REFINE_WGS84_LAT'], mData['REFINE_WGS84_LOGT']], zoom_start=13)
        folium.Marker([mData['REFINE_WGS84_LAT'], mData['REFINE_WGS84_LOGT']], popup=mData['BIZPLC_NM']).add_to(m)
        m.save('map.html')
        if self.browser is not None:
            self.browser.Reload()
    def __init__(self,window,mapFrame,cefNum):

        self.browser = None  # browser 속성을 None으로 초기화

        self.cefNum = cefNum

        self.listbox = Listbox(mapFrame,width=30,height=30)
        self.listbox.place(x=0,y=0)
        self.listbox.bind('<<ListboxSelect>>',self.on_select)
        for i in data:
            self.listbox.insert(END,i['SIGUN_NM']+" "+i['BIZPLC_NM'])

        # Button(frame1, text=data['MovieTheater'][1]['row'][0]['SIGUN_NM'], command=self.pressed_1).pack()
        self.mapFrame2 = Frame(mapFrame,width=800,height=700)
        self.mapFrame2.place(x=214,y=0)

        self.setup(self.mapFrame2)
        window.mainloop()
    def showMap(self,frame):
        sys.excepthook = cef.ExceptHook
        window_info = cef.WindowInfo(frame.winfo_id())
        window_info.SetAsChild(frame.winfo_id(), [0,0,800,700])
        if self.cefNum==0:
           cef.Initialize()
        self.browser = cef.CreateBrowserSync(window_info, url='file:///map.html')
        cef.MessageLoop()


    def setup(self,mapFrame2):
        # 지도 저장
        # 위도 경도 지정
        m = folium.Map(location=[37.4413298775, 127.1464590420], zoom_start=13)
        # 마커 지정
        folium.Marker([37.4413298775, 127.1464590420], popup='중앙영상아트극장').add_to(m)
        # html 파일로 저장
        m.save('map.html')

        # 브라우저를 위한 쓰레드 생성
        thread = threading.Thread(target=self.showMap, args=(mapFrame2,))
        thread.daemon = True
        thread.start()