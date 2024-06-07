# pip install requests
# pip install googlemaps
import ConvenienceStore
from ConvenienceStore import *
from Favorites import *
from UrbanPark import *
from SportsCenter import *
from PublicToilet import *
import library_file


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
        library_file.sendMessage(self.user, "Goodbye!")

    def telebot(self):
        self.user = '7463275315'

        bot.message_loop(self.handle)
        library_file.sendMessage(self.user, "Hello World!")

    def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type != 'text':
            library_file.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
            return

        text = msg['text']
        args = text.split(' ')

        if args[0] == '편의점' and len(args) > 1:
            ConvenienceStore.tele_si(chat_id=chat_id, si=args[1])



MainGUI()
