# 네이버 검색 API 예제 - 블로그 검색
import os
import sys
import urllib.request
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
    print(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)