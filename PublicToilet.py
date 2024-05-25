import library_file
from library_file import *


class PublicToilet:
    url = "https://openapi.gg.go.kr/Publtolt"
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

    toilets = []
    for item in items:
        toilet = {
            "name": item.findtext("PBCTLT_PLC_NM"),
            "type": item.findtext("PUBLFACLT_DIV_NM"),
            "addr": item.findtext("REFINE_ROADNM_ADDR"),
            "si": item.findtext("SIGUN_NM"),
            "telno": item.findtext("MANAGE_INST_TELNO"),
            "manage": item.findtext("MANAGE_INST_NM"),
            "area": item.findtext("toilet_AR"),
            "facil": [],
            "data_type": "공중화장실"
        }
        toilet['facil'].append(item.findtext("toilet_SPORTS_FACLT_DTLS"))
        toilet['facil'].append(item.findtext("toilet_AMSMT_FACLT_DTLS"))
        toilet['facil'].append(item.findtext("toilet_CNVNC_FACLT_DTLS"))
        toilet['facil'].append(item.findtext("toilet_CLTR_FACLT_DTLS"))
        toilet['facil'].append(item.findtext("toilet_ETC_FACLT_DTLS	"))

        search_toilet = toilet['si'] + ' +' + toilet['name']

        toilets.append(toilet)

    def __init__(self, frame):

        self.selected_si = StringVar()
        self.selected_si.set("시흥시")  # 초기값 설정
        self.si_options = set()
        for toilet in self.toilets:
            if toilet['si']:
                self.si_options.add(toilet['si'])
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
        self.toilet_list = Listbox(frame2, width=50)
        self.toilet_list.pack(side=LEFT)

        # 스크롤바 생성
        scrollbar = Scrollbar(frame2)
        scrollbar.pack(side=RIGHT, fill=Y)

        # 스크롤바와 공원 목록 연결
        self.toilet_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.toilet_list.yview)

        self.si_combo.bind("<<ComboboxSelected>>", self.on_si_select)

        self.show_toilets()

        # 공원 정보 출력 캔버스 생성
        self.toilet_info = Canvas(frame1, width=300, height=200, bg='white')
        self.toilet_info.pack(side=RIGHT)

        # 정보 출력을 위한 버튼, 나중에 리스트 항목 클릭 시 정보 출력하도록 변경
        Button(frame, width=5, text='출력', command=self.show_info).pack()

        # 선택 항목 화장실 시설 표시 캔버스 (장애인 화장실, 기저귀 교환대, 어린이용 화장실 여부)
        self.toilet_type = Canvas(frame3, width=380, height=250, bg='white')
        self.toilet_type.pack(side=LEFT)
        self.show_types()

        # 지도 이미지 캔버스 생성
        map_img = Canvas(frame3, width=300, height=250, bg='white')
        map_img.pack()

    def show_toilets(self):
        self.toilet_list.delete(0, END)

        si_name = self.selected_si.get()
        self.toilets_in_si = [toilet for toilet in self.toilets if toilet['si'] == si_name]

        # 공원 목록에 추가
        for toilet in self.toilets_in_si:
            self.toilet_list.insert(END, f"{toilet['name']} ({toilet['type']})")

    def on_si_select(self, event):
        # 콤보박스 시군 선택 시 해당 시에 맞는 정보 업데이트 이벤트 함수
        self.show_toilets()
        self.show_types()

    def show_info(self):
        # 리스트박스 오른쪽에 정보를 나타내는 이벤트 함수
        self.toilet_info.delete('all')

        name_font = font.Font(size=13, weight='bold', family='Consolas')
        temp_font = font.Font(size=10, family='Consolas')
        a = self.toilet_list.curselection()
        if a:
            toilet = self.toilets_in_si[a[0]]

            self.toilet_info.create_text(150, 15, font=name_font, text=toilet['name'])

            self.toilet_info.create_text(30, 45, font=temp_font, text="주소: ")
            self.toilet_info.create_text(170, 45, font=temp_font, text=toilet['addr'][:13])
            self.toilet_info.create_text(170, 60, font=temp_font, text=toilet['addr'][13:])

            self.toilet_info.create_text(45, 80, font=temp_font, text="공원 종류: ")
            self.toilet_info.create_text(170, 80, font=temp_font, text=toilet['type'])

            self.toilet_info.create_text(42, 100, font=temp_font, text="전화번호: ")
            self.toilet_info.create_text(170, 100, font=temp_font, text=toilet['telno'])

            self.toilet_info.create_text(55, 120, font=temp_font, text="공원 내 시설: ")
            facils = ''
            for facil in toilet['facil']:
                if facil:
                    facils += ' ' + facil
            self.toilet_info.create_text(170, 120, font=temp_font, text=facils.split())

            self.toilet_info.create_text(75, 140, font=temp_font, text="공원 면적(평방미터): ")
            self.toilet_info.create_text(170, 140, font=temp_font, text=toilet['area'])

            self.toilet_info.create_text(45, 160, font=temp_font, text="담당 기관: ")
            self.toilet_info.create_text(170, 160, font=temp_font, text=toilet['manage'])

    def show_types(self):
        pass

    def add_favorite(self):
        a = self.toilet_list.curselection()
        if a:
            toilet = self.toilets_in_si[a[0]]
            if toilet not in library_file.favorites:
                library_file.favorites.append(toilet)



