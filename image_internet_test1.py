# 네이버 검색 API 예제
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from tkinter import *
from PIL import Image, ImageTk
import io

client_id = "xFNxfdv0x0hZx61b5kW_"
client_secret = "62ROLhKEWc"
encText = urllib.parse.quote("시흥 +소망공원 -야구")
url = "https://openapi.naver.com/v1/search/image.xml?query=" + encText
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret", client_secret)

response = urllib.request.urlopen(request)
rescode = response.getcode()

if(rescode==200):
    response_body = response.read()
    # XML 파싱
    root = ET.fromstring(response_body)
    items = root.findall('./channel/item')
    # 첫 번째 이미지 URL 가져오기
    if items:
        image_url = items[0].find('thumbnail').text
    else:
        image_url = None
else:
    print("Error Code:" + rescode)
    image_url = None

LABEL_WIDTH = 380
LABEL_HEIGHT = 250

window = Tk()

if image_url:
    # 이미지 URL로부터 이미지 로드
    image_byt = urllib.request.urlopen(image_url).read()
    image_bf = io.BytesIO(image_byt)
    image = Image.open(image_bf)

    # 이미지 크기를 라벨 크기에 맞게 조정
    image = image.resize((LABEL_WIDTH, LABEL_HEIGHT), Image.LANCZOS)
    image = ImageTk.PhotoImage(image)

    # Tkinter Label에 이미지 추가
    label = Label(window, image=image, width=LABEL_WIDTH, height=LABEL_HEIGHT)
    label.image = image  # 이미지가 garbage collected 되는 것을 방지하기 위해 참조를 유지
    label.pack()

window.mainloop()

