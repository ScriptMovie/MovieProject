from tkinter import *
from tkinter import font

# 현재 고른 컨텐츠를 나타냄
currentPick = None

class GOTODETAIL:
    def __init__(self,info_poster,window,img,data,kind):
        x_offset = 100
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
        self.info_hide = Label(window, width=29, height=20)
        self.info_hide.place(x=240+x_offset, y=225)
        self.info_hide.configure(bg='#FFA500')

        # 정보란 콘텐츠 정보

        # 폰트
        fontTitle = font.Font(window, size=16, weight='bold', family='Consolas')
        fontOverview = font.Font(window, size=12, weight='bold', family='Consolas')

        # 제목,출시일
        if kind == "M":  # 영화
            #제목
            self.info_title_label = Label(window, text=data["title"], wraplength=200, justify='left',
                                          font=fontTitle)
            self.info_title_label.configure(bg='#FFA500')
            self.info_title_label.place(x=240+x_offset, y=225)
            #출시일
            self.info_release_label = Label(window,text="개봉일: " + data["release_date"],justify='left')
            self.info_release_label.configure(bg='#FFA500')
            self.info_release_label.place(x=240+x_offset,y=330)
        elif kind == "T":  # TV
            #제목
            self.info_title_label = Label(window, text=data["name"], wraplength=200, justify='left',
                                          font=fontTitle)
            self.info_title_label.configure(bg='#FFA500')
            self.info_title_label.place(x=240+x_offset, y=225)
            #출시일
            self.info_release_label = Label(window,text="방영일: " + data["first_air_date"],justify='left')
            self.info_release_label.configure(bg='#FFA500')
            self.info_release_label.place(x=240+x_offset,y=330)

        # 별점
        for i in range(round(data["vote_average"])):
            self.star_label = Label(window, text="⭐", fg="red")
            self.star_label.configure(bg='#FFA500')
            self.star_label.place(x=240+x_offset + i * 20, y=310)


        # 설명
        self.info_overview_label = Label(window, text=truncated_text, wraplength=200, justify='left',
                                         font=fontOverview)
        self.info_overview_label.configure(bg='#FFA500')
        self.info_overview_label.place(x=240+x_offset, y=350)
