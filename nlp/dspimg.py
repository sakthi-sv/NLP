try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True
    
from PIL import ImageTk, Image
import os

#This creates the main window of an application
window = tk.Tk()
window.title("Preview")
window.geometry("900x900")
window.configure(background='grey')

text_file = open("path.txt","r")
x=text_file.read()
text_file.close()
path = x

#Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
img = ImageTk.PhotoImage(Image.open(path))

#The Label widget is a standard Tkinter widget used to display a text or image on the screen.
panel = tk.Label(window, image = img)

#The Pack geometry manager packs widgets in rows or columns.
panel.pack(side = "bottom", fill = "both", expand = "yes")

#Start the GUI
window.mainloop()

os.system("py rohit.py")
