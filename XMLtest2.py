import requests
import xml.etree.ElementTree as ET
from tkinter import *
import tkinter.ttk as ttk


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
            "si": item.findtext("SIGUN_NM")
        }
        stores.append(store)


    def __init__(self):
        window = Tk()
        window.title("편의점 정보")

        self.selected_si = StringVar()
        self.selected_si.set("시흥시")  # 초기값 설정
        self.si_options = set()
        for store in self.stores:
            if store['si']:
                self.si_options.add(store['si'])
        self.si_combo = ttk.Combobox(window, textvariable=self.selected_si, values=list(self.si_options))
        self.si_combo.pack()

        frame = Frame(window)
        frame.pack()
        # 편의점 목록 리스트박스 생성
        self.store_list = Listbox(frame, width=60)
        self.store_list.pack()

        # 스크롤바 생성
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # 스크롤바와 편의점 목록 연결
        self.store_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.store_list.yview)


        self.si_combo.bind("<<ComboboxSelected>>", self.on_si_select)

        self.show_stores()

        window.mainloop()

        # 통계 캔버스 생성
        # canvas = Canvas(window, width=300, height=300)
        # canvas.pack(side=LEFT)

    def show_stores(self):
        self.store_list.delete(0, END)

        si_name = self.selected_si.get()
        stores_in_si = [store for store in self.stores if store['si'] == si_name]

        # 병원 목록에 추가
        for store in stores_in_si:
            self.store_list.insert(END, f"{store['name']}")

    def on_si_select(self,event):
        self.show_stores()





