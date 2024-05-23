from library_file import *


class ConvenienceStore:
    url = "http://openapi.gg.go.kr/Resrestrtcvnstr"
    params = {
        "KEY": "874d62100e224676a4f0cd46e40b3da5",
        "Type": "xml",
        "pIndex": "1",
        "pSize": "1000"
    }

    response = requests.get(url, params=params)
    root = ET.fromstring(response.text)
    items = root.findall(".//row")
    #items = root.iter("row")

    stores = []
    for item in items:
        store = {
            "name": item.findtext("BIZPLC_NM"),
            "addr": item.findtext("REFINE_ROADNM_ADDR"),
            "state": item.findtext("BSN_STATE_NM"),
            "si": item.findtext("SIGUN_NM"),
            "type": "기타",
            "telno": "031-000-0000"
        }

        if 'GS' in store['name'] or '지에스' in store['name']:
            store['type'] = 'GS25'
        elif 'CU' in store['name'] or '씨유' in store['name']:
            store['type'] = 'CU'
        elif '7eleven' in store['name'] or '7ELEVEN' in store['name'] or '세븐일레븐' in store['name']:
            store['type'] = '세븐일레븐'
        elif 'mini' in store['name'] or 'MINI' in store['name'] or '미니스톱' in store['name']:
            store['type'] = '미니스톱'
        elif '이마트' in store['name'] or 'e' in store['name']:
            store['type'] = '이마트24'
        else:
            store['type'] = '기타'

        stores.append(store)


    def __init__(self, frame):

        self.selected_si = StringVar()
        self.selected_si.set("시흥시")  # 초기값 설정
        self.si_options = set()
        for store in self.stores:
            if store['si']:
                self.si_options.add(store['si'])
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
        self.store_list = Listbox(frame2, width=50)
        self.store_list.pack(side=LEFT)

        # 스크롤바 생성
        scrollbar = Scrollbar(frame2)
        scrollbar.pack(side=RIGHT, fill=Y)

        # 스크롤바와 편의점 목록 연결
        self.store_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.store_list.yview)

        self.si_combo.bind("<<ComboboxSelected>>", self.on_si_select)

        self.show_stores()

        # 편의점 정보 출력 캔버스 생성
        self.con_info = Canvas(frame1, width=300, height=200, bg='white')
        self.con_info.pack(side=RIGHT)
        Button(frame, width=5, command=self.show_info).pack()

        # 통계 캔버스 생성, 막대 그래프 그리기
        self.con_type = Canvas(frame3, width=380, height=250, bg='white')
        self.con_type.pack(side=LEFT)
        self.show_types()

        # 지도 이미지 캔버스 생성
        map_img = Canvas(frame3, width=300, height=250, bg='white')
        map_img.pack()



    def show_stores(self):
        self.store_list.delete(0, END)

        si_name = self.selected_si.get()
        self.stores_in_si = [store for store in self.stores if store['si'] == si_name]

        # 편의점 목록에 추가
        for store in self.stores_in_si:
            self.store_list.insert(END, f"{store['name']} ({store['type']})")

    def on_si_select(self, event):
        self.show_stores()
        self.show_types()

    def show_info(self):
        self.con_info.delete('all')

        name_font = font.Font(size=13, weight='bold', family='Consolas')
        temp_font = font.Font(size=10, family='Consolas')
        a = self.store_list.curselection()
        store = {}
        if a:
            store = self.stores_in_si[a[0]]

            self.con_info.create_text(150, 15, font=name_font, text=store['name'])

            self.con_info.create_text(30, 45, font=temp_font, text="주소: ")
            self.con_info.create_text(170, 45, font=temp_font, text=store['addr'][:18])
            self.con_info.create_text(170, 60, font=temp_font, text=store['addr'][18:])

            self.con_info.create_text(52, 90, font=temp_font, text="편의점 종류: ")
            self.con_info.create_text(170, 90, font=temp_font, text=store['type'])

            self.con_info.create_text(45, 120, font=temp_font, text="운영 상태: ")
            self.con_info.create_text(170, 120, font=temp_font, text=store['state'])

            self.con_info.create_text(42, 150, font=temp_font, text="전화번호: ")
            self.con_info.create_text(170, 150, font=temp_font, text=store['telno'])

    def show_types(self):
        # 기타 포함 6종류의 막대그래프 그림
        # 캔버스 크기: 380x250
        self.con_type.delete('all')

        types = {
            "GS25": 0,
            "CU": 0,
            "세븐일레븐": 0,
            "미니스톱": 0,
            "이마트24": 0,
            "기타": 0
        }

        for store in self.stores_in_si:
            types[store['type']] += 1

        max_value = max(types.values()) + 1
        width = int(self.con_type['width'])
        height = int(self.con_type['height'])
        barwidth = (width - 60) / 6
        for i, (name, count) in enumerate(types.items()):
            x1 = i * (barwidth + 10) + 5
            x2 = x1 + barwidth
            y2 = height - 20
            y1 = y2 - y2 * count / max_value
            self.con_type.create_rectangle(x1, y1, x2, y2, fill='light blue')
            self.con_type.create_text((x1+x2)/2, height - 10, text=name)
            self.con_type.create_text((x1+x2)/2, y1-10, text=count)





