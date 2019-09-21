from tkinter import *
import tkFont
import os
from shog_start import GameInitializer
from tkinter import filedialog

def sel():
   selection = "You selected the option " + str(var.get())
   if (var.get() == 2):
       GameInitializer().run()

   if (var.get() == 3):
       root.filename =  filedialog.askopenfilename(initialdir = "/home/ubuntu/Documents/Shogi-DISS/src/records/",title = "Select file",filetypes = (("txt files","*.txt"),("all files","*.*")))
       print (root.filename)

       f = open(root.filename, "r")
       replaygame = f.read()
       f.close()

       f = open('ext_data/load_game.txt', "w")
       f.write(replaygame)
       f.close()
       GameInitializer().run()

   label.config(text = selection)

try:
    root = Tk()
    root.title("ShogAI: A Dissertation by Vikram Chhapwale")

    var = IntVar()

    T1 = Label(root, text="Game Mode")
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
