'''
This lets the user decide what color they want to choose
when they play the AI
'''

from tkinter import IntVar, Radiobutton, Label, W
import tkinter as tk
from gameinitializer import GameInitializer

#What to do if the user sets themselves as black
#Basically, just sets one of the parameters as Black
def blackSelect():
    print('Going black')
    GameInitializer().run(False, True, 'Black')



#What to do if the user sets themselves as white
#Basically, just sets one of the parameters as White
def WhiteSelect():
    print('Going white')
    GameInitializer().run(False, True, 'White')


# Draw Graphical User Interface screen for selecting the player
# color when you choose to fight the AI
root = tk.Tk()
root.title("ShogAI: A Dissertation by Vikram Chhapwale")
root.geometry('600x200')
colorSelection = IntVar()

T0 = Label(root, text="Choose your color")
T0.pack(anchor=W)

R1 = Radiobutton(
    root,
    text="Black",
    variable=colorSelection,
    value=1,
    command=blackSelect)
R1.pack(anchor=W)

R2 = Radiobutton(
    root,
    text="White",
    variable=colorSelection,
    value=2,
    command=WhiteSelect)
R2.pack(anchor=W)

label = Label(root)
label.pack()
root.mainloop()
