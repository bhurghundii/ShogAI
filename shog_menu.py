from tkinter import *
import tkFont

root = Tk()
root.title("ShogAI")
root.geometry("1009x1009")
center = Frame(root, bg='white', width=300, height=100, padx=460, pady=400)


helv36 = tkFont.Font(family="Helvetica",size=36,weight="bold")

center.grid(row=2, column =2, sticky="nsew")
cell = Frame(center)

cell.grid(row=0, column=0)
square_board = Label(cell, text='ShogAI', bg='white',font=helv36)
square_board.pack()

cell.grid(row=1, column=1)
square_board = Button(cell, text='Vs 2 Player', bg='grey', highlightbackground="black", highlightcolor="black", highlightthickness=1, height=6, width=9)
square_board.pack()

cell.grid(row=2, column=2)
square_board = Button(cell, text='Vs AI', bg='grey', highlightbackground="black", highlightcolor="black", highlightthickness=1, height=6, width=9)
square_board.pack()

# create the center widgets
center.grid_rowconfigure(0, weight=1)
center.grid_columnconfigure(1, weight=1)

root.mainloop()
