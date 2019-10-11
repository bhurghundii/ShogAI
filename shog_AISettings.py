from tkinter import *
import os
from shog_start import GameInitializer
from tkinter import filedialog
import tkinter as tk

def sel():
   selection = "You selected the option " + str(var.get())

   if (var.get() == 1):
       'Playing against the AI'
       GameInitializer().run(False, True)

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
       GameInitializer().run(True, False)

   label.config(text = selection)

try:
    root = tk.Tk()
    root.title("ShogAI: A Dissertation by Vikram Chhapwale")
    root.geometry('600x200')
    var = IntVar()

    T0 = Label(root, text="Choose your color")
    T0.pack( anchor = W )

    R1 = Radiobutton(root, text="Black", variable=var, value=1, command=sel)
    R1.pack( anchor = W )

    R2 = Radiobutton(root, text="White", variable=var, value=2, command=sel)
    R2.pack( anchor = W )

    T1 = Label(root, text="Pick the AI difficulty")
    T1.pack( anchor = W )

    R3 = Radiobutton(root, text="Easy", variable=var, value=1, command=sel)
    R3.pack( anchor = W )

    R4 = Radiobutton(root, text="Medium", variable=var, value=2, command=sel)
    R4.pack( anchor = W )

    R5 = Radiobutton(root, text="Hard", variable=var, value=3, command=sel)
    R5.pack( anchor = W )

    square_board = Button(root, text='Start the game', height=6, width=9)
    square_board.pack()

    label = Label(root)
    label.pack()
    root.mainloop()
except:
    print('Caught exception CTRL-C: Terminating ShogAI gracefully')
