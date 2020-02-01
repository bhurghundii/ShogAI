from tkinter import *
import os
from gameinitializer import GameInitializer
from tkinter import filedialog
import tkinter as tk

def BlackSelect():
  print('Going black')
  GameInitializer().run(False, True, 'Black')

def WhiteSelect():
  print('Going white')
  GameInitializer().run(False, True, 'White')

try:
    root = tk.Tk()
    root.title("ShogAI: A Dissertation by Vikram Chhapwale")
    root.geometry('600x200')
    colorSelection = IntVar()

    T0 = Label(root, text="Choose your color")
    T0.pack( anchor = W )

    R1 = Radiobutton(root, text="Black", variable=colorSelection, value=1, command=BlackSelect)
    R1.pack( anchor = W )

    R2 = Radiobutton(root, text="White", variable=colorSelection, value=2, command=WhiteSelect)
    R2.pack( anchor = W )

    label = Label(root)
    label.pack()
    root.mainloop()
except Exception as e:
    print(e)
    print('Caught exception CTRL-C: Terminating ShogAI gracefully')
