from tkinter import *
import os
from shog_start import GameInitializer
from tkinter import filedialog
import tkinter as tk

def sel():
  if (var.get() == 1):
      print('Going black')
      GameInitializer().run(False, True, 'Black')

  if (var.get() == 2):
      print('Going white')
      GameInitializer().run(False, True, 'White')

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

    label = Label(root)
    label.pack()
    root.mainloop()
except exception as e:
    print(e)
    print('Caught exception CTRL-C: Terminating ShogAI gracefully')
