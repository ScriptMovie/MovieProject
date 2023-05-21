from tkinter import *
from PIL import Image, ImageDraw, ImageTk
import io
import requests
import re
import zzim
import math
# TMDB API = 9f0490f698de8457de01c1f761c6fdc1

api_key = '9f0490f698de8457de01c1f761c6fdc1'
language = 'ko-KR'
# language = 'en'

# -----------------------------------------------------------------------------
# 현재 고른 컨텐츠를 나타냄
currentPick = None
# -----------------------------------------------------------------------------


class MainGUI:
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
    def search_select_show_movie_poster(self,evant): # 함수명 변경
        index = self.search_movie_listbox.curselection()[0]
        if self.search_movie_list[index]:
            # -----------------------------------------------------------------------------
            global currentPick
            currentPick = self.search_movie_list[index] # 현재 고른 컨텐츠를 의미함.
            # -----------------------------------------------------------------------------
            poster_path = self.search_movie_list[index]['poster_path']
            poster_url = f'https://image.tmdb.org/t/p/w500/{poster_path}'
            response = requests.get(poster_url)
            # img_data = response.content

            img = Image.open(io.BytesIO(response.content))
            img = img.convert('RGB')
            img = img.resize((200, 300), Image.LANCZOS)
            # NEAREST(빠름) , LANCZOS(느림)

            img = ImageTk.PhotoImage(img)
            self.poster_label.configure(image=img)
            self.poster_label.image = img
        else:
            self.poster_label.configure(image='')
            self.poster_label.image = None
            # -----------------------------------------------------------------------------
            currentPick = None
            # -----------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------
    def AddZzim(self):
        if currentPick != None:
            self.zzim.add_zzim(currentPick)
            print(self.zzim.get_zzimlist())
    def OpenZzimFrame(self):
        new_frame = Toplevel(self.window,width=300,height=600)
        new_frame.geometry('300x600+900+100')
        new_frame.title('찜 목록')

        # 딕셔너리 데이터
        movie_list = self.zzim.get_zzimlist()

        self.Zzim_listbox = Listbox(new_frame,width=300,height=600,bg='light gray')
        self.Zzim_listbox.place(x=-3,y=0) # -3 은 리스트박스 경계선 안보이도록

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
            img = img.resize((200, 300), Image.LANCZOS)
            # NEAREST(빠름) , LANCZOS(느림)

            img = ImageTk.PhotoImage(img)
            self.poster_label.configure(image=img)
            self.poster_label.image = img
        else:
            self.poster_label.configure(image='')
            self.poster_label.image = None
    # -------------------------------------------------------------------------------------------
    def __init__(self):
        self.window = Tk()
        self.window.title("알자비디오")
        self.window.geometry("800x600+100+100")
        # window.resizable(True, True)

        self.search_entry = Entry(self.window, width=40)
        self.search_entry.place(x=50,y=10)

        self.search_button = Button(self.window, text="검색", command=self.search)
        self.search_button.place(x= 340,y= 5)

        self.search_movie_listbox = Listbox(self.window,width=40)
        self.search_movie_listbox.place(x=50,y=50)

        self.search_movie_listbox.bind('<<ListboxSelect>>', self.search_select_show_movie_poster)

        self.poster_label = Label(self.window,width=200,height=300)
        self.poster_label.place(x=50,y=250)

        # -----------------------------------------------------------------------------
        # 찜 버튼 만들기 (동그라미 버튼)
        image = Image.open("resource/Circle.png")
        # 이미지 사이즈 조절
        image_with_alpha = image.convert("RGBA")
        resized_image = image_with_alpha.resize((50,50))
        # 이미지를 PhotoImage로 변환
        photo = ImageTk.PhotoImage(resized_image)
        # 버튼 생성 및 이미지 설정
        Button(self.window, image=photo,bd=0,command=self.AddZzim).place(x=0, y=550)

        # 찜 목록 버튼 # 위 방식과 똑같이 목록 버튼 이미지를 불러오자
        Button(self.window, image=photo,bd=0,command=self.OpenZzimFrame).place(x=600, y=550)

        # 찜 변수 선언
        self.zzim = zzim.ZZIM()
        # -----------------------------------------------------------------------------
        self.window.mainloop()



MainGUI()