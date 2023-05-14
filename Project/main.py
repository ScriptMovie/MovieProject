from tkinter import *
from PIL import Image, ImageTk
import io
import requests
import re

# TMDB API = 9f0490f698de8457de01c1f761c6fdc1

api_key = '9f0490f698de8457de01c1f761c6fdc1'
language = 'ko-KR'
# language = 'en'

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
            print(f'Overview: {overview}') # 줄거리

    # 선택한 영화의 포스터 이미지를 가져와서 보여주는 함수
    def show_movie_poster(self,evant):
        index = self.search_movie_listbox.curselection()[0]
        if self.search_movie_list[index]:
            poster_path = self.search_movie_list[index]['poster_path']
            poster_url = f'https://image.tmdb.org/t/p/w500/{poster_path}'
            response = requests.get(poster_url)
            # img_data = response.content

            img = Image.open(io.BytesIO(response.content))
            img = img.convert('RGB')
            img = img.resize((200, 300), Image.LANCZOS)
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
        self.window.geometry("1000x600")

        # 검색창
        self.search_entry = Entry(self.window, width=40)
        self.search_entry.place(x=50,y=10)

        # 검색버튼
        self.search_button = Button(self.window, text="검색", command=self.search)
        self.search_button.place(x= 340,y= 5)

        # 검색한 리스트박스
        self.search_movie_listbox = Listbox(self.window,width=40)
        self.search_movie_listbox.place(x=50,y=50)
        self.search_movie_listbox.bind('<<ListboxSelect>>', self.show_movie_poster)

        # 정보란 포스터 라벨
        self.info_poster_label = Label(self.window, width=200, height=300)
        self.info_poster_label.place(x=50, y=250)

        self.window.mainloop()



MainGUI()