import urllib.parse
import urllib.request
import requests
import xml.etree.ElementTree as ET
from tkinter import *

url = "http://safemap.go.kr/openApiService/data/getConvenienceStoreData.do"
params = {
    "serviceKey": "CPXKIT4A-CPXK-CPXK-CPXK-CPXKIT4A5A",
    "pageNo": "1",
    "numOfRows": "10",
    "dataType": "xml",
    "CTPRVN_CD": '110000',
    "SSG_CD": '110019'
}

response = requests.get(url, params=params)
print(response.text)
root = ET.fromstring(response.text)

window = Tk()
window.title("편의점 정보")

frame = Frame(window)
frame.pack()

header = ["상호명", "주소", "전화번호"]

for i, col_name in enumerate(header):
    label = Label(frame, text=col_name, font=("Helvetica", 14, "bold"))
    label.grid(row=0, column=1)

row_count = 1
for item in root.iter("item"):
    name = item.findtext("FCLTY_NM")
    addr = item.findtext("RN_ADRES")
    telno = item.findtext("TELNO")

    data = [name, addr, telno]
    for i, value in enumerate(data):
        label = Label(frame, text=value, font=("Helvetica", 12))
        label.grid(row=row_count, column=1)

    row_count += 1

window.mainloop()



