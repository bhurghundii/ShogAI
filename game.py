# -*- coding: UTF-8 -*-
import upsidedown
from tkinter import *
import copy

#-------------------------------
#Global constants
BLACKTURN = True
GAMESTATE = 0
newMatrixPosX = None
newMatrixPosY = None
oldMatrixPosX = None
oldMatrixPosY = None

class ruleChecker():
    def moveLegalGO():
        Matrix[0][0] = 'BW';

class startGame():

    def init(self):
        print('Doing warm up functions like checking settings and params')

    def moveLegalGO(self, pos, oldMatrixPosX, oldMatrixPosY, newMatrixPosX, newMatrixPosY, Matrix):
        print('Value is' + Matrix)
        Matrix[0][0] = 'BW'
        self.cells[(0, 0)].configure(text='BW')
        #self.DrawBoard(Matrix)


    def click(self, pos, row, col, Matrix):
        global GAMESTATE, newMatrixPosX, newMatrixPosY, oldMatrixPosX, oldMatrixPosY
        print Matrix
        if GAMESTATE == 1:
            self.cells[(row, col)].configure(background='blue')
            newMatrixPosX = row
            newMatrixPosY = col
            GAMESTATE = 2
        if GAMESTATE == 0:
            self.cells[(row, col)].configure(background='yellow')
            oldMatrixPosX = row
            oldMatrixPosY = col
            #self.cells[(row, col)].configure(text='TEST')
            GAMESTATE = 1

        if newMatrixPosX != None and newMatrixPosY != None:
            self.moveLegalGO(Matrix, pos, oldMatrixPosX, oldMatrixPosY,  newMatrixPosX, newMatrixPosY)

        print("you clicked row %s column %s with %s" % (row, col, pos))



    def run(self):
        self.initStandardGame()

    def getPieceFrmPos(self, Matrix, h, w):
        return Matrix[(h-1)][(w-1)]

    def DrawBoard(self, Matrix):
        #print Matrix
        root = Tk()
        root.title('ShogAI')
        root.geometry('909x909')
        self.cells = {}

        # create main container
        center = Frame(root, bg='white', width=900, height=900, padx=3, pady=3)

        # layout all of the main containers
        root.grid_rowconfigure(9, weight=1)
        root.grid_columnconfigure(9, weight=1)
        center.grid(row=1, sticky="nsew")

        # create the center widgets
        center.grid_rowconfigure(0, weight=1)
        center.grid_columnconfigure(1, weight=1)

        #we copy the matrix to another one purely for drawing because we want this to be used again
        #since python sets variables as references to variables, and we have a 2d array, we use deepcopy
        #becasue its easier than just loopcopying

        drawMatrix = copy.deepcopy(Matrix)
        for row in range(9):
            for column in range(9):
                cell = Frame(center)
                cell.grid(row=row, column=column)

                if (drawMatrix[row][column] == 0):
                    drawMatrix[row][column] = ''
                if ('W' in drawMatrix[row][column]):
                    drawMatrix[row][column] = upsidedown.convChartoUpsideDown(drawMatrix[row][column])[:-1]
                else:
                    drawMatrix[row][column] = (drawMatrix[row][column])[1:]
                square_board = Button(cell, text=drawMatrix[row][column], bg='white', highlightbackground="black",
                             highlightcolor="black", highlightthickness=1, height=6, width=9, command =  lambda pos=Matrix[row][column], row=row, col=column, Matr=Matrix: self.click(pos, row, col, Matr))
                square_board.pack()
                self.cells[(row, column)] = square_board


        root.mainloop()

    def initStandardGame(self):
        map_size = 9
        #h is in numbers, w is in alphabets
        w, h = map_size, map_size
        Matrix = [[0 for  x in range(w)] for y in range(h)]
        #Load from standardlayout and place here

        with open('standardlayout.txt') as f:
            content = f.readlines()
            if (content[0].split(' ')[0] == '[BLACK]'):
                print ('Setting black')
                for i in range(1, len(content[0].split(' '))):
                    x = list(content[0].split(' ')[i])
                    Matrix[int(x[1]) -1][int(x[2]) - 1] = 'B' + x[0].lower()

            if (content[1].split(' ')[0] == '[WHITE]'):
                print ('Setting white')
                for i in range(1, len(content[1].split(' '))):
                    x = list(content[1].split(' ')[i])
                    Matrix[int(x[1]) - 1][int(x[2]) - 1] = 'W' + x[0].lower()

            #Even though we use a 0 - 8 array, games are recorded using 1 - 9
            #Rather than overloading, we just subtract 1 from user input
            self.DrawBoard(Matrix)
            print (self.getPieceFrmPos(Matrix, 1, 1))



if __name__ == '__main__':
    gameInstanceBegins = startGame()
    gameInstanceBegins.run()
