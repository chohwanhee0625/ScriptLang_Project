import urllib.parse
import urllib.request
import requests
import xml.etree.ElementTree as ET
from tkinter import *

import urllib.parse
import urllib.request
import requests
import xml.etree.ElementTree as ET
from tkinter import *

url = "http://openapi.gg.go.kr/Resrestrtcvnstr"
params = {
    "KEY": "874d62100e224676a4f0cd46e40b3da5",
    "Type": "xml",
    "pIndex": "1",
    "pSize": "100"
    #"SIGUN_NM": '',
    #"SIGUN_CD": ''
}

response = requests.get(url, params=params)
print(response.text)
root = ET.fromstring(response.text)

window = Tk()
window.title("편의점 정보")

frame = Frame(window)
frame.pack()

header = ["상호명", "주소"]

for i, col_name in enumerate(header):
    label = Label(frame, text=col_name, font=("Helvetica", 14, "bold"))
    label.grid(row=0, column=i)

row_count = 1
for item in root.iter("row"):
    name = item.findtext("BIZPLC_NM")
    addr = item.findtext("REFINE_ROADNM_ADDR")
    #telno = item.findtext("TELNO")

    data = [name, addr]
    for i, value in enumerate(data):
        label = Label(frame, text=value, font=("Helvetica", 12))
        label.grid(row=row_count, column=i)

    row_count += 1

window.mainloop()



