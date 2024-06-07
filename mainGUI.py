# pip install requests
# pip install googlemaps
import telepot
import traceback
import sys

from ConvenienceStore import *
from Favorites import *
from UrbanPark import *
from SportsCenter import *
from PublicToilet import *


class MainGUI:
    def __init__(self):
        window = Tk()
        window.title('우리동네 공공시설')
        notebook = ttk.Notebook(window, width=800, height=600)
        notebook.pack()

        self.frame1 = Frame(window)
        notebook.add(self.frame1, text='편의점')
        ConvenienceStore(self.frame1)

        self.frame2 = Frame(window)
        notebook.add(self.frame2, text='도시공원')
        UrbanPark(self.frame2)

        self.frame3 = Frame(window)
        notebook.add(self.frame3, text='체육시설')
        SportsCenter(self.frame3)

        self.frame4 = Frame(window)
        notebook.add(self.frame4, text='공중화장실')
        PublicToilet(self.frame4)

        self.frame5 = Frame(window)
        notebook.add(self.frame5, text='즐겨찾기')
        Favorites(self.frame5)

        self.telebot()

        window.mainloop()
        self.sendMessage(self.user, "봇 종료")

    def telebot(self):
        key = 'sea100UMmw23Xycs33F1EQnumONR%2F9ElxBLzkilU9Yr1oT4TrCot8Y2p0jyuJP72x9rG9D8CN5yuEs6AS2sAiw%3D%3D'
        TOKEN = '7279986887:AAFoPg_7tTNxYZgu9VkNkDp9kGpGDJCJIgY'
        MAX_MSG_LENGTH = 300
        self.bot = telepot.Bot(TOKEN)
        self.user = '7463275315'

        self.bot.message_loop(self.handle)
        self.sendMessage(self.user, "시작 메시지")
        print('Listening...')

    def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type != 'text':
            self.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
            return

        text = msg['text']
        args = text.split(' ')
        self.sendMessage(chat_id, "메시지 테스트")

    def sendMessage(self, user, msg):
        try:
            self.bot.sendMessage(user, msg)
        except:
            traceback.print_exc(file=sys.stdout)


MainGUI()
