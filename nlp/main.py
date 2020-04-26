from tkinter import *
import os
import time
from tkinter import filedialog
import urllib
def browsefunc():
    global x
    master.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    x=master.filename
    print (x)
    
def show_entry_fields():
        text_file = open("path.txt","w+")
        text_file.write(x)
        text_file.close()
        os.system("py ocr.py")
        os.system("py dspimg.py")

def nlp():
        text_file = open("path.txt","w+")
        text_file.write(e1.get())
        text_file.close()
        os.system("py ocr.py")
        os.system("py nlp.py")
        os.system("py rohit2.py")

master = Tk()
Label(master, text="            CHARACTER RECOGNIZER").grid(row=0)
Label(master, text="            -----------------------------------").grid(row=1)

e1 = Entry(master)

Button(master, text='Preview', command=show_entry_fields).grid(row=3, column=1, sticky=W, pady=4)
Button(master, text='NLP', command=nlp).grid(row=3, column=2, sticky=W, pady=4)
browsebutton = Button(master, text="Browse", command=browsefunc).grid(row=3, column=0, sticky=W, pady=4)
#browsebutton.pack()
pathlabel = Label(master)
#pathlabel.pack()

mainloop( )
