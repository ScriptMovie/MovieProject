from tkinter import *
from tkinter import font
from PIL import Image, ImageTk
from io import BytesIO
from tkinter import ttk

import io
import re

import zzim
import goToDetail
import map

import threading
import sys
from tkinter import messagebox
import folium


import requests
import json
import teller
import noti
import spam

api_key = spam.getapikey('tmdb')
# language = 'en-US'

WINDOW_ROW = 1100
WINDOW_COL = 700


class MainGUI:
    def fetchMovieData(self):
        # Trend API 가져오기
        url = "https://api.themoviedb.org/3/trending/movie/day?language="+self.language
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwNWI4MWZmZTA1Y2IyNGMzYWIwNDRlYTA0YWE5Y2MxNyIsInN1YiI6IjYxNzY3MTM4ZmQ3YWE0MDA5MDhiYTM2MSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.UOphTbPyyXEENKyaUd36d31TgXdt4y-mp5qfc407G3s"
        }
        tempR = requests.get(url, headers=headers)
        self.MovieD = json.loads(tempR.text)
        print(self.MovieD)
        #print(self.MovieD["results"])
        self.printTrendMovie()
    def fetchTvData(self):
        # Trend API 가져오기
        url = "https://api.themoviedb.org/3/trending/tv/day?language="+self.language
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwNWI4MWZmZTA1Y2IyNGMzYWIwNDRlYTA0YWE5Y2MxNyIsInN1YiI6IjYxNzY3MTM4ZmQ3YWE0MDA5MDhiYTM2MSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.UOphTbPyyXEENKyaUd36d31TgXdt4y-mp5qfc407G3s"
        }
        tempR = requests.get(url, headers=headers)
        self.TvD = json.loads(tempR.text)
        print(self.TvD)
        self.printTrendTv()
    def printTrendMovie(self):
        self.imageM=[0]*21
        noti.telegram_Movie_Trand.clear()
        for i in range(len(self.MovieD["results"])):
            self.MimageUrl = "https://image.tmdb.org/t/p/w200" + str(self.MovieD["results"][i]["poster_path"])
            self.m = requests.get(self.MimageUrl)
            noti.telegram_Movie_Trand += [self.MovieD["results"][i]]

            self.MImage = Image.open(BytesIO(self.m.content))
            self.MImage = self.MImage.convert('RGB')
            self.MImage = self.MImage.resize((190, 290), Image.NEAREST)

            self.imageM[i] = ImageTk.PhotoImage(self.MImage)

            # 버튼 안에 이미지 넣기
            kindT="M"
            imageHeight = 290
            self.MImageButton = Button(self.MFrame, image=self.imageM[i], anchor=N,height=imageHeight, command=lambda i=i: (goToDetail.GOTODETAIL(self.info_poster_label,self.homeFrame,self.imageM[i],self.MovieD["results"][i],kindT,self.language),self.ZzimImageChangeJudge()))
            self.MImageButton.image = self.imageM[i]
            self.MImageButton.grid(row=0, column=i, sticky="ew")

        # frame의 길이에 따라 canvas의 길이 조절하기
        self.MFrame.update_idletasks()
        self.MovieCanvas.create_window((0, 0), window=self.MFrame, anchor="nw")
        self.MFrame.bind("<Configure>",self.MovieCanvas.configure(scrollregion=self.MovieCanvas.bbox("all"), width=self.MFrame.winfo_width()))

    def printTrendTv(self):
        self.image=[0]*21
        noti.telegram_TV_Trand.clear()
        for i in range(len(self.TvD["results"])):
            self.imageUrl = "https://image.tmdb.org/t/p/w200" + str(self.TvD["results"][i]["poster_path"])
            self.r = requests.get(self.imageUrl)
            noti.telegram_TV_Trand += [self.TvD['results'][i]]

            self.pilImage = Image.open(BytesIO(self.r.content))
            self.pilImage = self.pilImage.convert('RGB')
            self.pilImage = self.pilImage.resize((190, 290), Image.NEAREST)

            self.image[i] = ImageTk.PhotoImage(self.pilImage)

            # 버튼 안에 이미지 넣기
            kindT="T"
            imageHeight = 290
            self.ImageButton = Button(self.TFrame, image=self.image[i], anchor=N,height=imageHeight, command=lambda i=i: (goToDetail.GOTODETAIL(self.info_poster_label,self.homeFrame,self.image[i],self.TvD["results"][i],kindT,self.language),self.ZzimImageChangeJudge()))
            self.ImageButton.image = self.image[i]
            self.ImageButton.grid(row=0, column=i, sticky="ew")

        # frame의 길이에 따라 canvas의 길이 조절하기
        self.TFrame.update_idletasks()
        self.TvCanvas.create_window((0, 0), window=self.TFrame, anchor="nw")
        self.TFrame.bind("<Configure>",self.TvCanvas.configure(scrollregion=self.TvCanvas.bbox("all"), width=self.TFrame.winfo_width()))

    def search(self):
        query = self.search_entry.get()
        url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}&language={self.language}'
        response = requests.get(url)
        data = response.json()

        results = data['results']
        self.search_movie_listbox.delete(0, END)      # 리스트 박스 요소 모두 제거
        self.search_movie_list = []
        for result in results:
            title = result['title'].split()
            if self.language=='en-US':
                if bool(re.match('^[a-zA-Z]+$', title[0][0])):  # 제목이 영어인지 확인한다 / 한글 버전 일시에 한글만 나열함
                    self.search_movie_listbox.insert(END, result['title'])
                    self.search_movie_list.append(result)
            elif self.language=='ko-KR':
                if not bool(re.match('^[a-zA-Z]+$', title[0][0])):
                    self.search_movie_listbox.insert(END, result['title'])
                    self.search_movie_list.append(result)
    # 선택한 영화의 포스터 이미지를 가져와서 보여주는 함수
    def search_select_show_movie_poster(self,evant):
        index = self.search_movie_listbox.curselection()[0]
        if self.search_movie_list[index]:
            poster_path = self.search_movie_list[index]['poster_path']
            poster_url = f'https://image.tmdb.org/t/p/w500/{poster_path}' # /p2l6hOlyx1ZP6jt9wagthliVg9h.jpg
            response = requests.get(poster_url)

            img = Image.open(io.BytesIO(response.content))
            img = img.convert('RGB')
            img = img.resize((190, 290), Image.NEAREST)

            img = ImageTk.PhotoImage(img)
            if 'title' in self.search_movie_list[index]:
                goToDetail.GOTODETAIL(self.info_poster_label, self.homeFrame, img, self.search_movie_list[index], "M",self.language)
            else:
                goToDetail.GOTODETAIL(self.info_poster_label, self.homeFrame, img, self.search_movie_list[index], "T",self.language)

            self.ZzimImageChangeJudge()
        else:
            self.info_poster_label.configure(image='')
            self.info_poster_label.image = None
            goToDetail.currentPick = None
    def AddZzim(self):
        if goToDetail.currentPick != None:
            if goToDetail.currentPick not in self.zzim.get_zzimlist(): # 현재 선택한 컨텐츠가 찜 목록에 없을떄 넣어라
                self.ZzimButton.configure(image=self.Zzim_after)
                self.ZzimButton.image = self.Zzim_after
                self.zzim.add_zzim(goToDetail.currentPick)
                # print(self.zzim.get_zzimlist())
            else: # 다시 누르면 찜 취소
                self.ZzimButton.configure(image=self.Zzim_before)
                self.ZzimButton.image = self.Zzim_before
                self.zzim.del_zzim(goToDetail.currentPick)
        self.Zzim_listbox_Sync()
        self.voteRatio_Sync()
    def ZzimImageChangeJudge(self):
        if goToDetail.currentPick not in self.zzim.get_zzimlist():
            self.ZzimButton.configure(image=self.Zzim_before)
            self.ZzimButton.image = self.Zzim_before
        else:
            self.ZzimButton.configure(image=self.Zzim_after)
            self.ZzimButton.image = self.Zzim_after
    def CreateZzim_listboxFrame(self):
        self.Zzim_listbox = Listbox(self.ZzimlistFrame, width=40, height=30)
        self.Zzim_listbox.place(x=600, y=100)  # -3 은 리스트박스 경계선 안보이도록
        self.Zzim_listbox.configure(bg='#FCD572')
        Label(self.ZzimlistFrame, text='찜 목록').place(x=550+175,y=75)

    def Zzim_listbox_Sync(self):
        self.Zzim_list = []
        self.Zzim_listbox.delete(0,END)
        self.Zzim_listbox.bind('<<ListboxSelect>>', self.Zzim_select_show_movie_poster)
        # 딕셔너리 데이터
        movie_list = self.zzim.get_zzimlist()
        # 딕셔너리의 키와 값을 리스트 박스에 추가
        for idx,result in enumerate(movie_list):
            if 'title' in result:
                self.Zzim_listbox.insert(END, f"{idx + 1} : " + result['title'])
            else:
                self.Zzim_listbox.insert(END, f"{idx + 1} : " + result['name'])
            self.Zzim_list.append(result)
    # 찜 목록에서 선택하면 포스터 가져오는 함수
    def Zzim_select_show_movie_poster(self, evant):
        index = self.Zzim_listbox.curselection()[0]
        if self.Zzim_list[index]:
            poster_path = self.Zzim_list[index]['poster_path']
            poster_url = f'https://image.tmdb.org/t/p/w500/{poster_path}'
            response = requests.get(poster_url)
            # img_data = response.content

            img = Image.open(io.BytesIO(response.content))
            img = img.convert('RGB')
            img = img.resize((300, 250), Image.LANCZOS)
            # NEAREST(빠름) , LANCZOS(느림)

            img = ImageTk.PhotoImage(img)
            # 포스터
            self.Zzim_poster_label = Label(self.ZzimlistFrame, width=310, height=260, bg='#EC7729')
            self.Zzim_poster_label.configure(image=img)
            self.Zzim_poster_label.image = img
            self.Zzim_poster_label.place(x=140, y=45)
            # self.ZzimImageChangeJudge()
        else:
            self.info_poster_label.configure(image='')
            self.info_poster_label.image = None
    def CreateZZimList(self):
        Label(self.ZzimlistFrame, text='평점').place(x=90+195,y=355-25)
        self.CreateZzim_listboxFrame()
        self.voteRatio_Sync()
    def voteRatio_Sync(self):
        # 찜 목록에 있는 평점 데이터를 담는 리스트
        movie_list = self.zzim.get_zzimlist()

        data = [round(i['vote_average'],1) for i in movie_list]
        c_width = 400
        c_height = 350
        c = Canvas(self.ZzimlistFrame, width=c_width, height=c_height, bg='#FCD572')
        c.place(x=90,y=355)
        y_stretch = 30
        y_gap = 20
        x_stretch = 10
        x_width = 20
        x_gap = 20
        for x, y in enumerate(data): # x는 인덱스 값 y는 평점을 나타냄
            x0 = x * x_stretch + x * x_width + x_gap
            y0 = c_height - (y * y_stretch + y_gap)
            x1 = x * x_stretch + x * x_width + x_width + x_gap
            y1 = c_height - y_gap

            c.create_rectangle(x0, y0, x1, y1, fill="sky blue")
            c.create_text(x0 + 2, y0, anchor=SW, text=str(y))
            c.create_text(x0 + 5, y1 + 20, anchor=SW, text=str(x+1))

    def checkState(self):
        self.var = 1-self.var
        if self.var == 1:
            self.language = 'en-US'
        elif self.var == 0:
            self.language = 'ko-KR'
        self.home()
    def home(self):
        self.homeFrame = Frame(self.window,bg="orange",width=1000,height=800)
        self.homeFrame.place(x=120,y=5)

        # if self.currentPageNum==1: #지도에서 홈으로 왔으면
        #     self.mapFrame.destroy()
        # self.currentPageNum=0

        #한영 토글
        self.LanguageCheck = Button(self.homeFrame, text=self.language , command = self.checkState)
        self.LanguageCheck.place(x=330,y=0)

        # 검색창
        self.search_entry = Entry(self.homeFrame, width=40)
        self.search_entry.place(x=0, y=0)
        self.search_entry.configure(bg='#FCD572')

        # 검색버튼
        self.search_button = Button(self.homeFrame, text="검색", command=self.search)
        self.search_button.place(x=290, y=0)

        # 검색한 리스트박스
        self.search_movie_listbox = Listbox(self.homeFrame, width=40)
        self.search_movie_listbox.place(x=0, y=50)
        self.search_movie_listbox.bind('<<ListboxSelect>>', self.search_select_show_movie_poster)
        self.search_movie_listbox.configure(bg='#FCD572')

        # 정보란 포스터 라벨
        self.info_poster_label = Label(self.homeFrame, width=200, height=300, bg="orange")
        self.info_poster_label.place(x=0, y=225)

        # 위도우 안에 글
        movieLabel = Label(self.homeFrame, text="Trend Movie", bg="orange")
        movieLabel.place(x=WINDOW_ROW / 2-120, y=0)

        tvLabel = Label(self.homeFrame, text="Trend Tv", bg="orange")
        tvLabel.place(x=WINDOW_ROW / 2-120, y=WINDOW_COL / 2)

        # 위도우 안에 프레임
        self.TrendMovieFrame = Frame(self.homeFrame, bg="orange")
        # self.TrendMovieFrame.pack(fill="both",expand=True, padx=(WINDOW_ROW/2,0), pady=(0,WINDOW_COL/2))
        self.TrendMovieFrame.place(x=WINDOW_ROW / 2 - 120, y=25, relwidth=0.5, relheight=0.4)

        self.TrendTvFrame = Frame(self.homeFrame, bg="orange")
        # self.TrendTvFrame.pack(fill="both",expand=True, padx=(WINDOW_ROW/2,0), pady=(WINDOW_COL/2,0))
        self.TrendTvFrame.place(x=WINDOW_ROW / 2- 120, y=WINDOW_COL / 2 + 25, relwidth=0.5, relheight=0.4)

        # 프레임안에 스크롤바
        self.MovieScrollBar = Scrollbar(self.TrendMovieFrame, orient=HORIZONTAL)
        self.MovieScrollBar.pack(side=BOTTOM, fill=X)

        self.TvScrollBar = Scrollbar(self.TrendTvFrame, orient=HORIZONTAL)
        self.TvScrollBar.pack(side=BOTTOM, fill=X)

        # 캔버스 생성
        self.MovieCanvas = Canvas(self.TrendMovieFrame, xscrollcommand=self.MovieScrollBar.set, bg="orange")
        self.MovieCanvas.pack(side=LEFT, fill=BOTH, expand=True)

        self.TvCanvas = Canvas(self.TrendTvFrame, xscrollcommand=self.TvScrollBar.set, bg="orange")
        self.TvCanvas.pack(side=LEFT, fill=BOTH, expand=True)

        # 스크롤바와 캔버스 연결
        self.MovieScrollBar.config(command=self.MovieCanvas.xview)
        self.TvScrollBar.config(command=self.TvCanvas.xview)

        # 캔버스안에 프레임 설정
        self.MFrame = Frame(self.MovieCanvas, bg="cyan")
        self.TFrame = Frame(self.TvCanvas, bg="cyan")

        # 폰트
        self.fontstyle = font.Font(self.homeFrame, size=24, weight='bold', family='Consolas')
        self.fontstyle2 = font.Font(self.homeFrame, size=16, weight='bold', family='Consolas')

        # api불러오기
        self.fetchMovieData()
        self.fetchTvData()

        # 찜 버튼 만들기 (동그라미 버튼)
        image = Image.open("resource/Zzim_before.png")
        # 이미지 사이즈 조절
        image_with_alpha = image.convert("RGBA")
        resized_image = image_with_alpha.resize((50, 50))
        # 이미지를 PhotoImage로 변환
        self.Zzim_before = ImageTk.PhotoImage(resized_image)
        # 버튼 생성 및 이미지 설정
        self.ZzimButton = Button(self.homeFrame, image=self.Zzim_before, bd=0, command=self.AddZzim, highlightthickness=0)
        self.ZzimButton.place(x=0, y=625)

        image = Image.open("resource/Zzim_after.png")
        image_with_alpha = image.convert("RGBA")
        resized_image = image_with_alpha.resize((50, 50))
        self.Zzim_after = ImageTk.PhotoImage(resized_image)

    def callMap(self):
        # if self.currentPageNum==0: #홈에서 지도로 왔으면
        #     self.homeFrame.destroy()
        # self.currentPageNum=1
        self.mapFrame = Frame(self.window,bg="orange",width=1000,height=800)
        self.mapFrame.place(x=120,y=5)

        self.map = map.MAP(self.window, self.mapFrame,self.cefInitialNum)
        #cef는 한번만 초기화 해야한다.
        self.cefInitialNum += 1
     # -------------------------추가------------------------------
    def show_frame(self, frame):
        frame.tkraise()
    def tele_start(self):
        teller.telegram_start()

    # -------------------------추가------------------------------
    def __init__(self):
        #현재 있는곳
        #0 : 홈, 1: 지도
        self.currentPageNum = 0
        self.language = 'ko-KR'

        self.window = Tk()
        self.window.title("무빙")
        self.window.geometry("1100x700+100+100")
        self.window.configure(bg='#FFA500')

        # 찜 변수 선언
        self.zzim = zzim.ZZIM()

        #지도
        self.cefInitialNum=0

        self.var = 0
        self.home()

        #====================왼쪽 메뉴 바========================
        # 찜 목록 버튼

        self.ZzimlistFrame = Frame(self.window, bg="orange", width=1000, height=800)
        self.ZzimlistFrame.place(x=120, y=-20)

        Label(self.ZzimlistFrame, bg="orange", width=1000, height=800).pack()
        self.CreateZZimList()

        image = Image.open("resource/Zzimlist.png")
        image_with_alpha = image.convert("RGBA")
        resized_image = image_with_alpha.resize((100, 100))
        photo2 = ImageTk.PhotoImage(resized_image)
        # Button(self.window, image=photo2, command=self.OpenZzimFrame,highlightthickness=0).place(x=8, y=5)
        Button(self.window, image=photo2, highlightthickness=0,
               command=lambda: self.show_frame(self.ZzimlistFrame)).place(x=8, y=5)

        image = Image.open("resource/telegram.png")
        image_with_alpha = image.convert("RGBA")
        resized_image = image_with_alpha.resize((100, 100))
        photo3 = ImageTk.PhotoImage(resized_image)
        # 텔레그램 버튼
        Button(self.window, image=photo3, highlightthickness=0, command=self.tele_start).place(x=8, y=125)

        # 홈버튼
        image = Image.open("resource/home.png")
        image_with_alpha = image.convert("RGBA")
        resized_image = image_with_alpha.resize((100, 100))
        photo5 = ImageTk.PhotoImage(resized_image)
        # self.homeBtn = Button(self.window, image=photo5, highlightthickness=0,command =lambda:self.home())
        Button(self.window, image=photo5, highlightthickness=0, command=lambda: self.show_frame(self.homeFrame)).place(
            x=8, y=360)
        # self.homeBtn.place(x=8, y=360)

        # 지도 버튼
        image = Image.open("resource/Map.png")
        image_with_alpha = image.convert("RGBA")
        resized_image = image_with_alpha.resize((100, 100))
        photo4 = ImageTk.PhotoImage(resized_image)
        # self.callMap()
        self.mapBtn = Button(self.window, image=photo4, highlightthickness=0, command=lambda: self.callMap())
        # Button(self.window, image=photo4, command=lambda: self.show_frame(self.mapFrame)).place(x=8, y=245)
        self.mapBtn.place(x=8, y=245)
        #====================왼쪽 메뉴 바========================

        self.show_frame(self.homeFrame)

        self.tel_count = 0
        self.window.mainloop()

MainGUI()