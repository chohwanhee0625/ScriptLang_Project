import library_file
from library_file import *


class SportsCenter:
    url = "https://openapi.gg.go.kr/PubPhstFtM"
    params = {
        "KEY": "874d62100e224676a4f0cd46e40b3da5",
        "Type": "xml",
        "pIndex": "1",
        "pSize": "1000"
    }

    response = requests.get(url, params=params)
    root = ET.fromstring(response.text)
    items = root.findall(".//row")
    # items = root.iter("row")

    sports = []
    for item in items:
        sport = {
            "name": item.findtext("FACLT_NM"),
            "type": item.findtext("FACLT_DIV_NM"),
            "addr": item.findtext("REFINE_ROADNM_ADDR"),
            "si": item.findtext("SIGUN_NM"),
            "telno": item.findtext("CONTCT_NO"),
            "data_type": "체육시설",
            "lat": item.findtext("REFINE_WGS84_LAT"),
            "lng": item.findtext("REFINE_WGS84_LOGT")
        }
        if not sport['addr']:
            sport['addr'] = '정보 없음'
        if not sport['telno']:
            sport['telno'] = '정보 없음'
        sports.append(sport)

    Google_API_Key = 'AIzaSyCzFgc9OGnXckq1-JNhSCVGo9zIq1kSWcE'
    gmaps = Client(key=Google_API_Key)

    def __init__(self, frame):

        self.selected_si = StringVar()
        self.selected_si.set("시흥시")  # 초기값 설정
        self.si_options = set()
        for sport in self.sports:
            if sport['si']:
                self.si_options.add(sport['si'])
        self.si_combo = ttk.Combobox(frame, textvariable=self.selected_si, values=list(self.si_options))
        self.si_combo.pack()

        # 즐겨찾기 버튼
        Button(frame, width=2, text='즐찾', command=self.add_favorite).pack()

        # 메인 프레임
        frame1 = Frame(frame)
        frame1.pack()

        # 리스트 박스와 스크롤바 담을 프레임
        frame2 = Frame(frame1)
        frame2.pack(side=LEFT)

        Frame(frame, height=10).pack()

        # 통계 캔버스와 지도 이미지 캔버스 담을 프레임
        frame3 = Frame(frame)
        frame3.pack()

        # 체육시설 목록 리스트박스 생성
        self.sport_list = Listbox(frame2, width=50)
        self.sport_list.pack(side=LEFT)

        # 스크롤바 생성
        scrollbar = Scrollbar(frame2)
        scrollbar.pack(side=RIGHT, fill=Y)

        # 스크롤바와 체육시설 목록 연결
        self.sport_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.sport_list.yview)

        self.si_combo.bind("<<ComboboxSelected>>", self.on_si_select)

        self.show_sports()

        # 체육시설 정보 출력 캔버스 생성
        self.sport_info = Canvas(frame1, width=300, height=200, bg='white')
        self.sport_info.pack(side=RIGHT)

        # 정보 출력을 위한 버튼, 나중에 리스트 항목 클릭 시 정보 출력하도록 변경
        Button(frame, width=5, text='출력', command=self.show_info).pack()

        # 통계 캔버스 생성, 막대 그래프 그리기
        self.sport_type = Canvas(frame3, width=380, height=250, bg='white')
        self.sport_type.pack(side=LEFT)
        self.show_types()

        # 지도 이미지 라벨 생성
        self.map_img = Label(frame3, width=300, height=250, bg='white')
        self.map_img.pack()
        self.show_map()

    def show_sports(self):
        self.sport_list.delete(0, END)

        si_name = self.selected_si.get()
        self.sports_in_si = [sport for sport in self.sports if sport['si'] == si_name]

        # 체육시설 목록에 추가
        for sport in self.sports_in_si:
            self.sport_list.insert(END, f"{sport['name']} ({sport['type']})")

    def on_si_select(self, event):
        # 콤보박스 시군 선택 시 해당 시에 맞는 정보 업데이트 이벤트 함수
        self.show_sports()
        self.show_map()

    def show_info(self):
        # 리스트박스 오른쪽에 정보를 나타내는 이벤트 함수
        self.sport_info.delete('all')

        name_font = font.Font(size=13, weight='bold', family='Consolas')
        temp_font = font.Font(size=10, family='Consolas')
        a = self.sport_list.curselection()
        if a:
            sport = self.sports_in_si[a[0]]

            self.sport_info.create_text(150, 15, font=name_font, text=sport['name'])

            self.sport_info.create_text(30, 45, font=temp_font, text="주소: ")
            self.sport_info.create_text(170, 45, font=temp_font, text=sport['addr'][:13])
            self.sport_info.create_text(170, 60, font=temp_font, text=sport['addr'][13:])

            self.sport_info.create_text(57, 100, font=temp_font, text="체육시설 구분: ")
            self.sport_info.create_text(170, 100, font=temp_font, text=sport['type'])

            self.sport_info.create_text(42, 140, font=temp_font, text="전화번호: ")
            self.sport_info.create_text(170, 140, font=temp_font, text=sport['telno'])

    def show_types(self):
        pass

    def add_favorite(self):
        a = self.sport_list.curselection()
        if a:
            sport = self.sports_in_si[a[0]]
            if sport not in library_file.favorites:
                library_file.favorites.append(sport)

    def show_map(self):
        si_name = self.selected_si.get()
        si_center = self.gmaps.geocode(f"{si_name}")[0]['geometry']['location']
        si_map_url = (f"https://maps.googleapis.com/maps/api/staticmap?center="
                      f"{si_center['lat']},{si_center['lng']}&zoom=12&size=300x250&maptype=roadmap")

        # 선택한 시/군의 시설 위치 마커 추가
        for sport in self.sports_in_si:
            if sport['lat'] and sport['lng']:
                lat, lng = float(sport['lat']), float(sport['lng'])
                marker_url = f"&markers=color:red%7C{lat},{lng}"
                si_map_url += marker_url

            # 지도 이미지 업데이트
            response = requests.get(si_map_url + '&key=' + self.Google_API_Key)
            image = Image.open(io.BytesIO(response.content))
            photo = ImageTk.PhotoImage(image)
            self.map_img.configure(image=photo)
            self.map_img.image = photo

