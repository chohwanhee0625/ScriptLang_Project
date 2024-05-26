from tkinter import *

window = Tk()
window.geometry("800x600")

image=PhotoImage(file="images/dspsn_female.png")

label=Label(window, image=image)
label.place(x=400, y=300)

window.mainloop()
