from tkinter import *
from subprocess import call


def Open():
    call(["python", "Snake_2\snake2.py"])
    call(["python", "YouTube-Download_3\youtube3.py"])


root = Tk()
root.title("Two in one")
root.geometry('300x300')
frame = Frame(root)
frame.pack(pady=30, padx=30)
btn = Button(frame, text='Start', width=50, height=50, command=Open)
btn.pack()

root.mainloop()
