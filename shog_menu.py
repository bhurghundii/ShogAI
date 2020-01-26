from tkinter import *
import os
from shog_start import GameInitializer
from tkinter import filedialog
import tkinter as tk

def sel():
   if (var.get() == 1):
       'Playing against the AI'
       #GameInitializer().run(False, True)
       import shog_AISettings

   if (var.get() == 2):
       GameInitializer().run(False, False)

   if (var.get() == 3):
       #I don't like initialdir ... find a more universal method
       root.filename =  filedialog.askopenfilename(initialdir = "/home/ubuntu/Documents/Shogi-DISS/src/records/",title = "Select file",filetypes = (("txt files","*.txt"),("all files","*.*")))
       print ('Preparing to load from ' + root.filename)

       f = open(root.filename, "r")
       replaygame = f.read()
       f.close()

       f = open('ext_data/load_game.txt', "w")
       f.write(replaygame)
       f.close()
       GameInitializer().run(True, False, None, root.filename)

try:
    f = open('ext_data/load_game.txt', "w", encoding='utf-8')
    f.write('')
    f.close
    f = open('ext_data/movetoplay.txt', "w", encoding='utf-8')
    f.write('')
    f.close

    root = tk.Tk()
    root.title("ShogAI: A Dissertation by Vikram Chhapwale")
    root.geometry('600x500')
    var = IntVar()

    path = "assets/INTRO.png"
    image = tk.PhotoImage(file=path)
    label = tk.Label(image=image)
    label.pack()

    T0 = Label(root, text="Welcome to ShogAI, a Dissertation by Vikramaditya Chhapwale from Nottingham")
    T0.pack( anchor = W )

    T1 = Label(root, text="Pick a Game Mode")
    T1.pack( anchor = W )

    R1 = Radiobutton(root, text="VS AI", variable=var, value=1, command=sel)
    R1.pack( anchor = W )

    R2 = Radiobutton(root, text="VS Another Player", variable=var, value=2, command=sel)
    R2.pack( anchor = W )

    R3 = Radiobutton(root, text="Load a game", variable=var, value=3, command=sel)
    R3.pack( anchor = W )

    label = Label(root)
    label.pack()
    root.mainloop()
except:
    print('Caught exception CTRL-C: Terminating ShogAI gracefully')
