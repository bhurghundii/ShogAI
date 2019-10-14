from tkinter import *
from tkinter import messagebox
import tkinter as tk
import copy
import upsidedown
from shog_logic import shog_logic
from shog_logic import AI_watcher
from threading import Timer, Thread, Event

class shog_gui():

    def __init__(self, gameState):
        self.gameState = gameState
        self.board_size = gameState.board_size
        self.gameMatrix = gameState.gameMatrix

    def drawInitialBoard(self):
        root = Tk()
        root.title('ShogAI')
        root.geometry('1009x1009')
        self.cells = {}
        self.turnIndicator = None
        self.dropBlacksPieces = []
        self.dropWhitePieces = []

        # create main containers for board, like dropped pieces, actual board etc.
        center = Frame(root, bg='white', width=900, height=900, padx=3, pady=3)
        bottom = Frame(root, bg='yellow', width=200, height=900, padx=3, pady=3)
        right = Frame(root, width=900, height=200, padx=3, pady=3)
        left = Frame(root, width=900, height=200, padx=3, pady=3)

        # layout all of the main containers
        root.grid_rowconfigure(self.board_size, weight=1)
        root.grid_columnconfigure(self.board_size, weight=1)

        center.grid(row=1, column = 1, sticky="nsew")
        bottom.grid(row=2, column=1, sticky="nsew")
        right.grid(column=2, row=1, sticky="nsew")
        left.grid(column=0, row=1, sticky="nsew")



        # create the center widgets
        center.grid_rowconfigure(0, weight=1)
        center.grid_columnconfigure(1, weight=1)

        bottom.grid_rowconfigure(0, weight=1)
        bottom.grid_columnconfigure(0, weight=1)

        right.grid_rowconfigure(0, weight=1)
        right.grid_columnconfigure(1, weight=1)

        left.grid_rowconfigure(0, weight=1)
        left.grid_columnconfigure(0, weight=1)
        #we copy the matrix to another one purely for drawing because we want this to be used again
        #since python sets variables as references to variables, and we have a 2d array, we use deepcopy
        #becasue its easier than just loopcopying

        drawMatrix = copy.deepcopy(self.gameMatrix)

        #We grab the class for logic and load it, ready for the square buttons to be used.

        for row in range(self.board_size):
            for column in range(self.board_size + 1):
                cell = Frame(center)
                cell.grid(row=row, column=column)

                if column == self.board_size:
                    T2 = Label(cell, text= (chr(row + 65), row), background='white')
                    T2.pack( anchor = E )
                try:
                    if (drawMatrix[row][column] == 0):
                        drawMatrix[row][column] = ''
                    if ('W' in drawMatrix[row][column]):
                        drawMatrix[row][column] = upsidedown.convChartoUpsideDown(drawMatrix[row][column])[:-1]
                    else:
                        drawMatrix[row][column] = (drawMatrix[row][column])[1:]

                    if row == 0:
                        T1 = Label(cell, text= (10 - (column + 1), column))
                        T1.pack( anchor = N )



                    square_board = Button(cell, text=drawMatrix[row][column], bg='white', highlightbackground="black",
                                 highlightcolor="black", highlightthickness=1, height=6, width=9, command =  lambda row=row, col=column: gameLogic.click(row, col))
                    square_board.pack()



                    self.cells[(row, column)] = square_board
                except:
                    pass

        self.options = Frame(bottom)
        self.options.grid(column=0)

        self.dropBlacks = Frame(right)
        self.dropBlacks.grid(column=0)

        self.dropWhites = Frame(left)
        self.dropWhites.grid(column=0)

        TurnIndicator = Label(self.options, text='Blacks Turn', bg='white', highlightbackground="black", highlightcolor="black", highlightthickness=1, height=3, width=9)
        TurnIndicator.pack(padx=10, side=tk.LEFT)

        self.turnIndicator = TurnIndicator

        gameLogic = shog_logic(self.gameState, self.cells, self.turnIndicator, self.dropBlacks, self.dropWhites, self.dropBlacksPieces, self.dropWhitePieces)

        if self.gameState.isAI == True:
            stopFlag = Event()
            print('Starting the AI watcher')
            thread = AI_watcher(stopFlag, self.gameState)
            thread.start()

        Load1Step = Button(self.options, text='>', bg='white', highlightbackground="black",
                     highlightcolor="black", highlightthickness=1, height=2, width=5, command = lambda : gameLogic.singleStepPlay())
        Load1Step.pack(padx=10, side=tk.LEFT)

        Load2Step = Button(self.options, text='>>', bg='white', highlightbackground="black",
                     highlightcolor="black", highlightthickness=1, height=2, width=5, command = lambda : gameLogic.fullStepPlay())
        Load2Step.pack(padx=10, side=tk.LEFT)

        root.mainloop()
