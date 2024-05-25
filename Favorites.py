import UrbanPark
import library_file
from library_file import *


class Favorites:
    favorites = library_file.favorites
    def __init__(self, frame):

        button_frame = Frame(frame)
        button_frame.pack()

        # 갱신용 버튼, 나중엔 추가하면 자동으로 갱신되게 바꿔보자
        Button(button_frame, text='갱신', command=self.show_favorites).pack(side=LEFT)

        Button(button_frame, text='삭제', command=self.delete_favorite).pack(side=LEFT)
        Button(button_frame, text='메일').pack(side=LEFT)

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
        self.fav_info = Canvas(frame3, width=300, height=200, bg='white')
        self.fav_info.pack()

        # 간격 조절을 위한 더미 프레임
        Frame(frame3, height=10).pack()

        # 선택 항목 지도 이미지 캔버스 생성
        self.fav_map = Canvas(frame3, width=300, height=200, bg='white')
        self.fav_map.pack()

    def show_favorites(self):
        self.favorite_list.delete(0, END)

        # 공원 목록에 추가
        for favorite in self.favorites:
            if any(type == favorite['data_type'] for type in ['편의점', '공원']):
                self.favorite_list.insert(END, f"{favorite['name']} ({favorite['type']})")

    def delete_favorite(self):
        a = self.favorite_list.curselection()
        if a:
            target = self.favorites[a[0]]
            self.favorites.remove(target)

        self.show_favorites()

    def show_info(self):
        self.fav_info.delete('all')

        name_font = font.Font(size=13, weight='bold', family='Consolas')
        temp_font = font.Font(size=10, family='Consolas')
        a = self.favorite_list.curselection()
        if a:
            favorite = self.favorites[a[0]]
            if favorite['data_type'] == '편의점':
                pass


