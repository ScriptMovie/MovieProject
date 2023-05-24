from tkinter import *
from tkinter import font

# 현재 고른 컨텐츠를 나타냄
currentPick = None

class GOTODETAIL:
    def __init__(self,info_poster,window,img,data,kind):
        global currentPick
        currentPick = data
        # 이미지 클릭시 화면에 이미지 출력
        info_poster.configure(image=img)
        info_poster.image = img

        # 개요의 최대 글자 수 설정
        max_characters = 70  # 최대 글자 수 설정
        original_text = data["overview"]
        truncated_text = original_text[:max_characters] + "..." if len(
            original_text) > max_characters else original_text

        # 예전 text가리기
        self.info_hide = Label(window, width=35, height=20)
        self.info_hide.place(x=240, y=225)

        # 정보란 콘텐츠 정보

        # 폰트
        fontTitle = font.Font(window, size=16, weight='bold', family='Consolas')
        fontOverview = font.Font(window, size=12, weight='bold', family='Consolas')

        # 제목,출시일
        if kind == "M":  # 영화
            #제목
            self.info_title_label = Label(window, text=data["title"], wraplength=240, justify='left',
                                          font=fontTitle)
            self.info_title_label.place(x=240, y=225)
            #출시일
            self.info_release_label = Label(window,text=data["release_date"],justify='left')
            self.info_release_label.place(x=240,y=300)
        elif kind == "T":  # TV
            #제목
            self.info_title_label = Label(window, text=data["name"], wraplength=240, justify='left',
                                          font=fontTitle)
            self.info_title_label.place(x=240, y=225)
            #출시일
            self.info_release_label = Label(window,text=data["first_air_date"],justify='left')
            self.info_release_label.place(x=240,y=300)

        # 별점
        for i in range(round(data["vote_average"])):
            self.star_label = Label(window, text="⭐", fg="red")
            self.star_label.place(x=240 + i * 20, y=280)


        # 설명
        self.info_overview_label = Label(window, text=truncated_text, wraplength=200, justify='left',
                                         font=fontOverview)
        self.info_overview_label.place(x=240, y=320)
