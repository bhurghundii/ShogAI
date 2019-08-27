# -*- coding: UTF-8 -*-
import upsidedown
from tkinter import *
from tkinter import messagebox
import copy

#-------------------------------
#Global constants
BLACKTURN = True
GAMESTATE = 0
isCheck = False
newMatrixPosX = None
newMatrixPosY = None
oldMatrixPosX = None
oldMatrixPosY = None
posToMove = None
possibleMoveMatrix = []
blackcaptured = []
whitecaptured = []
gameMatrix = None
isMoveDropPiece = False

with open('configure.txt') as f:
    size_board = int(f.read())

class GameManager():

    def init(self):
        print('Doing warm up functions like checking settings and params')

    def resetBoardGraphics(self):
        for i in range(0, size_board):
            for j in range(0, size_board):
                self.cells[(i, j)].configure(background='white')

    def dropPiece(self, pos):
        print (pos)
        if pos == 'p':
            pass

    def clickDrop(self, row):
        global isMoveDropPiece, GAMESTATE
        self.dropPiece(blackcaptured[row - 1])
        isMoveDropPiece = True
        GAMESTATE = 3


    def isKingUnderCheck(self, oldMatrixPosX, oldMatrixPosY, pos):
        global BLACKTURN, GAMESTATE, isCheck

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
                                if oldMatrixPosX + x_dif >= 0 and oldMatrixPosY + y_dif >= 0:
                                    if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] == 'B') and BLACKTURN == True):
                                        break

                                    if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] == 'W') and BLACKTURN == False):
                                        break

                                    if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] != 'B') and BLACKTURN == True):
                                        if str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1)) == 'Wk':
                                            print 'BLACK CHECK!'
                                            isCheck = True

                                        self.cells[(oldMatrixPosX + x_dif, oldMatrixPosY + y_dif)].configure(background='cyan')



                                    if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] != 'W') and BLACKTURN == False):
                                        if str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1)) == 'Bk':
                                            print(oldMatrixPosX + x_dif , oldMatrixPosY + y_dif, pos )
                                            print 'WHITE CHECK!'
                                            isCheck = True

                                        self.cells[(oldMatrixPosX + x_dif, oldMatrixPosY + y_dif)].configure(background='cyan')

                                    if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] == 'W') and BLACKTURN == True):
                                        break

                                    if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] == 'B') and BLACKTURN == False):
                                        break

                            except Exception as e:
                                pass
            return 1
        else:
            return 0

    def promotion(self, pos):
        if 'g' not in pos and 'k' not in pos and pos[-1:].islower() == True:
            MsgBox = messagebox.askquestion("Promotion!", "You have reached promotion. Would you like to promote your piece?")
            if MsgBox == 'yes':
                return pos.upper()
            else:
                return pos
        return pos

    def moveLegalGO(self, pos, oldMatrixPosXlocal, oldMatrixPosYlocal, newMatrixPosXlocal, newMatrixPosYlocal):
        global possibleMoveMatrix, isCheck
        global GAMESTATE, newMatrixPosX, newMatrixPosY, oldMatrixPosX, oldMatrixPosY, posToMove, gameMatrix, BLACKTURN
        if ((newMatrixPosXlocal,newMatrixPosYlocal)) in possibleMoveMatrix:



            #Get current pre-move position we are moving to
            old_state_pos = self.getPieceFrmPos(newMatrixPosXlocal + 1, newMatrixPosYlocal + 1)
            print old_state_pos

            #Promotion
            if (BLACKTURN == True and newMatrixPosXlocal <= 2):
                if (pos[-1:] == 'f' and newMatrixPosXlocal <= 0) or (pos[-1:] == 'n' and newMatrixPosXlocal <= 1):
                    pos = pos.upper()
                else:
                    pos = self.promotion(pos)
            if (BLACKTURN == False and newMatrixPosXlocal >= 6):
                pos = self.promotion(pos)

            #Capture
            if (gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal] != 0):
                print 'Captured: ' + gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal]
                if BLACKTURN == True:
                    blackcaptured.append(gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal].lower())
                    newButton = Button(self.dropBlacks, text= 'B' + str(gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal]).lower()[-1:])
                    newButton.pack()
                    self.dropBlacksPieces.append(newButton)

                if BLACKTURN == False:
                    whitecaptured.append(gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal].lower())
                    newButton = Button(self.dropWhites, text= 'W' + str(gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal]).lower()[-1:])
                    newButton.pack()
                    self.dropWhitePieces.append(newButton)


            GAMESTATE = 0


            gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal] = pos
            gameMatrix[oldMatrixPosXlocal][oldMatrixPosYlocal] = 0
            self.cells[(oldMatrixPosXlocal, oldMatrixPosYlocal)].configure(text='')



            #Check for checks
            #This method. Is. perfect.
            if isCheck == False:
                #Does our move reveal a check for the other team?
                BLACKTURN = not BLACKTURN
                for i in range(0, size_board):
                    for j in range(0, size_board):
                        p = self.getPieceFrmPos(i + 1, j + 1)
                        if p != 0:
                            self.isKingUnderCheck(i, j, p)

                            if isCheck == True:
                                print 'ILLEGAL MOVE: Reveals check'
                                break

                    if isCheck == True:
                        break
                BLACKTURN = not BLACKTURN

            if isCheck == False:
                #Does our move give a check?
                for i in range(0, size_board):
                    for j in range(0, size_board):
                        p = self.getPieceFrmPos(i + 1, j + 1)
                        if p != 0:
                            self.isKingUnderCheck(i, j, p)

            else:
                #Does our move get us out of a check?
                print 'Now that the opponents move has been made, lets check if check is still valid'
                BLACKTURN = not BLACKTURN
                for i in range(0, size_board):
                    for j in range(0, size_board):
                        p = self.getPieceFrmPos(i + 1, j + 1)
                        if p != 0:
                            self.isKingUnderCheck(i, j, p)

                #reminder: [y axis][x axis]
                if BLACKTURN == True:
                    kingcolor = self.cells[self.getPosFromPiece('Wk')].cget('background')
                else:
                    kingcolor = self.cells[self.getPosFromPiece('Bk')].cget('background')

                if (kingcolor == 'cyan') :
                    print 'Still in check, Restart that move'
                    old_fill = old_state_pos
                    if old_fill == 0:
                        old_fill = ''

                    print 'Resetting old position: ' + str(old_fill) + ' as move ' + str(pos) + ' is illegal'
                    #Load back or direct drop?
                    if (BLACKTURN == True):
                        self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(text=upsidedown.convChartoUpsideDown(str(old_fill)[-1:]))
                        self.cells[(oldMatrixPosXlocal, oldMatrixPosYlocal)].configure(text=upsidedown.convChartoUpsideDown(str(pos)[-1:]))
                    else:
                        self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(text=str(old_fill)[-1:])
                        self.cells[(oldMatrixPosXlocal, oldMatrixPosYlocal)].configure(text=str(pos)[-1:])

                        #self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(text=upsidedown.convChartoUpsideDown(pos[-1:]))
                    BLACKTURN = not BLACKTURN
                    gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal] = old_state_pos
                    gameMatrix[oldMatrixPosXlocal][oldMatrixPosYlocal] = pos
                    self.resetBoardGraphics()

                    newMatrixPosX = None
                    newMatrixPosY = None
                    oldMatrixPosX = None
                    oldMatrixPosY = None
                    posToMove = None
                    GAMESTATE = 0

                    return

                else:
                    print 'King is out of check, continue play'
                    isCheck = False
                    BLACKTURN = not BLACKTURN



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



            if (BLACKTURN == True):
                self.turnIndicator.configure(text='White Turn')
                BLACKTURN = False
            else:
                self.turnIndicator.configure(text='Black Turn')
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
                                print('Move not on board so ignoring')
            return 1
        else:
            print 'It is not your turn yet'
            return 0

    def getNumberPossibleMoves(self, oldMatrixPosX, oldMatrixPosY, pos):
        count = 0
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
                                count = count + 1

                            if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] != 'W') and BLACKTURN == False):
                                count = count + 1

                            if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] == 'W') and BLACKTURN == True):
                                break

                            if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] == 'B') and BLACKTURN == False):
                                break

                        except Exception as e:
                            print('Move not on board so ignoring')
        return count

    def click(self, row, col):
        global GAMESTATE, newMatrixPosX, newMatrixPosY, oldMatrixPosX, oldMatrixPosY, posToMove, gameMatrix
        pos = gameMatrix[row][col]


        if GAMESTATE == 3:
            self.cells[(row, col)].configure(background='RED')
            newMatrixPosX = row
            newMatrixPosY = col



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

    def getPosFromPiece(self, pos):
        global gameMatrix
        for i in range(0, size_board):
            for j in range(0, size_board):
                if pos == gameMatrix[i][j]:
                    return i,j
        return None

    def getPieceFrmPos(self, h, w):
        global gameMatrix
        return gameMatrix[(h-1)][(w-1)]

    #TODO: Change this to something other than Tkinter. 3d graphics would be cool
    def DrawBoard(self, Matrix):
        root = Tk()
        root.title('ShogAI')
        root.geometry('1009x1009')
        self.cells = {}
        self.turnIndicator = None
        self.dropBlacksPieces = []
        self.dropWhitePieces = []

        # create main container
        center = Frame(root, bg='white', width=900, height=900, padx=3, pady=3)
        bottom = Frame(root, bg='yellow', width=200, height=900, padx=3, pady=3)
        right = Frame(root, bg='black', width=900, height=200, padx=3, pady=3)
        left = Frame(root, bg='gray', width=900, height=200, padx=3, pady=3)

        # layout all of the main containers
        root.grid_rowconfigure(size_board, weight=1)
        root.grid_columnconfigure(size_board, weight=1)

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

        drawMatrix = copy.deepcopy(gameMatrix)
        for row in range(size_board):
            for column in range(size_board):
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


        self.options = Frame(bottom)
        self.options.grid(column=0)

        self.dropBlacks = Frame(right)
        self.dropBlacks.grid(column=0)

        self.dropWhites = Frame(left)
        self.dropWhites.grid(column=0)



        TurnIndicator = Label(self.options, text='Blacks Turn', bg='white', highlightbackground="black", highlightcolor="black", highlightthickness=1, height=3, width=9)

        TurnIndicator.pack()
        self.turnIndicator = TurnIndicator
        root.mainloop()

    def initStandardGame(self):
        with open('configure.txt') as f:
            content = f.read()
        map_size = int(content)

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
