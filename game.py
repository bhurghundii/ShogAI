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
posToMove = None
possibleMoveMatrix = []
blackcaptured = []
whitecaptured = []
gameMatrix = None
#class turnStateManager():



class GameManager():

    def init(self):
        print('Doing warm up functions like checking settings and params')

    def resetBoardGraphics(self):
        for i in range(0, 9):
            for j in range(0, 9):
                self.cells[(i, j)].configure(background='white')

    def moveLegalGO(self, pos, oldMatrixPosXlocal, oldMatrixPosYlocal, newMatrixPosXlocal, newMatrixPosYlocal):
        global possibleMoveMatrix
        print possibleMoveMatrix
        global GAMESTATE, newMatrixPosX, newMatrixPosY, oldMatrixPosX, oldMatrixPosY, posToMove, gameMatrix, BLACKTURN
        print 'Checking if ' + pos + ' originally on square (' + str(oldMatrixPosXlocal) + ',' + str(oldMatrixPosYlocal) + ') can move to square (' + str(newMatrixPosXlocal) + ',' + str(newMatrixPosYlocal) + ')'
        if ((newMatrixPosXlocal,newMatrixPosYlocal)) in possibleMoveMatrix:
            if (gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal] != 0):
                print 'Captured: ' + gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal]

            gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal] = pos
            gameMatrix[oldMatrixPosXlocal][oldMatrixPosYlocal] = 0
            self.cells[(oldMatrixPosXlocal, oldMatrixPosYlocal)].configure(text='')

            if (BLACKTURN == True):
                self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(text=pos[-1:])
            else:
                self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(text=upsidedown.convChartoUpsideDown(pos[-1:]))

            self.resetBoardGraphics()


            newMatrixPosX = None
            newMatrixPosY = None
            oldMatrixPosX = None
            oldMatrixPosY = None
            posToMove = None
            GAMESTATE = 0

            if (BLACKTURN == True):
                self.optionButtons.configure(text='White Turn')
                BLACKTURN = False
            else:
                self.optionButtons.configure(text='Black Turn')
                BLACKTURN = True



        else:
            print 'That move is NOT legal!'

            self.resetBoardGraphics()

            newMatrixPosX = None
            newMatrixPosY = None
            oldMatrixPosX = None
            oldMatrixPosY = None
            posToMove = None
            GAMESTATE = 0

        possibleMoveMatrix *= 0


    def getPossibleMoves(self, oldMatrixPosX, oldMatrixPosY, pos):
        global BLACKTURN

        if (BLACKTURN == True and pos[:-1] == 'B') or (BLACKTURN == False and pos[:-1] == 'W'):
            with open('movesets.txt') as f:
                content = f.readlines()
                for index in range(len(content)):
                    if pos[-1:] in content[index]:
                        movesets = content[index].split('=')[1]
                        #cast movesets to array
                        possiblemovelayouts =  eval(movesets)
                        for j in range(len(possiblemovelayouts)):
                            x_dif = int((possiblemovelayouts[j])[0])
                            y_dif = int((possiblemovelayouts[j])[1])

                            if pos[:-1] == 'B':
                                x_dif = -1 * x_dif
                                y_dif = -1 * y_dif
                            if pos[:-1] == 'W':
                                x_dif = 1 * x_dif
                                y_dif = 1 * y_dif


                            try:
                                if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] == 'B') and BLACKTURN == True):
                                    break

                                if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] == 'W') and BLACKTURN == False):
                                    break

                                if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] != 'B') and BLACKTURN == True):
                                    self.cells[(oldMatrixPosX + x_dif, oldMatrixPosY + y_dif)].configure(background='orange')
                                    possibleMoveMatrix.append((oldMatrixPosX + x_dif, oldMatrixPosY + y_dif))

                                if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] != 'W') and BLACKTURN == False):
                                    self.cells[(oldMatrixPosX + x_dif, oldMatrixPosY + y_dif)].configure(background='orange')
                                    possibleMoveMatrix.append((oldMatrixPosX + x_dif, oldMatrixPosY + y_dif))

                                if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] == 'W') and BLACKTURN == True):
                                    break

                                if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] == 'B') and BLACKTURN == False):
                                    break

                            except Exception as e:
                                print (e)
                                print('Move not on board so ignoring')
            return 1
        else:
            print 'It is not your turn yet'
            return 0



    def click(self, row, col):
        global GAMESTATE, newMatrixPosX, newMatrixPosY, oldMatrixPosX, oldMatrixPosY, posToMove, gameMatrix
        pos = gameMatrix[row][col]


        if GAMESTATE == 1:
            self.cells[(row, col)].configure(background='blue')
            newMatrixPosX = row
            newMatrixPosY = col
            GAMESTATE = 2

        if GAMESTATE == 0:
            if pos != 0:
                self.cells[(row, col)].configure(background='yellow')
                oldMatrixPosX = row
                oldMatrixPosY = col
                posToMove = pos
                GAMESTATE = self.getPossibleMoves(oldMatrixPosX, oldMatrixPosY, pos)


        if newMatrixPosX != None and newMatrixPosY != None and posToMove != None:
            #checkRules = ruleChecker()
            #checkRules.
            self.resetBoardGraphics()
            self.moveLegalGO(posToMove, oldMatrixPosX, oldMatrixPosY,  newMatrixPosX, newMatrixPosY)




    def run(self):
        self.initStandardGame()

    def getPieceFrmPos(self, h, w):
        global gameMatrix

        return gameMatrix[(h-1)][(w-1)]

    #TODO: Change this to something other than Tkinter. 3d graphics would be cool
    def DrawBoard(self, Matrix):
        root = Tk()
        root.title('ShogAI')
        root.geometry('909x1009')
        self.cells = {}
        self.optionButtons = None

        # create main container
        center = Frame(root, bg='white', width=900, height=900, padx=3, pady=3)
        bottom = Frame(root, bg='yellow', width=900, height=200, padx=3, pady=3)

        # layout all of the main containers
        root.grid_rowconfigure(9, weight=1)
        root.grid_columnconfigure(9, weight=1)
        center.grid(row=1, sticky="nsew")
        bottom.grid(row=2, sticky="nsew")


        # create the center widgets
        center.grid_rowconfigure(0, weight=1)
        center.grid_columnconfigure(1, weight=1)

        bottom.grid_rowconfigure(0, weight=1)
        bottom.grid_columnconfigure(1, weight=1)
        #we copy the matrix to another one purely for drawing because we want this to be used again
        #since python sets variables as references to variables, and we have a 2d array, we use deepcopy
        #becasue its easier than just loopcopying

        drawMatrix = copy.deepcopy(gameMatrix)
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
                             highlightcolor="black", highlightthickness=1, height=6, width=9, command =  lambda row=row, col=column: self.click(row, col))
                square_board.pack()
                self.cells[(row, column)] = square_board


        options = Frame(bottom)
        options.grid(row=row, column=column)

        DropAPiece = Button(options, text='Drop a piece', bg='white', highlightbackground="black",
                     highlightcolor="black", highlightthickness=1, height=3, width=9)

        TurnIndicator = Label(options, text='Blacks Turn', bg='white', highlightbackground="black",
                     highlightcolor="black", highlightthickness=1, height=3, width=9)

        TurnIndicator.pack()
        DropAPiece.pack()
        self.optionButtons = TurnIndicator
        root.mainloop()

    def initStandardGame(self):
        map_size = 9
        #h is in numbers, w is in alphabets
        w, h = map_size, map_size
        #Load from standardlayout and place here
        global gameMatrix
        gameMatrix = [[0 for  x in range(w)] for y in range(h)]
        with open('standardlayout.txt') as f:
            content = f.readlines()
            if (content[0].split(' ')[0] == '[BLACK]'):
                print ('Setting black')
                for i in range(1, len(content[0].split(' '))):
                    x = list(content[0].split(' ')[i])
                    gameMatrix[int(x[1]) -1][int(x[2]) - 1] = 'B' + x[0].lower()

            if (content[1].split(' ')[0] == '[WHITE]'):
                print ('Setting white')
                for i in range(1, len(content[1].split(' '))):
                    x = list(content[1].split(' ')[i])
                    gameMatrix[int(x[1]) - 1][int(x[2]) - 1] = 'W' + x[0].lower()

            #Even though we use a 0 - 8 array, games are recorded using 1 - 9
            #Rather than overloading, we just subtract 1 from user input
            self.DrawBoard(gameMatrix)


if __name__ == '__main__':
    gameInstanceBegins = GameManager()
    gameInstanceBegins.run()
