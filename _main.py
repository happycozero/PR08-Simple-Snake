from tkinter import *
from subprocess import call

def Open():
    call(["python", "downthe1.py"])
    call(["python", "_Snake_2\snake2.py"])
    call(["python", "youtube3.py"])
    call(["python", "weather4.py"])

root=Tk()
root.geometry('300x300')
frame = Frame(root)
frame.pack(pady=30, padx=30)
btn=Button(frame, text='Full Pack', width=50, height=50, command=Open)
btn.pack()

root.mainloop()