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
            "si": None,
            "type": item.findtext("PUBLFACLT_DIV_NM"),
            "addr": item.findtext("REFINE_LOTNO_ADDR"),
            "telno": item.findtext("MANAGE_INST_TELNO"),
            "manage": item.findtext("MANAGE_INST_NM"),
            "time": item.findtext("OPEN_TM_INFO"),
            "unisex": item.findtext("MALE_FEMALE_CMNUSE_TOILET_YN"),
            "facil": [],
            "data_type": "공중화장실",
            "lat": item.findtext("REFINE_WGS84_LAT"),
            "lng": item.findtext("REFINE_WGS84_LOGT")
        }
        if item.findtext("MALE_DSPSN_WTRCLS_CNT") and item.findtext("MALE_DSPSN_UIL_CNT"):
            toilet['dspsn_male'] = True
            toilet['facil'].append("남성용 장애인 화장실")
        if item.findtext("FEMALE_DSPSN_WTRCLS_CNT"):
            toilet['dspsn_female'] = True
            toilet['facil'].append("여성용 장애인 화장실")
        if item.findtext("MALE_KID_WTRCLS_CNT") or item.findtext("FEMALE_KID_WTRCLS_CNT"):
            toilet['kid'] = True
            toilet['facil'].append("어린이용 화장실")

        toilet['nappy'] = item.findtext("PLC_NM")
        if toilet['addr']:
            if toilet['addr'].split()[0] == '경기도' or toilet['addr'].split()[0] == "경도기":
                toilet['si'] = toilet['addr'].split()[1]
            else:
                toilet['si'] = toilet['addr'].split()[0]

        toilets.append(toilet)

    def __init__(self, frame):

        self.selected_si = StringVar()
        self.selected_si.set("성남시")  # 초기값 설정
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

        # 시설 캔버스와 지도 이미지 캔버스 담을 프레임
        frame3 = Frame(frame)
        frame3.pack()

        # 공원 목록 리스트박스 생성
        self.toilet_list = Listbox(frame2, width=50)
        self.toilet_list.pack(side=LEFT)

        # 스크롤바 생성
        scrollbar = Scrollbar(frame2)
        scrollbar.pack(side=RIGHT, fill=Y)

        # 스크롤바와 화장실 목록 연결
        self.toilet_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.toilet_list.yview)

        self.si_combo.bind("<<ComboboxSelected>>", self.on_si_select)

        self.show_toilets()

        # 화장실 정보 출력 캔버스 생성
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

        # 화장실 목록에 추가
        for toilet in self.toilets_in_si:
            self.toilet_list.insert(END, f"{toilet['name']} ({toilet['type']})")

    def on_si_select(self, event):
        # 콤보박스 시군 선택 시 해당 시에 맞는 정보 업데이트 이벤트 함수
        self.show_toilets()

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
            self.toilet_info.create_text(170, 45, font=temp_font, text=toilet['addr'][:18])
            self.toilet_info.create_text(170, 60, font=temp_font, text=toilet['addr'][18:])

            self.toilet_info.create_text(52, 80, font=temp_font, text="화장실 종류: ")
            self.toilet_info.create_text(170, 80, font=temp_font, text=toilet['type'])

            self.toilet_info.create_text(45, 100, font=temp_font, text="개방 시간: ")
            self.toilet_info.create_text(170, 100, font=temp_font, text=toilet['time'])

            self.toilet_info.create_text(45, 120, font=temp_font, text="남녀 공용: ")
            self.toilet_info.create_text(170, 120, font=temp_font, text=toilet['unisex'])

            self.toilet_info.create_text(50, 140, font=temp_font, text="기저귀 교환대")
            self.toilet_info.create_text(170, 140, font=temp_font, text=toilet['nappy'])

            self.toilet_info.create_text(42, 160, font=temp_font, text="전화번호: ")
            self.toilet_info.create_text(170, 160, font=temp_font, text=toilet['telno'])

            self.toilet_info.create_text(45, 180, font=temp_font, text="관리 기관: ")
            self.toilet_info.create_text(170, 180, font=temp_font, text=toilet['manage'])

            self.show_types()

    def show_types(self):
        # 화장실 내 장애인 화장실, 기저귀 교환대, 어린이용 화장실 여부
        self.toilet_type.delete('all')

        name_font = font.Font(size=13, weight='bold', family='Consolas')
        temp_font = font.Font(size=10, weight='bold', family='Consolas')
        a = self.toilet_list.curselection()
        if a:
            toilet = self.toilets_in_si[a[0]]

            self.toilet_type.create_text(190, 40, font=name_font, text=toilet['name'] + ' 화장실 시설 현황')
            self.toilet_type.create_text(70, 80, font=temp_font, text="장애인 화장실")
            dspn_m = Label(self.toilet_type, bg='white', width=100, height=100)
            dspn_m.place(x=20, y=110)
            self.toilet_type.create_text(190, 80, font=temp_font, text="어린이용 화장실")
            kid = Label(self.toilet_type, bg='white', width=100, height=100)
            kid.place(x=140, y=110)
            self.toilet_type.create_text(300, 80, font=temp_font, text='기저귀 교환대')
            nappy = Label(self.toilet_type, bg='white', width=100, height=100)
            nappy.place(x=250, y=110)

            # 해당 시설 존재 시 해당 아이콘 이미지 출력
            if toilet['dspsn_male'] and toilet['dspsn_female']:
                my_img = PhotoImage(file='images/dspsn_male.png')
                dspn_m.configure(image=my_img)
                dspn_m.image = my_img
            else:
                dspn_m.configure()
                dspn_m.image = None

            if toilet['kid']:
                my_img = PhotoImage(file='images/kid.png')
                kid.configure(image=my_img)
                kid.image = my_img
            else:
                kid.configure()
                kid.image = None

            if toilet['nappy'] != 'N' and toilet['nappy']:
                my_img = PhotoImage(file='images/nappy.png')
                nappy.configure(image=my_img)
                nappy.image = my_img
                self.toilet_type.create_text(300, 100, text=toilet['nappy'])
            else:
                nappy.configure()
                nappy.image = None

    def add_favorite(self):
        a = self.toilet_list.curselection()
        if a:
            toilet = self.toilets_in_si[a[0]]
            if toilet not in library_file.favorites:
                library_file.favorites.append(toilet)
