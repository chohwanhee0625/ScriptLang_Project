# pip install requests
# pip install googlemaps
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
        library_file.sendMessage(self.user, "필요한 정보를 입력하세요\n편의점, 공원, 체육시설, 공중화장실 또는 즐겨찾기 + 시/군 또는 조회")

    def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type != 'text':
            library_file.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
            return

        text = msg['text']
        args = text.split(' ')

        if any(type in args[0] for type in ['편의점', '공원', '체육시설', '공중화장실']) and len(args) > 1:
            self.tele_facil(chat_id, facil_type=args[0], si=args[1])
        elif args[0] in '즐겨찾기':
            if args[1] == '조회' or args[1] == '저장':
                self.tele_fav(chat_id, args[1])
        else:
            library_file.sendMessage(chat_id, '잘못된 입력입니다.\n다시 입력해주세요')

        library_file.sendMessage(chat_id, "필요한 정보를 입력하세요\n편의점, 공원, 체육시설, 공중화장실 또는 즐겨찾기\n + 시/군 또는 조회")

    @staticmethod
    def tele_facil(chat_id, facil_type, si):
        if facil_type in '편의점':
            facil_list = ConvenienceStore.stores
        elif facil_type in '공원':
            facil_list = UrbanPark.parks
        elif facil_type in '체육시설':
            facil_list = SportsCenter.sports
        elif facil_type in '공중화장실':
            facil_list = PublicToilet.toilets
        else:
            sendMessage(chat_id, "잘못된 입력입니다. 다시 입력해주세요.")
            return

        allow_list = ['name', 'si', 'telno', 'state', 'type', 'manage', 'time', 'facil', 'area', 'unisex']
        for facil in facil_list:
            if si in facil['si']:
                msg = ""
                for k, v in facil.items():
                    if any(k == key for key in allow_list):
                        msg += k + ": " + str(v) + "\n"
                sendMessage(chat_id, msg)

    @staticmethod
    def tele_fav(chat_id, mode):
        allow_list = ['name', 'si', 'telno', 'state', 'type', 'manage', 'time', 'facil', 'area', 'unisex']
        if mode == '조회':
            if not favorites:
                msg = '즐겨찾기 목록이 비어있습니다.'
                sendMessage(chat_id, msg)
                return

            for favorite in favorites:
                msg = ""
                for k, v in favorite.items():
                    if any(k == key for key in allow_list):
                        msg += k + ": " + str(v) + "\n"
                sendMessage(chat_id, msg)
        else:
            msg = '잘못된 입력입니다.\n다시 입력해주세요.'
            sendMessage(chat_id, msg)


MainGUI()
