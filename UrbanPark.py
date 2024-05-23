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
            "facil": []
        }
        park['facil'].append(item.findtext("PARK_SPORTS_FACLT_DTLS"))
        park['facil'].append(item.findtext("PARK_AMSMT_FACLT_DTLS"))
        park['facil'].append(item.findtext("PARK_CNVNC_FACLT_DTLS"))
        park['facil'].append(item.findtext("PARK_CLTR_FACLT_DTLS"))
        park['facil'].append(item.findtext("PARK_ETC_FACLT_DTLS	"))

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
        Button(frame, width=2).pack()

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

        # 편의점 목록 리스트박스 생성
        self.park_list = Listbox(frame2, width=50)
        self.park_list.pack(side=LEFT)

        # 스크롤바 생성
        scrollbar = Scrollbar(frame2)
        scrollbar.pack(side=RIGHT, fill=Y)

        # 스크롤바와 편의점 목록 연결
        self.park_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.park_list.yview)

        self.si_combo.bind("<<ComboboxSelected>>", self.on_si_select)

        self.show_parks()

        # 편의점 정보 출력 캔버스 생성
        self.park_info = Canvas(frame1, width=300, height=200, bg='white')
        self.park_info.pack(side=RIGHT)
        Button(frame, width=5, command=self.show_info).pack()

        # 통계 캔버스 생성, 막대 그래프 그리기
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

        # 편의점 목록에 추가
        for park in self.parks_in_si:
            self.park_list.insert(END, f"{park['name']} ({park['type']})")

    def on_si_select(self, event):
        self.show_parks()
        self.show_types()

    def show_info(self):
        self.park_info.delete('all')

        name_font = font.Font(size=13, weight='bold', family='Consolas')
        temp_font = font.Font(size=10, family='Consolas')
        a = self.park_list.curselection()
        park = {}
        if a:
            park = self.parks_in_si[a[0]]

            print(park['facil'])

            self.park_info.create_text(150, 15, font=name_font, text=park['name'])

            self.park_info.create_text(30, 45, font=temp_font, text="주소: ")
            self.park_info.create_text(170, 45, font=temp_font, text=park['addr'][:13])
            self.park_info.create_text(170, 60, font=temp_font, text=park['addr'][13:])

            self.park_info.create_text(52, 90, font=temp_font, text="공원 종류: ")
            self.park_info.create_text(170, 90, font=temp_font, text=park['type'])

            self.park_info.create_text(42, 150, font=temp_font, text="전화번호: ")
            self.park_info.create_text(170, 150, font=temp_font, text=park['telno'])

    def show_types(self):
        pass



