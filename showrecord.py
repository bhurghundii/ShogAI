'''
This handles the GUI for displaying the game's record
'''
from tkinter import Tk, NORMAL, END, DISABLED, Scrollbar, Text, RIGHT, LEFT, Y, Label
import os
import tkinter as tk
import time
from threading import Thread


class showRecordGUI(Thread):
    def __init__(self, FILENAME):
        Thread.__init__(self)
        self.FILENAME = FILENAME
    # We check the file and read it
    # Then, we update it

    def readUpdatedFile(self, T):
        with open(self.FILENAME, "r") as f:
            data = f.read()
            T.config(state=NORMAL)
            T.delete('1.0', END)
            T.insert(END, data)
            T.config(state=DISABLED)
    # The file doesn't need to be updated every frame
    # Do it every 1 second

    def sleeper(self, T):
        while True:
            self.readUpdatedFile(T)
            time.sleep(1)

    def run(self):
        # Draw the gamelog
        root = tk.Tk()
        root.title("ShogAI: Game Record")
        root.geometry('200x400')
        s = Scrollbar(root)
        T = Text(root)
        s.pack(side=RIGHT, fill=Y)
        T.pack(side=LEFT, fill=Y)
        s.config(command=T.yview)
        T.config(bg='light goldenrod', pady=14, yscrollcommand=s.set)
        # Put it on the main thread so it destroys when we end the game.
        t = Thread(target=self.sleeper, args=(T,))
        t.setDaemon(True)
        t.start()

        label = Label(root)
        label.pack()
        root.mainloop()
