from tkinter import *
import tkinter.ttk

class MainGUI:
    def __init__(self):
        window = Tk()
        window.title('우리동네 공공시설')
        notebook = tkinter.ttk.Notebook(window, width=800, height=600)
        notebook.pack()

        self.frame1 = Frame(window)
        notebook.add(self.frame1, text='편의점')
        #Label(frame1, text='page1 내용', fg='red', font='helvetica 48').pack()

        self.frame2 = Frame(window)
        notebook.add(self.frame2, text='공원')
        #Label(frame2, text='page2 내용', fg='blue', font='helvetica 48').pack()

        self.frame3 = Frame(window)
        notebook.add(self.frame3, text='체육시설')
        #Label(frame3, text='page3 내용', fg='green', font='helvetica 48').pack()

        self.frame4 = Frame(window)
        notebook.add(self.frame4, text='공중화장실')
        #Label(frame4, text='page4 내용', fg='yellow', font='helvetica 48').pack()

        self.frame5 = Frame(window)
        notebook.add(self.frame5, text='즐겨찾기')
        #Label(frame5, text='page5 내용', fg='black', font='helvetica 48').pack()

        window.mainloop()



MainGUI()
