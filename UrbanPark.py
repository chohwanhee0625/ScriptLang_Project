import library_file
from library_file import *



class UrbanPark:
    url = "https://openapi.gg.go.kr/CityPark"
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

    parks = []
    for item in items:
        park = {
            "name": item.findtext("PARK_NM"),
            "type": item.findtext("PARK_DIV_NM"),
            "addr": item.findtext("REFINE_ROADNM_ADDR"),
            "si": item.findtext("SIGUN_NM"),
            "telno": item.findtext("MANAGE_INST_TELNO"),
            "manage": item.findtext("MANAGE_INST_NM"),
            "area": item.findtext("PARK_AR"),
            "facil": [],
            "data_type": "공원"
        }
        park['facil'].append(item.findtext("PARK_SPORTS_FACLT_DTLS"))
        park['facil'].append(item.findtext("PARK_AMSMT_FACLT_DTLS"))
        park['facil'].append(item.findtext("PARK_CNVNC_FACLT_DTLS"))
        park['facil'].append(item.findtext("PARK_CLTR_FACLT_DTLS"))
        park['facil'].append(item.findtext("PARK_ETC_FACLT_DTLS	"))

        search_park = park['si'] + ' +' + park['name']

        parks.append(park)

    def __init__(self, frame):

        self.selected_si = StringVar()
        self.selected_si.set("시흥시")  # 초기값 설정
        self.si_options = set()
        for park in self.parks:
            if park['si']:
                self.si_options.add(park['si'])
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

        # 공원 목록 리스트박스 생성
        self.park_list = Listbox(frame2, width=50)
        self.park_list.pack(side=LEFT)

        # 스크롤바 생성
        scrollbar = Scrollbar(frame2)
        scrollbar.pack(side=RIGHT, fill=Y)

        # 스크롤바와 공원 목록 연결
        self.park_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.park_list.yview)

        self.si_combo.bind("<<ComboboxSelected>>", self.on_si_select)

        self.show_parks()

        # 공원 정보 출력 캔버스 생성
        self.park_info = Canvas(frame1, width=300, height=200, bg='white')
        self.park_info.pack(side=RIGHT)
        
        # 정보 출력을 위한 버튼, 나중에 리스트 항목 클릭 시 정보 출력하도록 변경
        Button(frame, width=5, text='출력', command=self.show_info).pack()

        # 선택 항목 공원 이미지 출력 캔버스
        self.park_type = Canvas(frame3, width=380, height=250, bg='white')
        self.park_type.pack(side=LEFT)
        self.show_types()

        # 지도 이미지 캔버스 생성
        map_img = Canvas(frame3, width=300, height=250, bg='white')
        map_img.pack()

    def show_parks(self):
        self.park_list.delete(0, END)

        si_name = self.selected_si.get()
        self.parks_in_si = [park for park in self.parks if park['si'] == si_name]

        # 공원 목록에 추가
        for park in self.parks_in_si:
            self.park_list.insert(END, f"{park['name']} ({park['type']})")

    def on_si_select(self, event):
        # 콤보박스 시군 선택 시 해당 시에 맞는 정보 업데이트 이벤트 함수
        self.show_parks()
        self.show_types()

    def show_info(self):
        # 리스트박스 오른쪽에 정보를 나타내는 이벤트 함수
        self.park_info.delete('all')

        name_font = font.Font(size=13, weight='bold', family='Consolas')
        temp_font = font.Font(size=10, family='Consolas')
        a = self.park_list.curselection()
        if a:
            park = self.parks_in_si[a[0]]

            self.park_info.create_text(150, 15, font=name_font, text=park['name'])

            self.park_info.create_text(30, 45, font=temp_font, text="주소: ")
            self.park_info.create_text(170, 45, font=temp_font, text=park['addr'][:13])
            self.park_info.create_text(170, 60, font=temp_font, text=park['addr'][13:])

            self.park_info.create_text(45, 80, font=temp_font, text="공원 종류: ")
            self.park_info.create_text(170, 80, font=temp_font, text=park['type'])

            self.park_info.create_text(42, 100, font=temp_font, text="전화번호: ")
            self.park_info.create_text(170, 100, font=temp_font, text=park['telno'])

            self.park_info.create_text(55, 120, font=temp_font, text="공원 내 시설: ")
            facils = ''
            for facil in park['facil']:
                if facil:
                    facils += ' ' + facil
            self.park_info.create_text(170, 120, font=temp_font, text=facils.split())

            self.park_info.create_text(75, 140, font=temp_font, text="공원 면적(평방미터): ")
            self.park_info.create_text(170, 140, font=temp_font, text=park['area'])

            self.park_info.create_text(45, 160, font=temp_font, text="담당 기관: ")
            self.park_info.create_text(170, 160, font=temp_font, text=park['manage'])

    def show_types(self):
        pass

    def add_favorite(self):
        a = self.park_list.curselection()
        if a:
            park = self.parks_in_si[a[0]]
            if park not in library_file.favorites:
                library_file.favorites.append(park)



