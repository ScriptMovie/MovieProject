from tkinter import *
from tkinter import font
from PIL import Image, ImageTk
from io import BytesIO
import io
import requests
import re
import json
import zzim
import math

# TMDB API = 9f0490f698de8457de01c1f761c6fdc1
api_key = '9f0490f698de8457de01c1f761c6fdc1'
language = 'ko-KR'
# language = 'en'

WINDOW_ROW = 1000
WINDOW_COL = 600

# 현재 고른 컨텐츠를 나타냄
currentPick = None

class MainGUI:
    def fetchMovieData(self):
        # Trend API 가져오기
        url = "https://api.themoviedb.org/3/trending/movie/day?language=en-US"
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwNWI4MWZmZTA1Y2IyNGMzYWIwNDRlYTA0YWE5Y2MxNyIsInN1YiI6IjYxNzY3MTM4ZmQ3YWE0MDA5MDhiYTM2MSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.UOphTbPyyXEENKyaUd36d31TgXdt4y-mp5qfc407G3s"
        }
        tempR = requests.get(url, headers=headers)
        self.MovieD = json.loads(tempR.text)
        self.printTrendMovie()
    def fetchTvData(self):
        # Trend API 가져오기
        url = "https://api.themoviedb.org/3/trending/tv/day?language=en-US"
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwNWI4MWZmZTA1Y2IyNGMzYWIwNDRlYTA0YWE5Y2MxNyIsInN1YiI6IjYxNzY3MTM4ZmQ3YWE0MDA5MDhiYTM2MSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.UOphTbPyyXEENKyaUd36d31TgXdt4y-mp5qfc407G3s"
        }
        tempR = requests.get(url, headers=headers)
        self.TvD = json.loads(tempR.text)
        print(self.TvD['results'])
        self.printTrendTv()
    def GoToDetail(self,data):
        #이미지 클릭시 화면에 이미지 출력
        self.info_poster_label.configure(image=data)
        self.info_poster_label.image = data

    def printTrendMovie(self):
        self.imageM=[0]*21
        for i in range(len(self.MovieD["results"])):
            self.MimageUrl = "https://image.tmdb.org/t/p/w200" + str(self.MovieD["results"][i]["poster_path"])
            self.m = requests.get(self.MimageUrl)

            self.MImage = Image.open(BytesIO(self.m.content))
            self.MImage = self.MImage.convert('RGB')
            self.MImage = self.MImage.resize((180, 250), Image.NEAREST)

            self.imageM[i] = ImageTk.PhotoImage(self.MImage)

            # 버튼 안에 이미지 넣기
            self.MImageButton = Button(self.MFrame, image=self.imageM[i], anchor=N,height=WINDOW_COL, command=lambda i=i: self.GoToDetail(self.imageM[i]))
            self.MImageButton.image = self.imageM[i]
            self.MImageButton.grid(row=0, column=i, sticky="ew")

        # frame의 길이에 따라 canvas의 길이 조절하기
        self.MFrame.update_idletasks()
        self.MovieCanvas.create_window((0, 0), window=self.MFrame, anchor="nw")
        self.MFrame.bind("<Configure>",self.MovieCanvas.configure(scrollregion=self.MovieCanvas.bbox("all"), width=self.MFrame.winfo_width()))

    def printTrendTv(self):
        self.image=[0]*21
        for i in range(len(self.TvD["results"])):
            self.imageUrl = "https://image.tmdb.org/t/p/w200" + str(self.TvD["results"][i]["poster_path"])
            self.r = requests.get(self.imageUrl)

            self.pilImage = Image.open(BytesIO(self.r.content))
            self.pilImage = self.pilImage.convert('RGB')
            self.pilImage = self.pilImage.resize((180, 250), Image.NEAREST)

            self.image[i] = ImageTk.PhotoImage(self.pilImage)

            # 버튼 안에 이미지 넣기
            self.ImageButton = Button(self.TFrame, image=self.image[i], anchor=N,height=WINDOW_COL, command=lambda i=i: self.GoToDetail(self.image[i]))
            self.ImageButton.image = self.image[i]
            self.ImageButton.grid(row=0, column=i, sticky="ew")

        # frame의 길이에 따라 canvas의 길이 조절하기
        self.TFrame.update_idletasks()
        self.TvCanvas.create_window((0, 0), window=self.TFrame, anchor="nw")
        self.TFrame.bind("<Configure>",self.TvCanvas.configure(scrollregion=self.TvCanvas.bbox("all"), width=self.TFrame.winfo_width()))

    def search(self):
        query = self.search_entry.get()
        url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}&language={language}'
        response = requests.get(url)
        data = response.json()

        results = data['results']
        self.search_movie_listbox.delete(0, END)      # 리스트 박스 요소 모두 제거
        self.search_movie_list = []
        for result in results:
            overview = result['overview']
            title = result['title'].split()
            if language == 'en' and bool(re.match('^[a-zA-Z]+$', title[0][0])):  # 제목이 영어인지 확인한다 / 한글 버전 일시에 한글만 나열함
                self.search_movie_listbox.insert(END, result['title'])
                self.search_movie_list.append(result)
            elif not bool(re.match('^[a-zA-Z]+$', title[0][0])):
                self.search_movie_listbox.insert(END, result['title'])
                self.search_movie_list.append(result)
            # print(f'Overview: {overview}') # 줄거리
    # 선택한 영화의 포스터 이미지를 가져와서 보여주는 함수
    def search_select_show_movie_poster(self,evant):
        index = self.search_movie_listbox.curselection()[0]
        if self.search_movie_list[index]:
            global currentPick
            currentPick = self.search_movie_list[index] # 현재 고른 컨텐츠를 의미함.
            poster_path = self.search_movie_list[index]['poster_path']
            poster_url = f'https://image.tmdb.org/t/p/w500/{poster_path}'
            response = requests.get(poster_url)

            img = Image.open(io.BytesIO(response.content))
            img = img.convert('RGB')
            img = img.resize((180, 250), Image.NEAREST)

            img = ImageTk.PhotoImage(img)
            self.info_poster_label.configure(image=img)
            self.info_poster_label.image = img
        else:
            self.info_poster_label.configure(image='')
            self.info_poster_label.image = None
            currentPick = None
    def AddZzim(self):
        if currentPick != None:
            self.zzim.add_zzim(currentPick)
            print(self.zzim.get_zzimlist())
    def OpenZzimFrame(self):
        new_frame = Toplevel(self.window, width=300, height=600)
        new_frame.geometry('300x600+1000+100')
        new_frame.title('찜 목록')

        # 딕셔너리 데이터
        movie_list = self.zzim.get_zzimlist()

        self.Zzim_listbox = Listbox(new_frame, width=300, height=600, bg='light gray')
        self.Zzim_listbox.place(x=-3, y=0)  # -3 은 리스트박스 경계선 안보이도록

        self.Zzim_listbox.bind('<<ListboxSelect>>', self.Zzim_select_show_movie_poster)
        self.Zzim_list = []
        # 딕셔너리의 키와 값을 리스트 박스에 추가
        for result in movie_list:
            self.Zzim_listbox.insert(END, result['title'])
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
            img = img.resize((180, 250), Image.NEAREST)
            # NEAREST(빠름) , LANCZOS(느림)

            img = ImageTk.PhotoImage(img)
            self.info_poster_label.configure(image=img)
            self.info_poster_label.image = img
        else:
            self.info_poster_label.configure(image='')
            self.info_poster_label.image = None
    def __init__(self):
        self.window = Tk()
        self.window.title("알자비디오")
        self.window.geometry("1000x600+100+100")

        # 검색창
        self.search_entry = Entry(self.window, width=40)
        self.search_entry.place(x=50,y=10)

        # 검색버튼
        self.search_button = Button(self.window, text="검색", command=self.search)
        self.search_button.place(x= 340,y= 5)

        # 검색한 리스트박스
        self.search_movie_listbox = Listbox(self.window,width=40)
        self.search_movie_listbox.place(x=50,y=50)
        self.search_movie_listbox.bind('<<ListboxSelect>>', self.search_select_show_movie_poster)

        # 정보란 포스터 라벨
        self.info_poster_label = Label(self.window, width=180, height=250)
        self.info_poster_label.place(x=50, y=225)

        #==========================준범==================================

        self.MoviePage=1
        #위도우 안에 글
        movieLabel = Label(self.window,text="Trend Movie")
        movieLabel.place(x=WINDOW_ROW/2,y=5)

        tvLabel = Label(self.window,text="Trend Tv")
        tvLabel.place(x=WINDOW_ROW/2,y=WINDOW_COL/2)

        #위도우 안에 프레임
        self.TrendMovieFrame = Frame(self.window,bg="orange")
        #self.TrendMovieFrame.pack(fill="both",expand=True, padx=(WINDOW_ROW/2,0), pady=(0,WINDOW_COL/2))
        self.TrendMovieFrame.place(x=WINDOW_ROW/2,y=30, relwidth=0.5, relheight=0.45)

        self.TrendTvFrame = Frame(self.window, bg="orange")
        #self.TrendTvFrame.pack(fill="both",expand=True, padx=(WINDOW_ROW/2,0), pady=(WINDOW_COL/2,0))
        self.TrendTvFrame.place(x=WINDOW_ROW/2,y=WINDOW_COL/2+30, relwidth=0.5, relheight=0.45)

        #프레임안에 스크롤바
        self.MovieScrollBar = Scrollbar(self.TrendMovieFrame, orient=HORIZONTAL)
        self.MovieScrollBar.pack(side=BOTTOM, fill=X)

        self.TvScrollBar = Scrollbar(self.TrendTvFrame, orient=HORIZONTAL)
        self.TvScrollBar.pack(side=BOTTOM, fill=X)

        # 캔버스 생성
        self.MovieCanvas = Canvas(self.TrendMovieFrame,xscrollcommand=self.MovieScrollBar.set,bg="cyan")
        self.MovieCanvas.pack(side=LEFT, fill=BOTH, expand = True)

        self.TvCanvas = Canvas(self.TrendTvFrame,xscrollcommand=self.TvScrollBar.set,bg="red")
        self.TvCanvas.pack(side=LEFT, fill=BOTH, expand = True)

        # 스크롤바와 캔버스 연결
        self.MovieScrollBar.config(command=self.MovieCanvas.xview)
        self.TvScrollBar.config(command=self.TvCanvas.xview)

        # 캔버스안에 프레임 설정
        self.MFrame = Frame(self.MovieCanvas, bg="cyan")
        self.TFrame = Frame(self.TvCanvas, bg="cyan")

        # 폰트
        self.fontstyle = font.Font(self.window, size=24, weight='bold', family='Consolas')
        self.fontstyle2 = font.Font(self.window, size=16, weight='bold', family='Consolas')

        #api불러오기
        self.fetchMovieData()
        self.fetchTvData()

        # ==========================준범==================================

        # --------------------------정일----------------------------------
        # 찜 버튼 만들기 (동그라미 버튼)
        image = Image.open("resource/Circle.png")
        # 이미지 사이즈 조절
        image_with_alpha = image.convert("RGBA")
        resized_image = image_with_alpha.resize((50, 50))
        # 이미지를 PhotoImage로 변환
        photo = ImageTk.PhotoImage(resized_image)
        # 버튼 생성 및 이미지 설정
        Button(self.window, image=photo, bd=0, command=self.AddZzim).place(x=0, y=550)

        image = Image.open("resource/Zzimlist.png")
        image_with_alpha = image.convert("RGBA")
        resized_image = image_with_alpha.resize((50, 50))
        photo2 = ImageTk.PhotoImage(resized_image)
        # 찜 목록 버튼
        Button(self.window, image=photo2, bd=0, command=self.OpenZzimFrame).place(x=450, y=550)

        # 찜 변수 선언
        self.zzim = zzim.ZZIM()
        # ----------------------------------------------------------------

        self.window.mainloop()



MainGUI()