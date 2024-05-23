from library_file import *


class Favorites:
    favorites = []
    def __init__(self, frame):
        Button(frame, text='삭제').pack()
        Button(frame, text='메일').pack()

        # 간격 조절을 위한 더미 프레임
        Frame(frame, height=20).pack()

        # 메인 프레임
        frame1 = Frame(frame)
        frame1.pack()

        # 리스트 박스와 스크롤바를 담을 프레임
        frame2 = Frame(frame1)
        frame2.pack(side=LEFT)

        # 간격 조절을 위한 더미 프레임
        Frame(frame1, width=10).pack(side=LEFT)

        # 선택 항목 정보와 지도 이미지를 담을 프레임
        frame3 = Frame(frame1)
        frame3.pack(side=LEFT)
        
        # 즐겨찾기 리스트박스 생성
        self.favorite_list = Listbox(frame2, width=50, height=25)
        self.favorite_list.pack(side=LEFT)

        # 스크롤바 생성
        scrollbar = Scrollbar(frame2)
        scrollbar.pack(side=RIGHT, fill=Y)

        # 스크롤바와 즐겨찾기 목록 연결
        self.favorite_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.favorite_list.yview)

        self.show_favorites()

        # 선택 항목 정보 출력 캔버스 생성
        fav_info = Canvas(frame3, width=300, height=200, bg='white')
        fav_info.pack()

        # 간격 조절을 위한 더미 프레임
        Frame(frame3, height=10).pack()

        # 선택 항목 지도 이미지 캔버스 생성
        fav_map = Canvas(frame3, width=300, height=200, bg='white')
        fav_map.pack()

    def show_favorites(self):
        self.favorite_list.delete(0, END)

        # 공원 목록에 추가
        for favorite in self.favorites:
            self.favorite_list.insert(END, f"{favorite['name']} ({favorite['type']})")
