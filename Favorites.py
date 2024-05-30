import mysmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import library_file
from library_file import *


class Favorites:
    favorites = library_file.favorites
    Google_API_Key = 'AIzaSyCzFgc9OGnXckq1-JNhSCVGo9zIq1kSWcE'
    gmaps = Client(key=Google_API_Key)

    # smtp 정보
    host = "smtp.gmail.com"  # Gmail SMTP 서버 주소.
    port = "587"

    sender_addr = "great1625@tukorea.ac.kr"
    passwd = "vdfi vwpx pqca ggde"


    def __init__(self, frame):

        button_frame = Frame(frame)
        button_frame.pack()

        # 갱신용 버튼, 나중엔 추가하면 자동으로 갱신되게 바꿔보자
        Button(button_frame, text='갱신', command=self.show_favorites).pack(side=LEFT)

        Button(button_frame, text='삭제', command=self.delete_favorite).pack(side=LEFT)
        Button(button_frame, text='메일', command=self.send_mail).pack(side=LEFT)

        # 정보 출력을 위한 버튼, 나중에 리스트 항목 클릭 시 정보 출력하도록 변경
        Button(frame, width=5, text='출력', command=self.show_info).pack()

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

        # 선택 항목 지도 이미지 라벨 생성
        self.fav_map = Label(frame3, width=300, height=200, bg='white')
        self.fav_map.pack()

    def show_favorites(self):
        self.favorite_list.delete(0, END)

        # 즐겨찾기 목록에 추가
        for favorite in self.favorites:
            if any(type == favorite['data_type'] for type in ['편의점', '공원', '체육시설', '공중화장실']):
                self.favorite_list.insert(END, f"{favorite['name']} ({favorite['type']})")

    def delete_favorite(self):
        a = self.favorite_list.curselection()
        if a:
            target = self.favorites[a[0]]
            self.favorites.remove(target)

        self.show_favorites()

    def show_map(self):
        a = self.favorite_list.curselection()
        if a:
            target = self.favorites[a[0]]
            lat, lng = float(target['lat']), float(target['lng'])
            si_map_url = (f"https://maps.googleapis.com/maps/api/staticmap?center="
                          f"{lat},{lng}&zoom=17&size=300x250&maptype=roadmap")

            # 위치 마커 추가
            if target['lat'] and target['lng']:
                lat, lng = float(target['lat']), float(target['lng'])
                marker_url = f"&markers=color:red%7C{lat},{lng}"
                si_map_url += marker_url

            # 지도 이미지 업데이트
            response = requests.get(si_map_url + '&key=' + self.Google_API_Key)
            image = Image.open(io.BytesIO(response.content))
            photo = ImageTk.PhotoImage(image)
            self.fav_map.configure(image=photo)
            self.fav_map.image = photo

    def show_info(self):
        self.show_map()

        self.fav_info.delete('all')

        name_font = font.Font(size=13, weight='bold', family='Consolas')
        temp_font = font.Font(size=10, family='Consolas')
        a = self.favorite_list.curselection()
        if a:
            favorite = self.favorites[a[0]]
            if favorite['data_type'] == '공원':
                park = favorite

                self.fav_info.create_text(150, 15, font=name_font, text=park['name'])

                self.fav_info.create_text(30, 45, font=temp_font, text="주소: ")
                self.fav_info.create_text(170, 45, font=temp_font, text=park['addr'][:13])
                self.fav_info.create_text(170, 60, font=temp_font, text=park['addr'][13:])

                self.fav_info.create_text(45, 80, font=temp_font, text="공원 종류: ")
                self.fav_info.create_text(170, 80, font=temp_font, text=park['type'])

                self.fav_info.create_text(42, 100, font=temp_font, text="전화번호: ")
                self.fav_info.create_text(170, 100, font=temp_font, text=park['telno'])

                self.fav_info.create_text(55, 120, font=temp_font, text="공원 내 시설: ")
                facils = ''
                for facil in park['facil']:
                    if facil:
                        facils += ' ' + facil
                self.fav_info.create_text(170, 120, font=temp_font, text=facils.split())

                self.fav_info.create_text(75, 140, font=temp_font, text="공원 면적(평방미터): ")
                self.fav_info.create_text(170, 140, font=temp_font, text=park['area'])

                self.fav_info.create_text(45, 160, font=temp_font, text="담당 기관: ")
                self.fav_info.create_text(170, 160, font=temp_font, text=park['manage'])
            elif favorite['data_type'] == '편의점':
                store = favorite

                self.fav_info.create_text(150, 15, font=name_font, text=store['name'])

                self.fav_info.create_text(30, 45, font=temp_font, text="주소: ")
                self.fav_info.create_text(170, 45, font=temp_font, text=store['addr'][:18])
                self.fav_info.create_text(170, 60, font=temp_font, text=store['addr'][18:])

                self.fav_info.create_text(52, 90, font=temp_font, text="편의점 종류: ")
                self.fav_info.create_text(170, 90, font=temp_font, text=store['type'])

                self.fav_info.create_text(45, 120, font=temp_font, text="운영 상태: ")
                self.fav_info.create_text(170, 120, font=temp_font, text=store['state'])

                self.fav_info.create_text(42, 150, font=temp_font, text="전화번호: ")
                self.fav_info.create_text(170, 150, font=temp_font, text=store['telno'])
            
            elif favorite['data_type'] == '체육시설':
                sport = favorite

                self.fav_info.create_text(150, 15, font=name_font, text=sport['name'])

                self.fav_info.create_text(30, 45, font=temp_font, text="주소: ")
                self.fav_info.create_text(170, 45, font=temp_font, text=sport['addr'][:13])
                self.fav_info.create_text(170, 60, font=temp_font, text=sport['addr'][13:])

                self.fav_info.create_text(57, 100, font=temp_font, text="체육시설 구분: ")
                self.fav_info.create_text(170, 100, font=temp_font, text=sport['type'])

                self.fav_info.create_text(42, 140, font=temp_font, text="전화번호: ")
                self.fav_info.create_text(170, 140, font=temp_font, text=sport['telno'])

            elif favorite['data_type'] == '공중화장실':
                toilet = favorite

                self.fav_info.create_text(150, 15, font=name_font, text=toilet['name'])

                self.fav_info.create_text(30, 45, font=temp_font, text="주소: ")
                self.fav_info.create_text(170, 45, font=temp_font, text=toilet['addr'][:13])
                self.fav_info.create_text(170, 60, font=temp_font, text=toilet['addr'][13:])

                self.fav_info.create_text(52, 80, font=temp_font, text="화장실 종류: ")
                self.fav_info.create_text(170, 80, font=temp_font, text=toilet['type'])

                self.fav_info.create_text(45, 100, font=temp_font, text="개방 시간: ")
                self.fav_info.create_text(170, 100, font=temp_font, text=toilet['time'])

                self.fav_info.create_text(45, 120, font=temp_font, text="남녀 공용: ")
                self.fav_info.create_text(170, 120, font=temp_font, text=toilet['unisex'])

                self.fav_info.create_text(50, 140, font=temp_font, text="기저귀 교환대")
                self.fav_info.create_text(170, 140, font=temp_font, text=toilet['nappy'])

                self.fav_info.create_text(42, 160, font=temp_font, text="전화번호: ")
                self.fav_info.create_text(170, 160, font=temp_font, text=toilet['telno'])

                self.fav_info.create_text(45, 180, font=temp_font, text="관리 기관: ")
                self.fav_info.create_text(170, 180, font=temp_font, text=toilet['manage'])
