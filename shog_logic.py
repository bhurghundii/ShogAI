import upsidedown
from tkinter import Button
from tkinter import messagebox
import random
import copy
from shog_ext import *
from shog_ext import shog_play_external_moves as spem

class shog_logic:
    def __init__(self, gameState, cells, turnIndicator, dropBlacks, dropWhites, dropBlacksPieces, dropWhitePieces):
        self.gameState = gameState
        self.cells = cells
        self.turnIndicator = turnIndicator
        self.dropBlacks = dropBlacks
        self.dropWhites = dropWhites
        self.dropBlacksPieces = dropBlacksPieces
        self.dropWhitePieces = dropWhitePieces
        self.simulMoveMatrix = []
        self.simulMoveMatrixPre = []

    def singleStepPlay(self):
        if (self.gameState.isLoad != True):
            print ('Single Step is not available because load not selected')
        else:
            print ('Single Step')
            self.gameState.gameState = 0
            self.click(0, 0, True)
            shog_ext = shog_play_external_moves()
            if (gameTurn().gameTurn >= shog_ext.getLengthOfPlay()):
                self.gameState.isLoad = False

    def singlePlayNextMove_ext(self):
        self.gameState.isLoad = True
        print ('Single Step')
        self.gameState.gameState = 0
        self.click(0, 0, True)
        self.gameState.isLoad = False

    def fullStepPlay(self):
        if (self.gameState.isLoad != True):
            print ('Full Step is not available because load not selected')
        else:
            print ('Full Step')
            shog_ext = shog_play_external_moves()
            for l in range(0, shog_ext.getLengthOfPlay()):
                self.click(0, 0, True)
            shog_ext.clearLoadGame()
            self.gameState.isLoad = False

    def click(self, row, col, isLoad = None):
        pos = self.gameState.gameMatrix[row][col]

        if self.gameState.gameState == 3:
            self.cells[(row, col)].configure(background='RED')
            print(('PIECE DROP:' + str(self.getPieceFrmPos(row + 1, col + 1))))

            if (str(self.getPieceFrmPos(row + 1, col + 1)) == '0'):
                self.gameState.newMatrixPosX = row
                self.gameState.newMatrixPosY = col
                pos = None
                if self.gameState.isBlackTurn == True:
                    print(('BLACK', len(self.gameState.blackcaptured), self.gameState.droprank, self.gameState.blackcaptured))
                    pos = self.gameState.blackcaptured[self.gameState.droprank]
                else:
                    print(('WHITE', len(self.gameState.whitecaptured), self.gameState.droprank, self.gameState.whitecaptured))
                    pos = self.gameState.whitecaptured[self.gameState.droprank]

                if 'n' in pos:
                    if (row <= 1 and self.gameState.isBlackTurn == True) or (row >= 7 and self.gameState.isBlackTurn == False):
                        print('Too deep for knight')
                        self.resetBoardGraphics()
                        pos = None
                        self.softReset()
                    else:
                        self.moveLegalDrop(pos, row, col)

                        self.gameState.isBlackTurn = not self.gameState.isBlackTurn
                        if self.gameState.isBlackTurn == True:
                            #self.gameState.blackcaptured.pop(self.gameState.droprank)
                            self.dropBlacksPieces[self.gameState.droprank].pack_forget()
                        else:
                            #self.gameState.whitecaptured.pop(self.gameState.droprank)
                            self.dropWhitePieces[self.gameState.droprank].pack_forget()
                        self.ResetSwitchTurns()


                elif 'l' in pos:
                    if (row == 0 and self.gameState.isBlackTurn == True) or (row == 8 and self.gameState.isBlackTurn == False):
                        print('Too deep for lance')
                        self.resetBoardGraphics()
                        pos = None
                        self.softReset()
                    else:

                        self.moveLegalDrop(pos, row, col)

                        self.gameState.isBlackTurn = not self.gameState.isBlackTurn
                        if self.gameState.isBlackTurn == True:
                            #self.gameState.blackcaptured.pop(self.gameState.droprank)
                            self.dropBlacksPieces[self.gameState.droprank].pack_forget()
                        else:
                            #self.gameState.whitecaptured.pop(self.gameState.droprank)
                            self.dropWhitePieces[self.gameState.droprank].pack_forget()
                        self.ResetSwitchTurns()

                #no 2 pawn rule
                elif 'p' in pos:
                    if (row == 8 and self.gameState.isBlackTurn == True) or (row == 0 and self.gameState.isBlackTurn == False):
                        print('Too deep for pawn')
                        self.resetBoardGraphics()
                        self.softReset()
                        pos = None
                    else:
                        colMat = []
                        for y in range(0, self.gameState.board_size):
                            colMat.append(self.gameState.gameMatrix[y][col])

                        print(colMat)
                        pawnTeam = 'p'
                        if self.gameState.isBlackTurn == True:
                            pawnTeam = 'B' + pawnTeam
                        else:
                            pawnTeam = 'W' + pawnTeam

                        if pawnTeam in colMat:
                            print('There is a pawn on this column')
                            pos = None
                            self.resetBoardGraphics()
                            self.softReset()

                        else:
                            #get pos of king
                            kingTeam = 'k'
                            if self.gameState.isBlackTurn == True:
                                kingTeam = 'W' + kingTeam
                            else:
                                kingTeam = 'B' + kingTeam

                            self.moveLegalDrop(pawnTeam, row, col)
                            self.gameState.isBlackTurn = not self.gameState.isBlackTurn


                            if self.gameState.isBlackTurn == True:
                                print('Removing from Black stack')
                                #self.gameState.blackcaptured.pop(self.gameState.droprank)
                                self.dropBlacksPieces[self.gameState.droprank].pack_forget()

                            else:
                                print('Removing from White stack')
                                #self.gameState.whitecaptured.pop(self.gameState.droprank)
                                self.dropWhitePieces[self.gameState.droprank].pack_forget()

                            self.ResetSwitchTurns()



                elif 'p' not in pos and 'l' not in pos and 'n' not in pos:
                    pos = pos[-1:]
                    if self.gameState.isBlackTurn == True:
                        pos = 'B' + pos
                    else:
                        pos = 'W' + pos

                    self.moveLegalDrop(pos, row, col)

                    self.gameState.isBlackTurn = not self.gameState.isBlackTurn
                    if self.gameState.isBlackTurn == True:
                        #self.gameState.blackcaptured.pop(self.gameState.droprank)
                        self.dropBlacksPieces[self.gameState.droprank].pack_forget()
                    else:
                        #self.gameState.whitecaptured.pop(self.gameState.droprank)
                        self.dropWhitePieces[self.gameState.droprank].pack_forget()
                    self.ResetSwitchTurns()
            else:
                print('A piece is already there. Move illegal.')
                self.resetBoardGraphics()

        elif self.gameState.gameState == 1:
            self.cells[(row, col)].configure(background='blue')
            self.gameState.newMatrixPosX = row
            self.gameState.newMatrixPosY = col
            self.gameState.gameState = 2

        elif self.gameState.gameState == 0:
            #AI parts
            shog_ext = shog_play_external_moves()

            if (self.gameState.isLoad == True and isLoad == True) or shog_ext.isThereAMoveToPlay_ext():
                print('TURN: ' + str(gameTurn().gameTurn + 1))
                shog_ext.updateMoveToPlayIfNotEmpty(gameTurn().gameTurn)

                if (shog_ext.isThereAMoveToPlay_ext()):
                    moveRead = shog_ext.convertTurnToGameMatrixCompatible()
                    possiblepcs = []
                    for i in range(0, self.gameState.board_size):
                        for j in range(0, self.gameState.board_size):
                            p = self.getPieceFrmPos(i + 1, j + 1)
                            if p != 0:
                                possiblepc = self.getPosWhichCanMakeMove(i, j, p, moveRead[4] + 1, moveRead[5] + 1)
                                if possiblepc != '':
                                    possiblepcs.append((possiblepc, i, j))

                    #print('PRE-MOVE: ' + str(possiblepcs))

                    if len(possiblepcs) == 1:
                        pos = possiblepcs[0][0]
                        self.gameState.oldMatrixPosX = possiblepcs[0][1]
                        self.gameState.oldMatrixPosY = possiblepcs[0][2]
                        self.gameState.newMatrixPosX = moveRead[4]
                        self.gameState.newMatrixPosY = moveRead[5]
                        self.gameState.pieceSelected = pos
                        self.gameState.gameState = 2
                        self.gameState.gameState = self.getPossibleMoves(self.gameState.oldMatrixPosX, self.gameState.oldMatrixPosY, pos)
                        open('ext_data/movetoplay.txt', 'w').close()
                    else:

                        for c in range(0, len(possiblepcs)):
                            print(possiblepcs[c])
                            if possiblepcs[c][0] == moveRead[1]:
                                pos = possiblepcs[c][0]
                                self.gameState.oldMatrixPosX = possiblepcs[c][1]
                                self.gameState.oldMatrixPosY = possiblepcs[c][2]
                                self.gameState.newMatrixPosX = moveRead[4]
                                self.gameState.newMatrixPosY = moveRead[5]
                                self.gameState.pieceSelected = moveRead[1]
                                self.gameState.gameState = 2
                                self.gameState.gameState = self.getPossibleMoves(self.gameState.oldMatrixPosX, self.gameState.oldMatrixPosY, pos)
                                open('ext_data/movetoplay.txt', 'w').close()
                else:
                    print ('As there are no more moves to load, proceed')
                    self.gameState.isLoad = False
                    isLoad = False
            else:
                if pos != 0:
                    self.cells[(row, col)].configure(background='yellow')
                    self.gameState.oldMatrixPosX = row
                    self.gameState.oldMatrixPosY = col
                    self.gameState.pieceSelected = pos
                    self.gameState.gameState = self.getPossibleMoves(self.gameState.oldMatrixPosX, self.gameState.oldMatrixPosY, pos)
                    self.gameState.isLoad = False
                    isLoad = False

        if self.gameState.newMatrixPosX != None and self.gameState.newMatrixPosY != None and self.gameState.pieceSelected != None:
            #print('TRYING: ' + str((self.gameState.pieceSelected, self.gameState.oldMatrixPosX, self.gameState.oldMatrixPosY,  self.gameState.newMatrixPosX, self.gameState.newMatrixPosY)))
            self.resetBoardGraphics()
            self.moveLegalGO(self.gameState.pieceSelected, self.gameState.oldMatrixPosX, self.gameState.oldMatrixPosY,  self.gameState.newMatrixPosX, self.gameState.newMatrixPosY)

    def resetBoardGraphics(self):
        for i in range(0, self.gameState.board_size):
            for j in range(0, self.gameState.board_size):
                self.cells[(i, j)].configure(background='white')

    def ResetSwitchTurns(self):

        self.resetBoardGraphics()
        self.softReset()

        if (self.gameState.isBlackTurn == True):
            self.turnIndicator.configure(text='White Turn')
            self.gameState.isBlackTurn = False
        else:
            self.turnIndicator.configure(text='Black Turn')
            self.gameState.isBlackTurn = True

    def softReset(self):
        self.gameState.newMatrixPosX = None
        self.gameState.newMatrixPosY = None
        self.gameState.oldMatrixPosX = None
        self.gameState.oldMatrixPosY = None
        self.gameState.pieceSelected = None
        self.gameState.gameState = 0

    def getPosFromPiece(self, pos):
        for i in range(0, self.gameState.board_size):
            for j in range(0, self.gameState.board_size):
                if pos == self.gameState.gameMatrix[i][j]:
                    return i,j
        return None

    def getPieceFrmPos(self, h, w):
        return self.gameState.gameMatrix[(h-1)][(w-1)]

    def getPossibleMoves(self, oldMatrixPosX, oldMatrixPosY, pos):

        if (self.gameState.isBlackTurn == True and pos[:-1] == 'B') or (self.gameState.isBlackTurn == False and pos[:-1] == 'W'):
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
                                if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] == 'B') and self.gameState.isBlackTurn == True):
                                    break

                                if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] == 'W') and self.gameState.isBlackTurn == False):
                                    break

                                if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] != 'B') and self.gameState.isBlackTurn == True):
                                    self.cells[(oldMatrixPosX + x_dif, oldMatrixPosY + y_dif)].configure(background='orange')
                                    self.gameState.possibleMoveMatrix.append((oldMatrixPosX + x_dif, oldMatrixPosY + y_dif))

                                if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] != 'W') and self.gameState.isBlackTurn == False):
                                    self.cells[(oldMatrixPosX + x_dif, oldMatrixPosY + y_dif)].configure(background='orange')
                                    self.gameState.possibleMoveMatrix.append((oldMatrixPosX + x_dif, oldMatrixPosY + y_dif))

                                if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] == 'W') and self.gameState.isBlackTurn == True):
                                    break

                                if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] == 'B') and self.gameState.isBlackTurn == False):
                                    break

                            except Exception as e:
                                print(e)
                                print('Move not on board so ignoring')
            return 1
        else:
            print('It is not your turn yet')
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
                            if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] == 'B') and self.gameState.isBlackTurn == True):
                                break

                            if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] == 'W') and self.gameState.isBlackTurn == False):
                                break

                            if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] != 'B') and self.gameState.isBlackTurn == True):
                                count = count + 1

                            if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] != 'W') and self.gameState.isBlackTurn == False):
                                count = count + 1

                            if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] == 'W') and self.gameState.isBlackTurn == True):
                                break

                            if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] == 'B') and self.gameState.isBlackTurn == False):
                                break

                        except Exception as e:
                            print('Move not on board so ignoring')
        return count

    def moveLegalGO(self, pos, oldMatrixPosXlocal, oldMatrixPosYlocal, newMatrixPosXlocal, newMatrixPosYlocal):

        #For the game recorder
        resultPromotion = False
        resultCapture = False
        resultDrop = False

        if ((newMatrixPosXlocal,newMatrixPosYlocal)) in self.gameState.possibleMoveMatrix:

            #When recording games... we check who actually made the move
            #Done by checking who can do it, THEN seeing if we need to clear ambiguity
            possiblepcs = []
            for i in range(0, self.gameState.board_size):
                for j in range(0, self.gameState.board_size):
                    p = self.getPieceFrmPos(i + 1, j + 1)
                    if p != 0:
                        possiblepc = self.getPosWhichCanMakeMove(i, j, p, newMatrixPosXlocal + 1, newMatrixPosYlocal + 1)
                        if possiblepc != '':
                            possiblepcs.append(possiblepc)

            #print(possiblepcs)
            #Get current pre-move position we are moving to
            old_state_pos = self.getPieceFrmPos(newMatrixPosXlocal + 1, newMatrixPosYlocal + 1)

            #Promotion
            if (self.gameState.isBlackTurn == True and (newMatrixPosXlocal <= 2 or oldMatrixPosXlocal <= 2)):
                if (pos[-1:] == 'p' and newMatrixPosXlocal <= 0) or (pos[-1:] == 'n' and newMatrixPosXlocal <= 1)  or (pos[-1:] == 'l' and newMatrixPosXlocal <= 0):
                    pos = pos.upper()
                    resultPromotion = True
                else:
                    pos, resultPromotion = self.promotion(pos)
            if (self.gameState.isBlackTurn == False and (newMatrixPosXlocal >= 6 or oldMatrixPosXlocal >= 6)):
                if (pos[-1:] == 'p' and newMatrixPosXlocal >= 8) or (pos[-1:] == 'n' and newMatrixPosXlocal >= 7)  or (pos[-1:] == 'l' and newMatrixPosXlocal >= 8):
                    pos = pos.upper()
                    resultPromotion = True
                else:
                    pos, resultPromotion = self.promotion(pos)

            #Capture
            if (self.gameState.gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal] != 0):
                print('Captured: ' + self.gameState.gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal])
                cap_piece = self.gameState.gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal]
                if self.gameState.isBlackTurn == True:
                    self.gameState.blackcaptured.append('B' + cap_piece[-1:].lower())
                    print(('Adding to black: ' + str(len(self.gameState.blackcaptured))))
                    newButton = Button(self.dropBlacks, text= 'B' + str(self.gameState.gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal]).lower()[-1:], command = lambda row=len(self.gameState.blackcaptured), piece='B' : self.clickDrop(row, piece))
                    newButton.pack()
                    self.dropBlacksPieces.append(newButton)
                    resultCapture = True

                if self.gameState.isBlackTurn == False:
                    print(('Adding to white: ' + str(len(self.gameState.whitecaptured))))
                    self.gameState.whitecaptured.append('W' + cap_piece[-1:].lower())
                    newButton = Button(self.dropWhites, text= 'W' + str(self.gameState.gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal]).lower()[-1:], command = lambda row=len(self.gameState.whitecaptured), piece='W' : self.clickDrop(row, piece))
                    newButton.pack()
                    self.dropWhitePieces.append(newButton)
                    resultCapture = True


            self.gameState.gameState = 0


            self.gameState.gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal] = pos
            self.gameState.gameMatrix[oldMatrixPosXlocal][oldMatrixPosYlocal] = 0
            self.cells[(oldMatrixPosXlocal, oldMatrixPosYlocal)].configure(text='')



            #Check for checks
            #This method. Is. perfect.
            if self.gameState.isCheck == False:
                #Does our move reveal a check for the other team?
                self.gameState.isBlackTurn = not self.gameState.isBlackTurn
                for i in range(0, self.gameState.board_size):
                    for j in range(0, self.gameState.board_size):
                        p = self.getPieceFrmPos(i + 1, j + 1)
                        if p != 0:
                            self.isKingUnderCheck(i, j, p)

                            if self.gameState.isCheck == True:
                                print('ILLEGAL MOVE: Reveals check')
                                break

                    if self.gameState.isCheck == True:
                        break
                self.gameState.isBlackTurn = not self.gameState.isBlackTurn

            if self.gameState.isCheck == False:
                #Does our move give a check?
                for i in range(0, self.gameState.board_size):
                    for j in range(0, self.gameState.board_size):
                        p = self.getPieceFrmPos(i + 1, j + 1)
                        if p != 0:
                            self.isKingUnderCheck(i, j, p)

            else:
                #Does our move get us out of a check?
                print('Now that the opponents move has been made, lets check if check is still valid')
                self.gameState.isBlackTurn = not self.gameState.isBlackTurn
                for i in range(0, self.gameState.board_size):
                    for j in range(0, self.gameState.board_size):
                        p = self.getPieceFrmPos(i + 1, j + 1)
                        if p != 0:
                            self.isKingUnderCheck(i, j, p)

                #reminder: [y axis][x axis]
                if self.gameState.isBlackTurn == True:
                    kingcolor = self.cells[self.getPosFromPiece('Wk')].cget('background')
                else:
                    kingcolor = self.cells[self.getPosFromPiece('Bk')].cget('background')

                if (kingcolor == 'cyan') :
                    print('Still in check, Restart that move')
                    old_fill = old_state_pos
                    if old_fill == 0:
                        old_fill = ''

                    print('Resetting old position: ' + str(old_fill) + ' as move ' + str(pos) + ' is illegal')
                    #Load back or direct drop?
                    if (self.gameState.isBlackTurn == True):
                        self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(text=upsidedown.convChartoUpsideDown(str(old_fill)[-1:]))
                        self.cells[(oldMatrixPosXlocal, oldMatrixPosYlocal)].configure(text=upsidedown.convChartoUpsideDown(str(pos)[-1:]))
                    else:
                        self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(text=str(old_fill)[-1:])
                        self.cells[(oldMatrixPosXlocal, oldMatrixPosYlocal)].configure(text=str(pos)[-1:])

                        #self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(text=upsidedown.convChartoUpsideDown(pos[-1:]))
                    self.gameState.isBlackTurn = not self.gameState.isBlackTurn
                    self.gameState.gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal] = old_state_pos
                    self.gameState.gameMatrix[oldMatrixPosXlocal][oldMatrixPosYlocal] = pos
                    self.resetBoardGraphics()

                    self.softReset()

                    return

                else:
                    print('King is out of check, continue play')
                    self.gameState.isCheck = False
                    self.gameState.isBlackTurn = not self.gameState.isBlackTurn




            if (self.gameState.isBlackTurn == True):
                self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(text=pos[-1:])
            else:
                self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(text=upsidedown.convChartoUpsideDown(pos[-1:]))

            self.resetBoardGraphics()



            self.gameState.newMatrixPosX = None
            self.gameState.newMatrixPosY = None
            self.gameState.oldMatrixPosX = None
            self.gameState.oldMatrixPosY = None
            self.gameState.pieceSelected = None


            if len(possiblepcs) != len(set(possiblepcs)):
                shog_recorder().recordMove(pos, resultPromotion, resultCapture, resultDrop, newMatrixPosYlocal, newMatrixPosXlocal, oldMatrixPosYlocal , oldMatrixPosXlocal )
            else:
                shog_recorder().recordMove(pos, resultPromotion, resultCapture, resultDrop, newMatrixPosYlocal, newMatrixPosXlocal)

            self.gameState.recordingFile = shog_recorder().getFileRecord()

            if (self.gameState.isBlackTurn == True):
                self.turnIndicator.configure(text='White Turn')
                self.gameState.isBlackTurn = False
            else:
                self.turnIndicator.configure(text='Black Turn')
                self.gameState.isBlackTurn = True


        else:
            print('That move is NOT legal!')

            self.resetBoardGraphics()
            self.softReset()

        self.gameState.possibleMoveMatrix *= 0


        #Now we check if its a checkmate
        if (self.gameState.isCheck == True):

            #Get all of your available moves
            print('JUDGE: Checking if it is a checkmate')
            resetMatrix = copy.deepcopy(self.gameState.gameMatrix)
            for i in range(0, self.gameState.board_size):
                for j in range(0, self.gameState.board_size):
                    self.populateSimulMoveArrays(i, j, str(self.gameState.gameMatrix[i][j]), True)

            for i in range(0, len(self.simulMoveMatrix)):
                if (self.simulateMove (self.simulMoveMatrixPre[i][0], self.simulMoveMatrixPre[i][1], self.simulMoveMatrixPre[i][2], self.simulMoveMatrix[i][0], self.simulMoveMatrix[i][1], i) == False):
                    break
                if i == (len(self.simulMoveMatrix) - 1):
                    #Check if we can drop a piece to cover the check
                    for k in range(0, len(self.simulMoveMatrix)):

                        if 'k' in self.simulMoveMatrix[k][2]:
                            if (self.gameState.isBlackTurn == True):
                                if (self.simulateDrop('Wp', self.simulMoveMatrix[i][0], self.simulMoveMatrix[i][1]) == False):
                                    break
                            else:
                                if (self.simulateDrop('Bp', self.simulMoveMatrix[i][0], self.simulMoveMatrix[i][1]) == False):
                                    break

                        print('RESULT: Checkmate! GAMEOVER')

            self.simulMoveMatrixPre *= 0
            self.simulMoveMatrix *= 0

    def getPosWhichCanMakeMove(self, oldMatrixPosX, oldMatrixPosY, pos, newMatrixPosX, newMatrixPosY):
        if (self.gameState.isBlackTurn == True and pos[:-1] == 'B') or (self.gameState.isBlackTurn == False and pos[:-1] == 'W'):
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
                                if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] == 'B') and self.gameState.isBlackTurn == True):
                                    break

                                if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] == 'W') and self.gameState.isBlackTurn == False):
                                    break

                                if ((oldMatrixPosX + x_dif + 1 == newMatrixPosX) and (oldMatrixPosY + y_dif + 1 == newMatrixPosY)):
                                    self.cells[(oldMatrixPosX + x_dif, oldMatrixPosY + y_dif)].configure(background='red')
                                    return pos

                                if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] == 'W') and self.gameState.isBlackTurn == True):
                                    break

                                if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] == 'B') and self.gameState.isBlackTurn == False):
                                    break

                            except Exception as e:
                                pass
            return ''
        else:
            return ''

    def isKingUnderCheck(self, oldMatrixPosX, oldMatrixPosY, pos):

        if (self.gameState.isBlackTurn == True and pos[:-1] == 'B') or (self.gameState.isBlackTurn == False and pos[:-1] == 'W'):
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
                                    if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] == 'B') and self.gameState.isBlackTurn == True):
                                        break

                                    if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] == 'W') and self.gameState.isBlackTurn == False):
                                        break

                                    if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] != 'B') and self.gameState.isBlackTurn == True):
                                        if str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1)) == 'Wk':
                                            print('BLACK CHECK!')
                                            self.gameState.isCheck = True

                                        self.cells[(oldMatrixPosX + x_dif, oldMatrixPosY + y_dif)].configure(background='cyan')



                                    if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] != 'W') and self.gameState.isBlackTurn == False):
                                        if str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1)) == 'Bk':
                                            print('WHITE CHECK!')
                                            self.gameState.isCheck = True

                                        self.cells[(oldMatrixPosX + x_dif, oldMatrixPosY + y_dif)].configure(background='cyan')

                                    if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] == 'W') and self.gameState.isBlackTurn == True):
                                        break

                                    if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] == 'B') and self.gameState.isBlackTurn == False):
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
                return pos.upper(), True
            else:
                return pos, False
        return pos, False

    def clickDrop(self, row, piece):

        print(('DROPPING: ', row, piece))

        with open('configure.txt') as f:
            configContent = f.readlines()
        dropSetting = int(configContent[1])

        if (dropSetting == 0):

            if (self.gameState.isBlackTurn == True and 'B' in piece) or (self.gameState.isBlackTurn == False and 'W' in piece):
                self.gameState.droprank = row - 1
                self.gameState.gameState = 3
            else:
                print('You can not drop your opponents pieces')
                self.resetBoardGraphics()
                self.gameState.gameState = 0

    def moveLegalDrop(self, pos, newMatrixPosXlocal, newMatrixPosYlocal):
        global isCheck, GAMESTATE, newMatrixPosX, newMatrixPosY, posToMove, gameMatrix, BLACKTURN
        #Get current pre-move position we are moving to
        old_state_pos = self.getPieceFrmPos(newMatrixPosXlocal + 1, newMatrixPosYlocal + 1)
        print(old_state_pos)

        #For the game recorder
        resultPromotion = False
        resultCapture = False
        resultDrop = True

        #No Capturing or Promotion
        self.gameState.gameState = 0


        self.gameState.gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal] = pos

        #Check for checks
        #This method. Is. perfect.
        if self.gameState.isCheck == False:
            #Does our move reveal a check for the other team?
            self.gameState.isBlackTurn = not self.gameState.isBlackTurn
            for i in range(0, self.gameState.board_size):
                for j in range(0, self.gameState.board_size):
                    p = self.getPieceFrmPos(i + 1, j + 1)
                    if p != 0:
                        self.isKingUnderCheck(i, j, p)

                        if self.gameState.isCheck == True:
                            print('ILLEGAL MOVE: Reveals check')
                            break

                if self.gameState.isCheck == True:
                    break
            self.gameState.isBlackTurn = not self.gameState.isBlackTurn

        if self.gameState.isCheck == False:
            #Does our move give a check?
            for i in range(0, self.gameState.board_size):
                for j in range(0, self.gameState.board_size):
                    p = self.getPieceFrmPos(i + 1, j + 1)
                    if p != 0:
                        self.isKingUnderCheck(i, j, p)

        else:
            #Does our move get us out of a check?
            print('Now that the opponents move has been made, lets check if check is still valid')
            self.gameState.isBlackTurn = not self.gameState.isBlackTurn
            for i in range(0, self.gameState.board_size):
                for j in range(0, self.gameState.board_size):
                    p = self.getPieceFrmPos(i + 1, j + 1)
                    if p != 0:
                        self.isKingUnderCheck(i, j, p)

            #reminder: [y axis][x axis]
            if self.gameState.isBlackTurn == True:
                kingcolor = self.cells[self.getPosFromPiece('Wk')].cget('background')
            else:
                kingcolor = self.cells[self.getPosFromPiece('Bk')].cget('background')

            if (kingcolor == 'cyan') :
                print('Still in check, Restart that move')
                old_fill = old_state_pos
                if old_fill == 0:
                    old_fill = ''

                print('Resetting old position: ' + str(old_fill) + ' as move ' + str(pos) + ' is illegal')
                #Load back or direct drop?
                if (self.gameState.isBlackTurn == True):
                    self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(text='')
                else:
                    self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(text='')

                    #self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(text=upsidedown.convChartoUpsideDown(pos[-1:]))
                self.gameState.isBlackTurn = not self.gameState.isBlackTurn
                self.gameState.gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal] = old_state_pos
                self.resetBoardGraphics()

                self.softReset()

                return

            else:
                print('King is out of check, continue play')
                self.gameState.isCheck = False
                self.gameState.isBlackTurn = not self.gameState.isBlackTurn




        if (self.gameState.isBlackTurn == True):
            self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(text=pos[-1:])
        else:
            self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(text=upsidedown.convChartoUpsideDown(pos[-1:]))

        self.resetBoardGraphics()



        self.softReset()



        if (self.gameState.isBlackTurn == True):
            self.turnIndicator.configure(text='White Turn')
            self.gameState.isBlackTurn = False
        else:
            self.turnIndicator.configure(text='Black Turn')
            self.gameState.isBlackTurn = True

        shog_recorder().recordMove(pos, resultPromotion, resultCapture, resultDrop, newMatrixPosYlocal, newMatrixPosXlocal)

        self.gameState.possibleMoveMatrix *= 0

        #Now we check if its a checkmate
        if (self.gameState.isCheck == True):

            #Get all of your available moves

            resetMatrix = copy.deepcopy(self.gameState.gameMatrix)
            for i in range(0, self.gameState.board_size):
                for j in range(0, self.gameState.board_size):
                    self.populateSimulMoveArrays(i, j, str(self.gameState.gameMatrix[i][j]), True)



            for i in range(0, len(self.simulMoveMatrix)):
                if (self.simulateMove (self.simulMoveMatrixPre[i][0], self.simulMoveMatrixPre[i][1], self.simulMoveMatrixPre[i][2], self.simulMoveMatrix[i][0], self.simulMoveMatrix[i][1], i) == False):
                    break
                if i == (len(self.simulMoveMatrix) - 1):
                    if ('p' not in pos):
                        print('Checkmate!')
                    else:
                        print('You can not check mate by dropping a pawn')
                        old_fill = old_state_pos
                        if old_fill == 0:
                            old_fill = ''

                        print('Resetting old position: ' + str(old_fill) + ' as move ' + str(pos) + ' is illegal')
                        #Load back or direct drop?
                        if (self.gameState.isBlackTurn == True):
                            self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(text='')
                        else:
                            self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(text='')

                            #self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(text=upsidedown.convChartoUpsideDown(pos[-1:]))
                        self.gameState.isBlackTurn = not self.gameState.isBlackTurn
                        self.gameState.gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal] = old_state_pos
                        self.resetBoardGraphics()

                        self.softReset()

                        return

            self.simulMoveMatrixPre *= 0
            self.simulMoveMatrix *= 0

    def populateSimulMoveArrays(self, oldMatrixPosX, oldMatrixPosY, pos, Turn):

        kingspace = False
        if (self.gameState.isBlackTurn == True and pos[:-1] == 'B') or (self.gameState.isBlackTurn == False and pos[:-1] == 'W'):
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
                                #If the piece is Black and youre black, stop
                                if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] == 'B') and self.gameState.isBlackTurn == True):
                                    break

                                #If the piece is White and youre White, stop
                                if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] == 'W') and self.gameState.isBlackTurn == False):
                                    break

                                #If the piece is White and youre Black, you can capture so color
                                if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] != 'B') and self.gameState.isBlackTurn == True):
                                    if (Turn == False and (self.cells[(oldMatrixPosX + x_dif, oldMatrixPosY + y_dif)].cget('background')) == 'blue'):
                                        pass
                                    else:
                                        self.cells[(oldMatrixPosX + x_dif, oldMatrixPosY + y_dif)].configure(background='pink')
                                        self.simulMoveMatrixPre.append((oldMatrixPosX, oldMatrixPosY, pos))
                                        self.simulMoveMatrix.append((oldMatrixPosX + x_dif, oldMatrixPosY + y_dif, pos))

                                #If the piece is Black and youre White, you can capture so color
                                if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] != 'W') and self.gameState.isBlackTurn == False):
                                    if (Turn == False and (self.cells[(oldMatrixPosX + x_dif, oldMatrixPosY + y_dif)].cget('background')) == 'pink') or (Turn == True and 'k' in pos and (self.cells[(oldMatrixPosX + x_dif, oldMatrixPosY + y_dif)].cget('background')) == 'pink'):
                                        pass
                                    else:
                                        self.cells[(oldMatrixPosX + x_dif, oldMatrixPosY + y_dif)].configure(background='blue')
                                        self.simulMoveMatrixPre.append((oldMatrixPosX, oldMatrixPosY, pos))
                                        self.simulMoveMatrix.append((oldMatrixPosX + x_dif, oldMatrixPosY + y_dif, pos))


                                if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] == 'W') and self.gameState.isBlackTurn == True and (str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[1:] != 'k')):
                                    break

                                if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[:-1] == 'B') and self.gameState.isBlackTurn == False and (str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[1:] != 'k')):
                                    break

                            except Exception as e:
                                pass

            #Now we check if we have any drops. We only take the 8 squares surrounding the king as those are the ones that matter anyways.
            return 1
        else:
            return 0

    def simulateMove(self, oldMatrixPosXlocal, oldMatrixPosYlocal, pos, newMatrixPosXlocal, newMatrixPosYlocal, iteration):
        print('ITERATION: ' + str(iteration) + ' USING ' + str((oldMatrixPosXlocal, oldMatrixPosYlocal, pos, newMatrixPosXlocal, newMatrixPosYlocal)))

        #Get current pre-move position we are moving to
        old_state_pos = self.getPieceFrmPos(newMatrixPosXlocal + 1, newMatrixPosYlocal + 1)

        self.gameState.gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal] = pos
        self.gameState.gameMatrix[oldMatrixPosXlocal][oldMatrixPosYlocal] = 0
        self.cells[(oldMatrixPosXlocal, oldMatrixPosYlocal)].configure(text='')

        #Check for checks
        #This method. Is. perfect.
        if self.gameState.isCheck == False:
            #Does our move reveal a check for the other team?
            self.gameState.isBlackTurn = not self.gameState.isBlackTurn
            for i in range(0, self.gameState.board_size):
                for j in range(0, self.gameState.board_size):
                    p = self.getPieceFrmPos(i + 1, j + 1)
                    if p != 0:
                        self.isKingUnderCheck(i, j, p)

                        if self.gameState.isCheck == True:
                            print('ILLEGAL MOVE: Reveals check')
                            break

                if self.gameState.isCheck == True:
                    break
            self.gameState.isBlackTurn = not self.gameState.isBlackTurn

        if self.gameState.isCheck == False:
            #Does our move give a check?
            for i in range(0, self.gameState.board_size):
                for j in range(0, self.gameState.board_size):
                    p = self.getPieceFrmPos(i + 1, j + 1)
                    if p != 0:
                        self.isKingUnderCheck(i, j, p)

        else:
            #Does our move get us out of a check?
            print('Now that the opponents move has been made, lets check if check is still valid')
            self.gameState.isBlackTurn = not self.gameState.isBlackTurn
            for i in range(0, self.gameState.board_size):
                for j in range(0, self.gameState.board_size):
                    p = self.getPieceFrmPos(i + 1, j + 1)
                    if p != 0:
                        self.isKingUnderCheck(i, j, p)

            #reminder: [y axis][x axis]
            if self.gameState.isBlackTurn == True:
                kingcolor = self.cells[self.getPosFromPiece('Wk')].cget('background')
            else:
                kingcolor = self.cells[self.getPosFromPiece('Bk')].cget('background')

            if (kingcolor == 'cyan') :
                print('Still in check, Restart that move')
                old_fill = old_state_pos
                if old_fill == 0:
                    old_fill = ''

                print('Resetting old position: ' + str(old_fill) + ' as move ' + str(pos) + ' is illegal')
                #Load back or direct drop?
                if (self.gameState.board_size == True):
                    self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(text=upsidedown.convChartoUpsideDown(str(old_fill)[-1:]))
                    self.cells[(oldMatrixPosXlocal, oldMatrixPosYlocal)].configure(text=upsidedown.convChartoUpsideDown(str(pos)[-1:]))
                else:
                    self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(text=str(old_fill)[-1:])
                    self.cells[(oldMatrixPosXlocal, oldMatrixPosYlocal)].configure(text=str(pos)[-1:])

                    #self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(text=upsidedown.convChartoUpsideDown(pos[-1:]))
                self.gameState.isBlackTurn = not self.gameState.isBlackTurn
                self.gameState.gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal] = old_state_pos
                self.gameState.gameMatrix[oldMatrixPosXlocal][oldMatrixPosYlocal] = pos
                self.resetBoardGraphics()

                self.softReset()

                return True

            else:
                old_fill = old_state_pos
                if old_fill == 0:
                    old_fill = ''


                if (self.gameState.isBlackTurn == True):
                    self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(text=upsidedown.convChartoUpsideDown(str(old_fill)[-1:]))
                    self.cells[(oldMatrixPosXlocal, oldMatrixPosYlocal)].configure(text=upsidedown.convChartoUpsideDown(str(pos)[-1:]))
                else:
                    self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(text=str(old_fill)[-1:])
                    self.cells[(oldMatrixPosXlocal, oldMatrixPosYlocal)].configure(text=str(pos)[-1:])

                self.gameState.isBlackTurn = not self.gameState.isBlackTurn
                self.gameState.gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal] = old_state_pos
                self.gameState.gameMatrix[oldMatrixPosXlocal][oldMatrixPosYlocal] = pos
                self.resetBoardGraphics()

                self.softReset()

                print('King is out of check, continue play')
                self.gameState.isCheck = False
                return False




        if (self.gameState.isBlackTurn == True):
            self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(text=pos[-1:])
        else:
            self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(text=upsidedown.convChartoUpsideDown(pos[-1:]))

        self.resetBoardGraphics()



        self.gameState.newMatrixPosX = None
        self.gameState.newMatrixPosY = None
        self.gameState.oldMatrixPosX = None
        self.gameState.oldMatrixPosY = None
        self.gameState.pieceSelected = None



        if (self.gameState.isBlackTurn == True):
            self.turnIndicator.configure(text='White Turn')
            self.gameState.isBlackTurn = False
        else:
            self.turnIndicator.configure(text='Black Turn')
            self.gameState.isBlackTurn = True

        self.gameState.possibleMoveMatrix *= 0

    def simulateDrop(self, pos, newMatrixPosXlocal, newMatrixPosYlocal):
        #Get current pre-move position we are moving to
        old_state_pos = self.getPieceFrmPos(newMatrixPosXlocal + 1, newMatrixPosYlocal + 1)

        #No Capturing or Promotion
        self.gameState.gameState = 0


        self.gameState.gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal] = pos

        #Check for checks
        #This method. Is. perfect.
        if self.gameState.isCheck == False:
            #Does our move reveal a check for the other team?
            self.gameState.isBlackTurn = not self.gameState.isBlackTurn
            for i in range(0, self.gameState.board_size):
                for j in range(0, self.gameState.board_size):
                    p = self.getPieceFrmPos(i + 1, j + 1)
                    if p != 0:
                        self.isKingUnderCheck(i, j, p)

                        if self.gameState.isCheck == True:
                            print('ILLEGAL MOVE: Reveals check')
                            break

                if self.gameState.isCheck == True:
                    break
            self.gameState.isBlackTurn = not self.gameState.isBlackTurn

        if self.gameState.isCheck == False:
            #Does our move give a check?
            for i in range(0, self.gameState.board_size):
                for j in range(0, self.gameState.board_size):
                    p = self.getPieceFrmPos(i + 1, j + 1)
                    if p != 0:
                        self.isKingUnderCheck(i, j, p)

        else:
            #Does our move get us out of a check?
            print('Now that the opponents move has been made, lets check if check is still valid')
            self.gameState.isBlackTurn = not self.gameState.isBlackTurn
            for i in range(0, self.gameState.board_size):
                for j in range(0, self.gameState.board_size):
                    p = self.getPieceFrmPos(i + 1, j + 1)
                    if p != 0:
                        self.isKingUnderCheck(i, j, p)

            #reminder: [y axis][x axis]
            if self.gameState.isBlackTurn == True:
                kingcolor = self.cells[self.getPosFromPiece('Wk')].cget('background')
            else:
                kingcolor = self.cells[self.getPosFromPiece('Bk')].cget('background')

            if (kingcolor == 'cyan') :
                print('Still in check, Restart that move')
                old_fill = old_state_pos
                if old_fill == 0:
                    old_fill = ''

                print('Resetting old position: ' + str(old_fill) + ' as move ' + str(pos) + ' is illegal')
                #Load back or direct drop?
                if (self.gameState.isBlackTurn == True):
                    self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(text='')
                else:
                    self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(text='')

                    #self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(text=upsidedown.convChartoUpsideDown(pos[-1:]))
                self.gameState.isBlackTurn = not self.gameState.isBlackTurn
                self.gameState.gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal] = old_state_pos
                self.resetBoardGraphics()

                self.softReset()

                return True

            else:
                print('King is out of check, continue play')

                old_fill = old_state_pos
                if old_fill == 0:
                    old_fill = ''

                print('Resetting old position: ' + str(old_fill) + ' as move ' + str(pos) + ' is illegal')
                #Load back or direct drop?
                if (self.gameState.isBlackTurn == True):
                    self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(text='')
                else:
                    self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(text='')

                    #self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(text=upsidedown.convChartoUpsideDown(pos[-1:]))
                self.gameState.isBlackTurn = not self.gameState.isBlackTurn
                self.gameState.gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal] = old_state_pos
                self.resetBoardGraphics()

                self.softReset()

                return False

class AI_watcher(Thread, spem, shog_logic):
    def __init__(self, event, gameState):
        Thread.__init__(self)
        self.stopped = event
        self.gameState = gameState
    def run(self):
        while not self.stopped.wait(0.5):
            #Grab record sheet so far...
            try:
                file = open(self.gameState.recordingFile, 'r')
                print (file.read())
                file.close()
                if (self.getLengthOfPlay() != 0):
                    shog_logic.singlePlayNextMove_ext(self)
            except:
                print('Game has not started yet - AI on standby')
