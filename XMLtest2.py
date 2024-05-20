
import requests
import xml.etree.ElementTree as ET
from tkinter import *
import tkinter.ttk as ttk

def on_si_select():
    store_list.delete(0, END)

    si_name = selected_si.get()
    stores_in_si = [store for store in stores if store['addr'] and store['addr'].split()[1] == si_name]

    # 병원 목록에 추가
    for store in stores_in_si:
        store_list.insert(END, f"{store['name']}")


url = "http://openapi.gg.go.kr/Resrestrtcvnstr"
params = {
    "KEY": "874d62100e224676a4f0cd46e40b3da5",
    "Type": "xml",
    "pIndex": "1",
    "pSize": "500"
    #"SIGUN_NM": '시흥시'
    #"SIGUN_CD": ''
}

response = requests.get(url, params=params)
#print(response.text)
root = ET.fromstring(response.text)
items = root.findall(".//row")
#items = root.iter("row")

stores = []
for item in items:
    store = {
        "name": item.findtext("BIZPLC_NM"),
        "addr": item.findtext("REFINE_ROADNM_ADDR"),
        "state": item.findtext("BSN_STATE_NM")
    }
    stores.append(store)



window = Tk()
window.title("편의점 정보")

selected_si = StringVar()
selected_si.set("시흥시")  # 초기값 설정
si_options = set()
for store in stores:
    if store['addr']:
        si_options.add(store['addr'].split()[1])
si_combo = ttk.Combobox(window, textvariable=selected_si, values=list(si_options))
si_combo.pack()


# 편의점 목록 리스트박스 생성
store_list = Listbox(window, width=60)
store_list.pack()

# 스크롤바 생성
scrollbar = Scrollbar(window)
scrollbar.pack(side=RIGHT, fill=Y)

# 스크롤바와 편의점 목록 연결
store_list.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=store_list.yview)


si_combo.bind("<<ComboboxSelected>>", on_si_select)


on_si_select()

window.mainloop()

# 통계 캔버스 생성
# canvas = Canvas(window, width=300, height=300)
# canvas.pack(side=LEFT)

#
# frame = Frame(window)
# frame.pack()
#
# header = ["상호명", "주소", "운영 상태"]
#
# for i, col_name in enumerate(header):
#     label = Label(frame, text=col_name, font=("Helvetica", 14, "bold"))
#     label.grid(row=0, column=i)
#
#
# row_count = 1
# for item in root.iter("row"):
#     name = item.findtext("BIZPLC_NM")
#     addr = item.findtext("REFINE_ROADNM_ADDR")
#     state = item.findtext("BSN_STATE_NM")
#     #telno = item.findtext("TELNO")
#     if '폐업' in state:
#         continue
#
#     data = [name, addr, state]
#     for i, value in enumerate(data):
#         label = Label(frame, text=value, font=("Helvetica", 12))
#         label.grid(row=row_count, column=i)
#
#     row_count += 1



