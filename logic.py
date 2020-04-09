'''
This class controls all rules and logic for the game.
ISSUES: Long, lot's of code reuse. Check metrics on Radon
'''

import upsidedown
from tkinter import Button, messagebox
import random
import os
import sys
import copy
import traceback
import inspect
from externalfileutil import playexternalmoves as spem, gamerecorder, gameTurn
try:
    from ml.move_gen import moveGeneration
except BaseException:
    from ml.move_gen import moveGeneration
import itertools
from threading import Timer, Thread, Event
from ml.generateCSV import csvUtil as csvUtil

#This class contains all the user actions including all the rules which allow for legal shogi 
# moves and rulesets 
class logic:
    def __init__(
            self,
            gameState,
            cells,
            turnIndicator,
            dropBlacks,
            dropWhites,
            dropBlacksPieces,
            dropWhitePieces,
            CheckIndicator):
        self.gameState = gameState
        self.cells = cells
        self.turnIndicator = turnIndicator
        self.dropBlacks = dropBlacks
        self.dropWhites = dropWhites
        self.dropBlacksPieces = dropBlacksPieces
        self.dropWhitePieces = dropWhitePieces
        self.simulMoveMatrix = []
        self.simulMoveMatrixPre = []
        self.CheckIndicator = CheckIndicator

    # Single steps through a loaded game
    def singleStepPlay(self):
        if (self.gameState.isLoad != True):
            print('Single Step is not available because load not selected')
        else:
            print('Single Step')
            self.gameState.gameState = 0
            self.click(0, 0, True)
            externalfileutil = spem()

            if (gameTurn().gameTurn >= externalfileutil.getLengthOfPlay()):
                self.gameState.isLoad = False

    # This is a single step to allow the AI to play a move
    # By checking the movetoplay file and reading it
    def PlayAIMove(self):
        if os.stat("ext_data/movetoplay.txt").st_size != 0:
            print('Playing the AI')
            self.gameState.isLoad = True
            self.click(0, 0, True)
        else:
            self.gameState.isLoad = False

    # Fullstep: we play every move to fully load a file
    def fullStepPlay(self):
        if (self.gameState.isLoad != True):
            print('Full Step is not available because load not selected')
        else:
            print('Full Step')
            externalfileutil = spem()
            for l in range(0, externalfileutil.getLengthOfPlay()):
                self.click(0, 0, True)
            externalfileutil.clearLoadGame()
            self.gameState.isLoad = False

    # Checks if number is even
    def isEven(self, n):
        if (n % 2) == 0:
            return True
        else:
            return False

    # Click is the action user invokes when clicking. Different states can
    # occur.
    def click(self, row, col, isLoad=None):
        if(not self.gameState.isPromotionMessageActive):
            movesPlayed = gamerecorder().getGameLength()
            if (self.gameState.isAI):
                if (self.gameState.playerSelected ==
                        'Black' and self.isEven(movesPlayed) == False):
                    self.actionSquare(row, col, isLoad)
                elif (self.gameState.playerSelected == 'White' and self.isEven(movesPlayed)):
                    self.actionSquare(row, col, isLoad)
                elif(isLoad):
                    self.actionSquare(row, col, isLoad, True)
                else:
                    print('It is not your move yet!')
            else:
                self.actionSquare(row, col, isLoad)
    
    # Drops are handled here
    def dropAction(self, row, col):
        #Quickly color it red to show which place we want to drop it. 
        #Debugging purposes only for now.
        self.cells[(row, col)].configure(background='RED')
        if (str(self.getPieceFrmPos(row + 1, col + 1)) == '0'):
            self.gameState.newMatrixPosX = row
            self.gameState.newMatrixPosY = col
            pos = None
            if self.gameState.isBlackTurn:
                print(('BLACK',
                       len(self.gameState.blackcaptured),
                       self.gameState.droprank,
                       self.gameState.blackcaptured))
                pos = self.gameState.blackcaptured[self.gameState.droprank]
            else:
                print(('WHITE',
                       len(self.gameState.whitecaptured),
                       self.gameState.droprank,
                       self.gameState.whitecaptured))
                pos = self.gameState.whitecaptured[self.gameState.droprank]
            #Check if drop location is legal for a knight
            if 'n' in pos:
                if (row <= 1 and self.gameState.isBlackTurn) or (
                        row >= 7 and self.gameState.isBlackTurn == False):
                    print('Too deep for knight')
                    self.resetBoardGraphics()
                    pos = None
                    self.softReset()
                else:
                    self.moveLegalDrop(pos, row, col)
                    #Switch turns over when the drop is done
                    self.gameState.isBlackTurn = not self.gameState.isBlackTurn
                    #Remove the dropped piece from the stack so user cant drop again
                    if self.gameState.isBlackTurn:
                        self.dropBlacksPieces[self.gameState.droprank].pack_forget(
                        )
                    else:
                        self.dropWhitePieces[self.gameState.droprank].pack_forget(
                        )
                    self.SwitchTurns()
            #Check if drop location is legal for lance
            elif 'l' in pos:
                if (row == 0 and self.gameState.isBlackTurn) or (
                        row == 8 and self.gameState.isBlackTurn == False):
                    print('Too deep for lance')
                    self.resetBoardGraphics()
                    pos = None
                    self.softReset()
                else:

                    self.moveLegalDrop(pos, row, col)
                    #Switch turns over when the drop is done
                    self.gameState.isBlackTurn = not self.gameState.isBlackTurn
                    #Remove the dropped piece from the stack so user cant drop again
                    if self.gameState.isBlackTurn:
                        self.dropBlacksPieces[self.gameState.droprank].pack_forget(
                        )
                    else:
                        self.dropWhitePieces[self.gameState.droprank].pack_forget(
                        )
                    self.SwitchTurns()
            #This makes sure pawns are legal
            # no 2 pawn rule
            elif 'p' in pos:
                if (row == 0 and self.gameState.isBlackTurn) or (
                        row == 8 and self.gameState.isBlackTurn == False):
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
                    if self.gameState.isBlackTurn:
                        pawnTeam = 'B' + pawnTeam
                    else:
                        pawnTeam = 'W' + pawnTeam

                    if pawnTeam in colMat:
                        print('There is a pawn on this column')
                        pos = None
                        self.resetBoardGraphics()
                        self.softReset()

                    else:
                        # get pos of king
                        kingTeam = 'k'
                        if self.gameState.isBlackTurn:
                            kingTeam = 'W' + kingTeam
                        else:
                            kingTeam = 'B' + kingTeam

                        self.moveLegalDrop(pawnTeam, row, col)
                        #Switch turns over when the drop is done
                        self.gameState.isBlackTurn = not self.gameState.isBlackTurn
                        #Remove the dropped piece from the stack so user cant drop again
                        if self.gameState.isBlackTurn:
                            print('Removing from Black stack')
                            self.dropBlacksPieces[self.gameState.droprank].pack_forget(
                            )

                        else:
                            print('Removing from White stack')
                            self.dropWhitePieces[self.gameState.droprank].pack_forget(
                            )

                        self.SwitchTurns()
            #If the piece we want to drop isn't a pawn, lance or knight
            #There isn't a problem so it doesn't matter.
            elif 'p' not in pos and 'l' not in pos and 'n' not in pos:
                pos = pos[-1:]
                if self.gameState.isBlackTurn:
                    pos = 'B' + pos
                else:
                    pos = 'W' + pos
                
                self.moveLegalDrop(pos, row, col)
                #Switch turns over when the drop is done
                self.gameState.isBlackTurn = not self.gameState.isBlackTurn
                #Remove the dropped piece from the stack so user cant drop again
                if self.gameState.isBlackTurn:
                    self.dropBlacksPieces[self.gameState.droprank].pack_forget()
                else:
                    self.dropWhitePieces[self.gameState.droprank].pack_forget()
                self.SwitchTurns()
        else:
            print('A piece is already there. Move illegal.')
            self.gameState.AIMessage = 'ILLEGAL'
            self.resetBoardGraphics()
    #This function handles the interactions when the user clicks
    #on a square on the board itself
    def actionSquare(self, row, col, isLoad=None, isAILoad=None):
        pos = self.gameState.gameMatrix[row][col]
        isPromote = None
        isDrop = None
        #If the gamestate is 3 (ready for drop)
        #We do a drop action
        if self.gameState.gameState == 3:
            self.dropAction(row, col)
        #If the game state is 2 (postion to move the piece to)
        #We store the new positions and set the gamestate to 2 (invoke the normal action)
        elif self.gameState.gameState == 1:
            self.cells[(row, col)].configure(background='blue')
            self.gameState.newMatrixPosX = row
            self.gameState.newMatrixPosY = col
            self.gameState.gameState = 2
        #If the game state is 0, we first check if the AI is on or we need to load
        elif self.gameState.gameState == 0:
            # AI parts
            externalfileutil = spem()
            if (self.gameState.isLoad and isLoad) or externalfileutil.isThereAMoveToPlay_ext():
                externalfileutil.updateMoveToPlayIfNotEmpty(
                    gameTurn().gameTurn)

                if (externalfileutil.isThereAMoveToPlay_ext()):
                    print('Playing from move')

                    moveRead = externalfileutil.convertTurnToGameMatrixCompatible()
                    isPromote = moveRead[6]
                    isDrop = moveRead[7]
                    #Load a drop move
                    if isDrop:
                        print('IS LOADING A DROP', row, col, isDrop)
                        self.moveLegalDrop(
                            moveRead[1], moveRead[4], moveRead[5])

                        if (moveRead[1][:-1] == 'B'):
                            for rank in range(0, len(self.dropBlacksPieces)):
                                if moveRead[1] == self.dropBlacksPieces[rank].cget(
                                        'text'):
                                    self.dropBlacksPieces[rank].pack_forget()
                        if (moveRead[1][:-1] == 'W'):
                            for rank in range(0, len(self.dropWhitePieces)):
                                if moveRead[1] == self.dropWhitePieces[rank].cget(
                                        'text'):
                                    self.dropWhitePieces[rank].pack_forget()

                        open('ext_data/movetoplay.txt', 'w').close()

                        self.resetBoardGraphics()
                        self.softReset()

                        return

                    possiblepcs = []
                    for i in range(0, self.gameState.board_size):
                        for j in range(0, self.gameState.board_size):
                            p = self.getPieceFrmPos(i + 1, j + 1)
                            if p != 0:
                                possiblepc = self.getPosWhichCanMakeMove(
                                    i, j, p, moveRead[4] + 1, moveRead[5] + 1)
                                if possiblepc != '':
                                    possiblepcs.append((possiblepc, i, j))

                    if len(possiblepcs) == 1:
                        pos = possiblepcs[0][0]
                        self.gameState.oldMatrixPosX = possiblepcs[0][1]
                        self.gameState.oldMatrixPosY = possiblepcs[0][2]
                        self.gameState.newMatrixPosX = moveRead[4]
                        self.gameState.newMatrixPosY = moveRead[5]
                        self.gameState.pieceSelected = pos
                        self.gameState.gameState = 2
                        self.gameState.gameState = self.getPossibleMoves(
                            self.gameState.oldMatrixPosX, self.gameState.oldMatrixPosY, pos)
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
                                self.gameState.gameState = self.getPossibleMoves(
                                    self.gameState.oldMatrixPosX, self.gameState.oldMatrixPosY, pos)
                                open('ext_data/movetoplay.txt', 'w').close()

                else:
                    print('As there are no more moves to load, proceed')
                    self.gameState.isLoad = False
                    isLoad = False
            else:
                #Otherwise, just grab the piece we want to make a move
                if pos != 0:
                    self.cells[(row, col)].configure(background='yellow')
                    self.gameState.oldMatrixPosX = row
                    self.gameState.oldMatrixPosY = col
                    self.gameState.pieceSelected = pos
                    self.gameState.gameState = self.getPossibleMoves(
                        self.gameState.oldMatrixPosX, self.gameState.oldMatrixPosY, pos)
                    self.gameState.isLoad = False
                    isLoad = False
        #FIXME: Potential design bug introduced here?
        if isAILoad:
            print('LOADING AI', moveRead)
            self.gameState.oldMatrixPosX = moveRead[2]
            self.gameState.oldMatrixPosY = moveRead[3]
            self.gameState.newMatrixPosX = moveRead[4]
            self.gameState.newMatrixPosY = moveRead[5]
            self.gameState.pieceSelected = moveRead[1]
            isPromote = moveRead[6]
            isDrop = moveRead[7]
            if isPromote == None: 
                isPromote = False

            self.gameState.gameState = self.getPossibleMoves(
                self.gameState.oldMatrixPosX, self.gameState.oldMatrixPosY, pos)
            self.gameState.isLoad = False
        #Make the move by checking it's legality
        if self.gameState.newMatrixPosX is not None and self.gameState.newMatrixPosY is not None and self.gameState.pieceSelected is not None:
            self.resetBoardGraphics()
            self.moveLegalGO(
                self.gameState.pieceSelected,
                self.gameState.oldMatrixPosX,
                self.gameState.oldMatrixPosY,
                self.gameState.newMatrixPosX,
                self.gameState.newMatrixPosY,
                isPromote)

        dimCollected = 0
        file = open('configure.txt', 'r')
        dimCollected = (file.read().split('\n'))
        file.close()

        # This is for feature collection
        # Moves are pulled to be converted as features
        if dimCollected[2] == '1':
            self.processForTraining2()
            # Convert the pieces into equivalent numbers because training
            # process only uses numbers
            
    #Resets the games board colors 
    #TODO: Phase this out as we move from debug 
    def resetBoardGraphics(self):
        for i in range(0, self.gameState.board_size):
            for j in range(0, self.gameState.board_size):
                self.cells[(i, j)].configure(background='#ffffb1')

    def processForTraining2(self, randomSelection = True):
        #the plan 
        #convert into binary bitmaps
        if (randomSelection):
            randomSelectionValue = random.randint(1,101)
            #Why 5? I like 5... seemed like a low enough chance 
            if (randomSelectionValue < 5):
                    whiteDrops, blackDrops = [], []
                    for dropIndex in range(0, len(self.dropBlacksPieces)):
                        if self.dropBlacksPieces[dropIndex].winfo_manager(
                        ) == 'pack':
                            blackDrops.append(
                                self.dropBlacksPieces[dropIndex].cget('text'))

                    for dropIndex in range(0, len(self.dropWhitePieces)):
                        if self.dropWhitePieces[dropIndex].winfo_manager(
                        ) == 'pack':
                            whiteDrops.append(
                                self.dropWhitePieces[dropIndex].cget('text'))

                    self.gameState.dropBlackPcs = blackDrops
                    self.gameState.dropWhitePcs = whiteDrops

                    while len(whiteDrops) != 19:
                        whiteDrops.append('0')
                    while len(blackDrops) != 19:
                        blackDrops.append('0')

                    rawMatrix = (
                        [y for x in self.gameState.gameMatrix for y in x] + whiteDrops + blackDrops)
                    #Store the numerical encoding into gamestate
                    self.gameState.NumericalEncodingGameState = rawMatrix

                    pcs = ['Wl', 'Wn', 'Ws', 'Wg', 'Wk', 'Wr', 'Wb', 'Wp', 'Bl', 'Bn', 'Bs', 'Bg', 'Bk', 'Br', 'Bb', 'Bp', 'WL', 'WN', 'WS', 'WR', 'WB', 'WP', 'BL', 'BN', 'BS', 'BR', 'BB', 'BP']
                    bitmap = []

                    for pc in pcs: 
                        for x in rawMatrix:
                            if x == pc:
                                bitmap.append(1)
                            else:
                                bitmap.append(0)
                    
                    try:
                        csvObj = csvUtil(self.gameState.loadFile[:-4])
                        csvObj.createCombinedCSV(
                            bitmap, 'training.csv', csvObj.getOriginalFile())
                    except Exception as e:
                        print(e)
                        print('No CSA found, so not generating labels / features')

    def processForTraining1(self):
        whiteDrops, blackDrops = [], []
        for dropIndex in range(0, len(self.dropBlacksPieces)):
            if self.dropBlacksPieces[dropIndex].winfo_manager(
            ) == 'pack':
                blackDrops.append(
                    self.dropBlacksPieces[dropIndex].cget('text'))

        for dropIndex in range(0, len(self.dropWhitePieces)):
            if self.dropWhitePieces[dropIndex].winfo_manager(
            ) == 'pack':
                whiteDrops.append(
                    self.dropWhitePieces[dropIndex].cget('text'))

        self.gameState.dropBlackPcs = blackDrops
        self.gameState.dropWhitePcs = whiteDrops

        while len(whiteDrops) != 19:
            whiteDrops.append('0')
        while len(blackDrops) != 19:
            blackDrops.append('0')

        rawMatrix = (
            [y for x in self.gameState.gameMatrix for y in x] + whiteDrops + blackDrops)
        #Store the numerical encoding into gamestate
        self.gameState.NumericalEncodingGameState = rawMatrix

        pc2num = ''
        file = open('ml/eval_pcs.map', 'r')
        pc2num = (file.read().split('\n'))
        file.close()
        convMatrix = []
        for x in rawMatrix:
            for l in pc2num:
                try:
                    if x[-1:] in l:
                        if x[0] == 'W':
                            convMatrix.append(
                                '-' + l.split('=')[1])
                            break
                        elif x[0] == 'B':
                            convMatrix.append(l.split('=')[1])
                            break
                        elif x[0] == '0':
                            convMatrix.append(l.split('=')[1])
                            break

                except BaseException:
                    if (x == 0):
                        convMatrix.append(0)
                        break
        # When we load a game, we try to generate features and
        # labels
        try:
            csvObj = csvUtil(self.gameState.loadFile[:-4])
            csvObj.createCombinedCSV(
                convMatrix, 'training.csv', csvObj.getOriginalFile())
        except Exception as e:
            print(e)
            print('No CSA found, so not generating labels / features')

    #Cleans the board, resets the variables and changes the turn around
    #For the next player to play
    def SwitchTurns(self):
        self.resetBoardGraphics()
        self.softReset()

        if (self.gameState.isBlackTurn):
            self.turnIndicator.configure(text='White Turn')
            self.gameState.isBlackTurn = False
        else:
            self.turnIndicator.configure(text='Black Turn')
            self.gameState.isBlackTurn = True
    
    #Reset gamestate variables 
    def softReset(self):
        self.gameState.newMatrixPosX = None
        self.gameState.newMatrixPosY = None
        self.gameState.oldMatrixPosX = None
        self.gameState.oldMatrixPosY = None
        self.gameState.pieceSelected = None
        self.gameState.gameState = 0
 
    #Checks the gamematrix to find the position on the matrix
    #Which holds a piece
    def getPosFromPiece(self, pos):
        for i in range(0, self.gameState.board_size):
            for j in range(0, self.gameState.board_size):
                if pos == self.gameState.gameMatrix[i][j]:
                    return i, j
        return None
    #Checks the gamematrix to find the piece on a matrix when given a position
    def getPieceFrmPos(self, h, w):
        return self.gameState.gameMatrix[(h - 1)][(w - 1)]

    #Gets all the possible moves a piece can make
    def getPossibleMoves(self, oldMatrixPosX, oldMatrixPosY, pos):
        if (self.gameState.isBlackTurn and pos[:-1] == 'B') or (
                self.gameState.isBlackTurn == False and pos[:-1] == 'W'):
            with open('movesets.txt') as f:
                content = f.readlines()
                for index in range(len(content)):
                    if pos[-1:] in content[index]:
                        movesets = content[index].split('=')[1]
                        # Cast movesets to array
                        possiblemovelayouts = eval(movesets)
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
                                #Apply the movesets to every position to show the possible moves
                                #And add certain rules to make it correct
                                if ((str(self.getPieceFrmPos(oldMatrixPosX +
                                                             x_dif +
                                                             1, oldMatrixPosY +
                                                             y_dif +
                                                             1))[:-
                                                                 1] == 'B') and self.gameState.isBlackTurn):
                                    break

                                if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[
                                        :-1] == 'W') and self.gameState.isBlackTurn == False):
                                    break
                                
                                #If the move is possible, we should store it to return
                                if ((str(self.getPieceFrmPos(oldMatrixPosX +
                                                             x_dif +
                                                             1, oldMatrixPosY +
                                                             y_dif +
                                                             1))[:-
                                                                 1] != 'B') and self.gameState.isBlackTurn):
                                    self.cells[(
                                        oldMatrixPosX + x_dif, oldMatrixPosY + y_dif)].configure(background='orange')
                                    self.gameState.possibleMoveMatrix.append(
                                        (oldMatrixPosX + x_dif, oldMatrixPosY + y_dif))

                                if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[
                                        :-1] != 'W') and self.gameState.isBlackTurn == False):
                                    self.cells[(
                                        oldMatrixPosX + x_dif, oldMatrixPosY + y_dif)].configure(background='orange')
                                    self.gameState.possibleMoveMatrix.append(
                                        (oldMatrixPosX + x_dif, oldMatrixPosY + y_dif))
                                #If we've hit an opposing piece, we break the loop as we don't need to do anymore 
                                #checking
                                if ((str(self.getPieceFrmPos(oldMatrixPosX +
                                                             x_dif +
                                                             1, oldMatrixPosY +
                                                             y_dif +
                                                             1))[:-
                                                                 1] == 'W') and self.gameState.isBlackTurn):
                                    break

                                if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[
                                        :-1] == 'B') and self.gameState.isBlackTurn == False):
                                    break
                            except:
                                pass
            return 1
        else:
            print('It is not your turn yet')
            return 0 
    #This function checks if the move is a legal move, and if it is, we play it
    #TODO: This function can most certainly broken. Its size is broken and it's deviated from it's original goal
    #Through extension
    def moveLegalGO(
            self,
            pos,
            oldMatrixPosXlocal,
            oldMatrixPosYlocal,
            newMatrixPosXlocal,
            newMatrixPosYlocal,
            isPromote=None):

        #Take a snapshot of the turn prior
        backupgamestateBlackcaptured = self.gameState.blackcaptured 
        backupgamestateWhitecaptured = self.gameState.whitecaptured

        priorCheckCondition = self.CheckIndicator.cget("text")
        # For the game recorder
        resultPromotion = False
        resultCapture = False
        resultDrop = False

        if ((newMatrixPosXlocal, newMatrixPosYlocal)
                ) in self.gameState.possibleMoveMatrix:

            # When recording games... we check who actually made the move
            # Done by checking who can do it, THEN seeing if we need to clear
            # ambiguity
            possiblepcs = []
            for i in range(0, self.gameState.board_size):
                for j in range(0, self.gameState.board_size):
                    p = self.getPieceFrmPos(i + 1, j + 1)
                    if p != 0:
                        possiblepc = self.getPosWhichCanMakeMove(
                            i, j, p, newMatrixPosXlocal + 1, newMatrixPosYlocal + 1)
                        if possiblepc != '':
                            possiblepcs.append(possiblepc)

            # Get current pre-move position we are moving to
            old_state_pos = self.getPieceFrmPos(
                newMatrixPosXlocal + 1, newMatrixPosYlocal + 1)

            # Promotion
            if (self.gameState.isBlackTurn and (
                    newMatrixPosXlocal <= 2 or oldMatrixPosXlocal <= 2) and isPromote != False):
                if (pos[-1:] == 'p' and newMatrixPosXlocal <= 0) or (pos[-1:] == 'n' and newMatrixPosXlocal <=
                                                                     1) or (pos[-1:] == 'l' and newMatrixPosXlocal <= 0) or (isPromote):
                    pos = pos.upper()
                    resultPromotion = True
                else:
                    try:
                        pos, resultPromotion = self.promotion(pos)
                    except BaseException:
                        pass

            if (self.gameState.isBlackTurn == False and (
                    newMatrixPosXlocal >= 6 or oldMatrixPosXlocal >= 6) and isPromote != False):
                if (pos[-1:] == 'p' and newMatrixPosXlocal >= 8) or (pos[-1:] == 'n' and newMatrixPosXlocal >=
                                                                     7) or (pos[-1:] == 'l' and newMatrixPosXlocal >= 8) or (isPromote):
                    pos = pos.upper()
                    resultPromotion = True
                else:
                    try:
                        pos, resultPromotion = self.promotion(pos)
                    except BaseException:
                        pass

            # Capture
            newButton = None
            if (self.gameState.gameMatrix[newMatrixPosXlocal]
                    [newMatrixPosYlocal] != 0):
                print(
                    'Captured: ' +
                    self.gameState.gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal])
                cap_piece = self.gameState.gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal]
               
                if self.gameState.isBlackTurn:
                    self.gameState.blackcaptured.append(
                        'B' + cap_piece[-1:].lower())
                    print(('Adding to black: ' +
                           str(len(self.gameState.blackcaptured))))
                    newButton = Button(
                        self.dropBlacks,
                        highlightcolor="black",
                        bg='#F6A379',
                        height=1,
                        width=1,
                        text='B' + str(
                            self.gameState.gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal]).lower()[
                            -1:],
                        command=lambda row=len(
                            self.gameState.blackcaptured),
                        piece='B': self.clickDrop(
                            row,
                            piece))
                    newButton.pack()
                    self.dropBlacksPieces.append(newButton)
                    resultCapture = True

                if not self.gameState.isBlackTurn:
                    print(('Adding to white: ' +
                           str(len(self.gameState.whitecaptured))))
                    self.gameState.whitecaptured.append(
                        'W' + cap_piece[-1:].lower())
                    newButton = Button(
                        self.dropWhites,
                        highlightcolor="black",
                        bg='#F6A379',
                        height=1,
                        width=1,
                        text='W' + str(
                            self.gameState.gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal]).lower()[
                            -1:],
                        command=lambda row=len(
                            self.gameState.whitecaptured),
                        piece='W': self.clickDrop(
                            row,
                            piece))
                    newButton.pack()
                    self.dropWhitePieces.append(newButton)
                    resultCapture = True



            self.gameState.gameState = 0

            self.gameState.gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal] = pos
            self.gameState.gameMatrix[oldMatrixPosXlocal][oldMatrixPosYlocal] = 0
            self.cells[(oldMatrixPosXlocal, oldMatrixPosYlocal)
                       ].configure(text='')

            # Check for checks
            # This method. Is. perfect.
            #print('CHECK??', self.gameState.isCheck)
            if not self.gameState.isCheck:
                # Does our move reveal a check for the other team?
                self.gameState.isBlackTurn = not self.gameState.isBlackTurn
                for i in range(0, self.gameState.board_size):
                    for j in range(0, self.gameState.board_size):
                        p = self.getPieceFrmPos(i + 1, j + 1)
                        if p != 0:
                            self.isKingUnderCheck(i, j, p)

                            if self.gameState.isCheck:
                                print('ILLEGAL MOVE: Reveals check')
                                self.gameState.AIMessage = 'ILLEGAL'
                                
                                try:
                                    newButton.pack_forget()
                                except:
                                    pass
                                break


                    if self.gameState.isCheck:
                        break
                self.gameState.isBlackTurn = not self.gameState.isBlackTurn

            if not self.gameState.isCheck:
                # Does our move give a check?
                for i in range(0, self.gameState.board_size):
                    for j in range(0, self.gameState.board_size):
                        p = self.getPieceFrmPos(i + 1, j + 1)
                        if p != 0:
                            self.isKingUnderCheck(i, j, p)

            else:
                # Does our move get us out of a check?
                print(
                    'Now that the opponents move has been made, lets check if check is still valid')
                self.gameState.isBlackTurn = not self.gameState.isBlackTurn
                for i in range(0, self.gameState.board_size):
                    for j in range(0, self.gameState.board_size):
                        p = self.getPieceFrmPos(i + 1, j + 1)
                        if p != 0:
                            self.isKingUnderCheck(i, j, p)

                # reminder: [y axis][x axis]
                if self.gameState.isBlackTurn:
                    kingcolor = self.cells[self.getPosFromPiece(
                        'Wk')].cget('background')
                else:
                    kingcolor = self.cells[self.getPosFromPiece(
                        'Bk')].cget('background')

                if (kingcolor == 'cyan'):
                    print('Still in check, Restart that move')
                    old_fill = old_state_pos
                    if old_fill == 0:
                        old_fill = ''

                    print(
                        'Resetting old position: ' +
                        str(old_fill) +
                        ' as move ' +
                        str(pos) +
                        ' is illegal')
                    self.gameState.AIMessage = 'ILLEGAL'
                    try:
                        newButton.pack_forget()
                    except:
                        pass

                    # Load back or direct drop?
                    if (self.gameState.isBlackTurn):
                        self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(
                            text=upsidedown.convChartoUpsideDown(str(old_fill)[-1:]))
                        self.cells[(oldMatrixPosXlocal, oldMatrixPosYlocal)].configure(
                            text=upsidedown.convChartoUpsideDown(str(pos)[-1:]))
                    else:
                        self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(
                            text=str(old_fill)[-1:])
                        self.cells[(oldMatrixPosXlocal, oldMatrixPosYlocal)].configure(
                            text=str(pos)[-1:])

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
            #We set the new position we are moving to as the old piece
            if (self.gameState.isBlackTurn):
                self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)
                           ].configure(text=pos[-1:])
            else:
                self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(
                    text=upsidedown.convChartoUpsideDown(pos[-1:]))

            #Reset game
            #TODO: Check if this a softreset ? Use it here
            self.resetBoardGraphics()

            self.gameState.newMatrixPosX = None
            self.gameState.newMatrixPosY = None
            self.gameState.oldMatrixPosX = None
            self.gameState.oldMatrixPosY = None
            self.gameState.pieceSelected = None

            #We record the move
            if len(possiblepcs) != len(set(possiblepcs)):
                gamerecorder().recordMove(
                    pos,
                    resultPromotion,
                    resultCapture,
                    resultDrop,
                    newMatrixPosYlocal,
                    newMatrixPosXlocal,
                    oldMatrixPosYlocal,
                    oldMatrixPosXlocal)
            else:
                gamerecorder().recordMove(pos, resultPromotion, resultCapture,
                                           resultDrop, newMatrixPosYlocal, newMatrixPosXlocal)
            #Store the current game record
            self.gameState.recordingFile = gamerecorder().getFileRecord()

            #Switch over sides
            if (self.gameState.isBlackTurn):
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

        # Now we check if its a checkmate
        if (self.gameState.isCheck):

            # Get all of your available moves
            print('JUDGE: Checking if it is a checkmate')
            for i in range(0, self.gameState.board_size):
                for j in range(0, self.gameState.board_size):
                    self.populateSimulMoveArrays(
                        i, j, str(self.gameState.gameMatrix[i][j]), True)

            for i in range(0, len(self.simulMoveMatrix)):
                if (
                    self.simulateMove(
                        self.simulMoveMatrixPre[i][0],
                        self.simulMoveMatrixPre[i][1],
                        self.simulMoveMatrixPre[i][2],
                        self.simulMoveMatrix[i][0],
                        self.simulMoveMatrix[i][1],
                        i) == False):
                    break

            if i == (len(self.simulMoveMatrix) - 1):
                # Check if we can drop a piece to cover the check

                if not self.gameState.isBlackTurn:
                    potentialThreatPcsAr = self.checkDistanceThreats(
                        self.getPosFromPiece('Wk')[0], self.getPosFromPiece('Wk')[1], 'Wb')
                    potentialThreatPcsAr = potentialThreatPcsAr + self.checkDistanceThreats(
                        self.getPosFromPiece('Wk')[0], self.getPosFromPiece('Wk')[1], 'Wr')

                if self.gameState.isBlackTurn:
                    potentialThreatPcsAr = self.checkDistanceThreats(
                        self.getPosFromPiece('Bk')[0], self.getPosFromPiece('Bk')[1], 'Bb')
                    potentialThreatPcsAr = potentialThreatPcsAr + self.checkDistanceThreats(
                        self.getPosFromPiece('Bk')[0], self.getPosFromPiece('Bk')[1], 'Br')

                print(potentialThreatPcsAr)
                if len(potentialThreatPcsAr) > 1:
                    print('RESULT: Checkmate! GAMEOVER')
                    self.CheckIndicator.configure(text='Checkmate')
                else:
                    # Alright, so there is a move and only one threat
                    # We can block. Right?

                    dropAvailable = False
                    # Get available drop pcs
                    if not self.gameState.isBlackTurn:
                        dropPcs = []
                        for rank in range(0, len(self.dropWhitePieces)):
                            if self.dropWhitePieces[rank].winfo_manager(
                            ) == 'pack':
                                dropPcs.append(
                                    self.dropWhitePieces[rank].cget('text'))

                        print(dropPcs)
                        for potentialThreats in potentialThreatPcsAr:
                            if ('Wp' in dropPcs):
                                if ((self.getPosFromPiece('Wk')[
                                        0] != 0) and potentialThreats[1] != 0):
                                    print('No white pawn here!')
                                else:
                                    poissiblePawnDrops = (
                                        list(
                                            range(
                                                self.getPosFromPiece('Wk')[1],
                                                potentialThreats[2])))
                                    for horiz in range(0, 9):
                                        for ver in range(0, 9):
                                            if (
                                                    self.gameState.gameMatrix[ver][horiz]) == 'Wp':
                                                if horiz in poissiblePawnDrops:
                                                    poissiblePawnDrops.remove(
                                                        horiz)

                                    if len(poissiblePawnDrops) == 0:
                                        filepcs = []
                                        for ver in range(0, 9):
                                            filepcs.append(
                                                self.gameState.gameMatrix[ver][self.getPosFromPiece('Wk')[1]])
                                        if ('Wp' in filepcs):
                                            print(
                                                'No white pawn can be dropped here')
                                        else:
                                            print('A white pawn can be played')
                                            dropAvailable = True
                                            break
                                    else:
                                        print('A white pawn can be played')
                                        dropAvailable = True
                                        break
                            else:
                                print('No white pawns are available')

                            if ('Wn' in dropPcs):
                                if ((self.getPosFromPiece('Wk')[
                                        0] <= 1) and potentialThreats[1] <= 1):
                                    print('No white knight here!')
                                else:
                                    print('A white knight can be played')
                                    dropAvailable = True
                                    break
                            else:
                                print('No white knights are available')

                            if ('Wl' in dropPcs):
                                if ((self.getPosFromPiece('Wk')[
                                        0] != 0) and potentialThreats[1] != 0):
                                    print('No white lance here!')
                                else:
                                    print('A white lance can be played')
                                    dropAvailable = True
                                    break
                            else:
                                print('No white lance are available')
                        
                            if ('Wb' in dropPcs or 'Wr' in dropPcs):
                                dropAvailable = True
                                break

                        if dropAvailable:
                            print('Moves available. Continue play.')
                        else:
                            print('RESULT: Checkmate! GAMEOVER')
                            self.CheckIndicator.configure(text='Checkmate')

                    else:
                        dropPcs = []
                        for rank in range(0, len(self.dropBlacksPieces)):
                            if self.dropBlacksPieces[rank].winfo_manager(
                            ) == 'pack':
                                dropPcs.append(
                                    self.dropBlacksPieces[rank].cget('text'))

                        print(dropPcs)
                        for potentialThreats in potentialThreatPcsAr:
                            if ('Bp' in dropPcs):
                                if ((self.getPosFromPiece('Bk')[
                                        0] != 0) and potentialThreats[1] != 0):
                                    print('No black pawn here!')
                                else:
                                    poissiblePawnDrops = (
                                        list(
                                            range(
                                                self.getPosFromPiece('Bk')[1],
                                                potentialThreats[2])))
                                    for horiz in range(0, 9):
                                        for ver in range(0, 9):
                                            if (
                                                    self.gameState.gameMatrix[ver][horiz]) == 'Bp':
                                                if horiz in poissiblePawnDrops:
                                                    poissiblePawnDrops.remove(
                                                        horiz)

                                    if len(poissiblePawnDrops) == 0:
                                        filepcs = []
                                        for ver in range(0, 9):
                                            filepcs.append(
                                                self.gameState.gameMatrix[ver][self.getPosFromPiece('Bk')[1]])
                                        if ('Bp' in filepcs):
                                            print(
                                                'No black pawn can be dropped here')
                                        else:
                                            print('A black pawn can be played')
                                            dropAvailable = True
                                            break
                                    else:
                                        print('A black pawn can be played')
                                        dropAvailable = True
                                        break
                            else:
                                print('No black pawns are available')

                            if ('Bn' in dropPcs):
                                if ((self.getPosFromPiece('Bk')[
                                        0] <= 1) and potentialThreats[1] <= 1):
                                    print('No black knight here!')
                                else:
                                    print('A black knight can be played')
                                    dropAvailable = True
                                    break
                            else:
                                print('No black knights are available')

                            if ('Bl' in dropPcs):
                                if ((self.getPosFromPiece('Bk')[
                                        0] != 0) and potentialThreats[1] != 0):
                                    print('No black lance here!')
                                else:
                                    print('A black lance can be played')
                                    dropAvailable = True
                                    break
                            else:
                                print('No black lance are available')

                            if ('Bb' in dropPcs or 'Br' in dropPcs):
                                dropAvailable = True
                                break

                        #We check if we can drop a piece to block the check
                        if dropAvailable:
                            print('Moves available. Continue play.')
                        else:
                            print('RESULT: Checkmate! GAMEOVER')
                            self.CheckIndicator.configure(text='Checkmate')

            self.simulMoveMatrixPre *= 0
            self.simulMoveMatrix *= 0

        # get raw numerical encoding
        whiteDrops, blackDrops = [], []
        for dropIndex in range(0, len(self.dropBlacksPieces)):
            if self.dropBlacksPieces[dropIndex].winfo_manager() == 'pack':
                blackDrops.append(
                    self.dropBlacksPieces[dropIndex].cget('text'))

        for dropIndex in range(0, len(self.dropWhitePieces)):
            if self.dropWhitePieces[dropIndex].winfo_manager() == 'pack':
                whiteDrops.append(self.dropWhitePieces[dropIndex].cget('text'))

        while len(whiteDrops) != 19:
            whiteDrops.append('0')
        while len(blackDrops) != 19:
            blackDrops.append('0')

        if (priorCheckCondition == 'Black Check') or (priorCheckCondition == 'White Check'):
            self.CheckIndicator.configure(text='No Check')

        rawMatrix = (
            [y for x in self.gameState.gameMatrix for y in x] + whiteDrops + blackDrops)
        #Store it for the AI player
        self.gameState.NumericalEncodingGameState = rawMatrix

    #Get the character to sub in
    def getTeamCharacter(self):
        if self.gameState.isBlackTurn:
            return 'B'
        else:
            return 'W'
    
    #This function checks which pieces can move to that spot
    #V useful for interpreting the classic shogi notation
    def getPosWhichCanMakeMove(
            self,
            oldMatrixPosX,
            oldMatrixPosY,
            pos,
            newMatrixPosX,
            newMatrixPosY):
        if (self.gameState.isBlackTurn and pos[:-1] == 'B') or (
                self.gameState.isBlackTurn == False and pos[:-1] == 'W'):
            with open('movesets.txt') as f:
                content = f.readlines()
                for index in range(len(content)):
                    if pos[-1:] in content[index]:
                        movesets = content[index].split('=')[1]
                        # cast movesets to array
                        possiblemovelayouts = eval(movesets)
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
                                if ((str(self.getPieceFrmPos(oldMatrixPosX +
                                                             x_dif +
                                                             1, oldMatrixPosY +
                                                             y_dif +
                                                             1))[:-
                                                                 1] == 'B') and self.gameState.isBlackTurn):
                                    break

                                if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[
                                        :-1] == 'W') and self.gameState.isBlackTurn == False):
                                    break

                                if ((oldMatrixPosX + x_dif + 1 == newMatrixPosX)
                                        and (oldMatrixPosY + y_dif + 1 == newMatrixPosY)):
                                    self.cells[(
                                        oldMatrixPosX + x_dif, oldMatrixPosY + y_dif)].configure(background='red')
                                    return pos

                                if ((str(self.getPieceFrmPos(oldMatrixPosX +
                                                             x_dif +
                                                             1, oldMatrixPosY +
                                                             y_dif +
                                                             1))[:-
                                                                 1] == 'W') and self.gameState.isBlackTurn):
                                    break

                                if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[
                                        :-1] == 'B') and self.gameState.isBlackTurn == False):
                                    break

                            except Exception as e:
                                pass
            return ''
        else:
            return ''

    #This checks whether the King is under check
    def isKingUnderCheck(self, oldMatrixPosX, oldMatrixPosY, pos):

        if (self.gameState.isBlackTurn and pos[:-1] == 'B') or (
                self.gameState.isBlackTurn == False and pos[:-1] == 'W'):
            with open('movesets.txt') as f:
                content = f.readlines()
                for index in range(len(content)):
                    if pos[-1:] in content[index]:
                        movesets = content[index].split('=')[1]
                        # cast movesets to array
                        possiblemovelayouts = eval(movesets)
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
                                    if ((str(self.getPieceFrmPos(oldMatrixPosX +
                                                                 x_dif +
                                                                 1, oldMatrixPosY +
                                                                 y_dif +
                                                                 1))[:-
                                                                     1] == 'B') and self.gameState.isBlackTurn):
                                        break

                                    if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[
                                            :-1] == 'W') and self.gameState.isBlackTurn == False):
                                        break

                                    if ((str(self.getPieceFrmPos(oldMatrixPosX +
                                                                 x_dif +
                                                                 1, oldMatrixPosY +
                                                                 y_dif +
                                                                 1))[:-
                                                                     1] != 'B') and self.gameState.isBlackTurn):
                                        if str(
                                            self.getPieceFrmPos(
                                                oldMatrixPosX + x_dif + 1,
                                                oldMatrixPosY + y_dif + 1)) == 'Wk':
                                            print('BLACK CHECK!')
                                            self.CheckIndicator.configure(text='Black Check')

                                            self.gameState.isCheck = True

                                        self.cells[(
                                            oldMatrixPosX + x_dif, oldMatrixPosY + y_dif)].configure(background='cyan')

                                    if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[
                                            :-1] != 'W') and self.gameState.isBlackTurn == False):
                                        if str(
                                            self.getPieceFrmPos(
                                                oldMatrixPosX + x_dif + 1,
                                                oldMatrixPosY + y_dif + 1)) == 'Bk':
                                            print('WHITE CHECK!')
                                            self.CheckIndicator.configure(text='White Check')

                                            self.gameState.isCheck = True

                                        self.cells[(
                                            oldMatrixPosX + x_dif, oldMatrixPosY + y_dif)].configure(background='cyan')

                                    if ((str(self.getPieceFrmPos(oldMatrixPosX +
                                                                 x_dif +
                                                                 1, oldMatrixPosY +
                                                                 y_dif +
                                                                 1))[:-
                                                                     1] == 'W') and self.gameState.isBlackTurn):
                                        break

                                    if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[
                                            :-1] == 'B') and self.gameState.isBlackTurn == False):
                                        break

                            except Exception as e:
                                pass

            return 1
        else:
            return 0

    #This checks whether the King has been checked by a piece far from it
    def checkDistanceThreats(self, oldMatrixPosX, oldMatrixPosY, pos):
        potentialThreatPcsArr = []
        if (self.gameState.isBlackTurn and pos[:-1] == 'B') or (
                self.gameState.isBlackTurn == False and pos[:-1] == 'W'):
            with open('movesets.txt') as f:
                content = f.readlines()

                for index in range(len(content)):
                    if pos[-1:] in content[index]:
                        movesets = content[index].split('=')[1]
                        # cast movesets to array
                        possiblemovelayouts = eval(movesets)

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
                                # If the piece is Black and youre black, stop
                                if ((str(self.getPieceFrmPos(oldMatrixPosX +
                                                             x_dif +
                                                             1, oldMatrixPosY +
                                                             y_dif +
                                                             1))[:-
                                                                 1] == 'B') and self.gameState.isBlackTurn):
                                    break

                                # If the piece is White and youre White, stop
                                if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[
                                        :-1] == 'W') and self.gameState.isBlackTurn == False):
                                    break

                                # If the piece is White and youre Black, you
                                # can capture so color
                                if ((str(self.getPieceFrmPos(oldMatrixPosX +
                                                             x_dif +
                                                             1, oldMatrixPosY +
                                                             y_dif +
                                                             1))[:-
                                                                 1] != 'B') and self.gameState.isBlackTurn):
                                    if (self.gameState.isBlackTurn == False and (self.cells[(
                                            oldMatrixPosX + x_dif, oldMatrixPosY + y_dif)].cget('background')) == 'blue'):
                                        pass
                                    else:
                                        self.cells[(
                                            oldMatrixPosX + x_dif, oldMatrixPosY + y_dif)].configure(background='blue')
                                        pc = (
                                            self.gameState.gameMatrix[oldMatrixPosX + x_dif][oldMatrixPosY + y_dif])

                                        if ('r' == pc[-1]) or ('R' == pc[-1]
                                                               ) or ('b' == pc[-1]) or ('B' == pc[-1]):
                                            potentialThreatPcsArr.append(
                                                str(pc))

                                # If the piece is Black and youre White, you
                                # can capture so color
                                if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[
                                        :-1] != 'W') and self.gameState.isBlackTurn == False):
                                    if (self.gameState.isBlackTurn == False and (self.cells[(oldMatrixPosX + x_dif, oldMatrixPosY + y_dif)].cget('background')) == 'pink') or (
                                            self.gameState.isBlackTurn == True and 'k' in pos and (self.cells[(oldMatrixPosX + x_dif, oldMatrixPosY + y_dif)].cget('background')) == 'pink'):
                                        pass
                                    else:
                                        self.cells[(
                                            oldMatrixPosX + x_dif, oldMatrixPosY + y_dif)].configure(background='blue')
                                        pc = (
                                            self.gameState.gameMatrix[oldMatrixPosX + x_dif][oldMatrixPosY + y_dif])

                                        if ('r' == pc[-1]) or ('R' == pc[-1]
                                                               ) or ('b' == pc[-1]) or ('B' == pc[-1]):
                                            potentialThreatPcsArr.append(
                                                [str(pc), oldMatrixPosX + x_dif, oldMatrixPosY + y_dif])

                                if ((str(self.getPieceFrmPos(oldMatrixPosX +
                                                             x_dif +
                                                             1, oldMatrixPosY +
                                                             y_dif +
                                                             1))[:-
                                                                 1] == 'W') and self.gameState.isBlackTurn and (str(self.getPieceFrmPos(oldMatrixPosX +
                                                                                                                                        x_dif +
                                                                                                                                        1, oldMatrixPosY +
                                                                                                                                        y_dif +
                                                                                                                                        1))[1:] != 'k')):
                                    break

                                if ((str(self.getPieceFrmPos(oldMatrixPosX +
                                                             x_dif +
                                                             1, oldMatrixPosY +
                                                             y_dif +
                                                             1))[:-
                                                                 1] == 'B') and self.gameState.isBlackTurn == False and (str(self.getPieceFrmPos(oldMatrixPosX +
                                                                                                                                                 x_dif +
                                                                                                                                                 1, oldMatrixPosY +
                                                                                                                                                 y_dif +
                                                                                                                                                 1))[1:] != 'k')):
                                    break

                            except Exception as e:
                                pass
            return potentialThreatPcsArr
        else:
            return 0

    #Handles promotion mechanics by letting the user select if they want to promote
    def promotion(self, pos):
        self.gameState.isPromotionMessageActive = True
        if not self.gameState.isLoad:
            if 'g' not in pos and 'k' not in pos and pos[-1:].islower():
                MsgBox = messagebox.askquestion(
                    "Promotion!",
                    "You have reached promotion. Would you like to promote your piece?")
                if MsgBox == 'yes':
                    self.gameState.isPromotionMessageActive = False
                    return pos.upper(), True
                else:
                    self.gameState.isPromotionMessageActive = False
                    return pos, False
            self.gameState.isPromotionMessageActive = False
            return pos, False
        else:
            #If we are loading a promotion move, we don't really give a choice
            self.gameState.isPromotionMessageActive = False
            file = open('ext_data/movetoplay.txt', 'r')
            print(file.read())

    def clickDrop(self, row, piece):

        print(('DROPPING: ', row, piece))

        with open('configure.txt') as f:
            configContent = f.readlines()
        dropSetting = int(configContent[1])

        if (dropSetting == 0):

            if (self.gameState.isBlackTurn and 'B' in piece) or (
                    self.gameState.isBlackTurn == False and 'W' in piece):
                self.gameState.droprank = row - 1
                self.gameState.gameState = 3
            else:
                print('You can not drop your opponents pieces')
                self.resetBoardGraphics()
                self.gameState.gameState = 0

    #Same as move legal, but it is tuned for drops
    def moveLegalDrop(self, pos, newMatrixPosXlocal, newMatrixPosYlocal):
        # Get current pre-move position we are moving to
        old_state_pos = self.getPieceFrmPos(
            newMatrixPosXlocal + 1, newMatrixPosYlocal + 1)
        print(old_state_pos)

        # For the game recorder
        resultPromotion = False
        resultCapture = False
        resultDrop = True

        # No Capturing or Promotion
        self.gameState.gameState = 0

        self.gameState.gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal] = pos

        # Check for checks
        # This method. Is. perfect.
        if not self.gameState.isCheck:
            # Does our move reveal a check for the other team?
            self.gameState.isBlackTurn = not self.gameState.isBlackTurn
            for i in range(0, self.gameState.board_size):
                for j in range(0, self.gameState.board_size):
                    p = self.getPieceFrmPos(i + 1, j + 1)
                    if p != 0:
                        self.isKingUnderCheck(i, j, p)

                        if self.gameState.isCheck:
                            print('ILLEGAL MOVE: Reveals check')
                            self.gameState.AIMessage = 'ILLEGAL'
                            break

                if self.gameState.isCheck:
                    break
            self.gameState.isBlackTurn = not self.gameState.isBlackTurn

        if not self.gameState.isCheck:
            # Does our move give a check?
            for i in range(0, self.gameState.board_size):
                for j in range(0, self.gameState.board_size):
                    p = self.getPieceFrmPos(i + 1, j + 1)
                    if p != 0:
                        self.isKingUnderCheck(i, j, p)

        else:
            # Does our move get us out of a check?
            print(
                'Now that the opponents move has been made, lets check if check is still valid')
            self.gameState.isBlackTurn = not self.gameState.isBlackTurn
            for i in range(0, self.gameState.board_size):
                for j in range(0, self.gameState.board_size):
                    p = self.getPieceFrmPos(i + 1, j + 1)
                    if p != 0:
                        self.isKingUnderCheck(i, j, p)

            # reminder: [y axis][x axis]
            if self.gameState.isBlackTurn:
                kingcolor = self.cells[self.getPosFromPiece(
                    'Wk')].cget('background')
            else:
                kingcolor = self.cells[self.getPosFromPiece(
                    'Bk')].cget('background')

            if (kingcolor == 'cyan'):
                print('Still in check, Restart that move')
                old_fill = old_state_pos
                if old_fill == 0:
                    old_fill = ''

                print(
                    'Resetting old position: ' +
                    str(old_fill) +
                    ' as move ' +
                    str(pos) +
                    ' is illegal')
                self.gameState.AIMessage = 'ILLEGAL'
                # Load back or direct drop?
                if (self.gameState.isBlackTurn):
                    self.cells[(newMatrixPosXlocal,
                                newMatrixPosYlocal)].configure(text='')
                else:
                    self.cells[(newMatrixPosXlocal,
                                newMatrixPosYlocal)].configure(text='')
                #Reset 
                self.gameState.isBlackTurn = not self.gameState.isBlackTurn
                self.gameState.gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal] = old_state_pos
                self.resetBoardGraphics()

                self.softReset()

                return

            else:
                print('King is out of check, continue play')
                self.gameState.isCheck = False
                self.gameState.isBlackTurn = not self.gameState.isBlackTurn

        if (self.gameState.isBlackTurn):
            self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)
                       ].configure(text=pos[-1:])
        else:
            self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(
                text=upsidedown.convChartoUpsideDown(pos[-1:]))

        self.resetBoardGraphics()

        self.softReset()

        if (self.gameState.isBlackTurn):
            self.turnIndicator.configure(text='White Turn')
            self.gameState.isBlackTurn = False
        else:
            self.turnIndicator.configure(text='Black Turn')
            self.gameState.isBlackTurn = True
        #Record move
        gamerecorder().recordMove(
            pos,
            resultPromotion,
            resultCapture,
            resultDrop,
            newMatrixPosYlocal,
            newMatrixPosXlocal)

        self.gameState.possibleMoveMatrix *= 0

        # Now we check if its a checkmate
        if (self.gameState.isCheck):

            # Get all of your available moves

            resetMatrix = copy.deepcopy(self.gameState.gameMatrix)
            for i in range(0, self.gameState.board_size):
                for j in range(0, self.gameState.board_size):
                    self.populateSimulMoveArrays(
                        i, j, str(self.gameState.gameMatrix[i][j]), True)

            for i in range(0, len(self.simulMoveMatrix)):
                if (
                    self.simulateMove(
                        self.simulMoveMatrixPre[i][0],
                        self.simulMoveMatrixPre[i][1],
                        self.simulMoveMatrixPre[i][2],
                        self.simulMoveMatrix[i][0],
                        self.simulMoveMatrix[i][1],
                        i) == False):
                    break
                if i == (len(self.simulMoveMatrix) - 1):
                    if ('p' not in pos):
                        print('Checkmate!')
                        self.CheckIndicator.configure(text='Checkmate')
                    else:
                        print('You can not check mate by dropping a pawn')
                        old_fill = old_state_pos
                        if old_fill == 0:
                            old_fill = ''

                        print(
                            'Resetting old position: ' +
                            str(old_fill) +
                            ' as move ' +
                            str(pos) +
                            ' is illegal')
                        self.gameState.AIMessage = 'ILLEGAL'
                        # Load back or direct drop?
                        if (self.gameState.isBlackTurn):
                            self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(
                                text='')
                        else:
                            self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(
                                text='')

                            #self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(text=upsidedown.convChartoUpsideDown(pos[-1:]))
                        self.gameState.isBlackTurn = not self.gameState.isBlackTurn
                        self.gameState.gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal] = old_state_pos
                        self.resetBoardGraphics()

                        self.softReset()

                        return

            self.simulMoveMatrixPre *= 0
            self.simulMoveMatrix *= 0
    
    #When checking if we can escape a check, we should simulate all the possible moves
    #This function handles that and checks if a check is escapable
    def populateSimulMoveArrays(self, oldMatrixPosX, oldMatrixPosY, pos, Turn):

        if (self.gameState.isBlackTurn and pos[:-1] == 'B') or (
                self.gameState.isBlackTurn == False and pos[:-1] == 'W'):
            with open('movesets.txt') as f:
                content = f.readlines()

                for index in range(len(content)):
                    if pos[-1:] in content[index]:
                        movesets = content[index].split('=')[1]
                        # cast movesets to array
                        possiblemovelayouts = eval(movesets)

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
                                # If the piece is Black and youre black, stop
                                if ((str(self.getPieceFrmPos(oldMatrixPosX +
                                                             x_dif +
                                                             1, oldMatrixPosY +
                                                             y_dif +
                                                             1))[:-
                                                                 1] == 'B') and self.gameState.isBlackTurn):
                                    break

                                # If the piece is White and youre White, stop
                                if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[
                                        :-1] == 'W') and self.gameState.isBlackTurn == False):
                                    break

                                # If the piece is White and youre Black, you
                                # can capture so color
                                if ((str(self.getPieceFrmPos(oldMatrixPosX +
                                                             x_dif +
                                                             1, oldMatrixPosY +
                                                             y_dif +
                                                             1))[:-
                                                                 1] != 'B') and self.gameState.isBlackTurn):
                                    if (Turn == False and (self.cells[(
                                            oldMatrixPosX + x_dif, oldMatrixPosY + y_dif)].cget('background')) == 'blue'):
                                        pass
                                    else:
                                        self.cells[(
                                            oldMatrixPosX + x_dif, oldMatrixPosY + y_dif)].configure(background='pink')
                                        self.simulMoveMatrixPre.append(
                                            (oldMatrixPosX, oldMatrixPosY, pos))
                                        self.simulMoveMatrix.append(
                                            (oldMatrixPosX + x_dif, oldMatrixPosY + y_dif, pos))

                                # If the piece is Black and youre White, you
                                # can capture so color
                                if ((str(self.getPieceFrmPos(oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1))[
                                        :-1] != 'W') and self.gameState.isBlackTurn == False):
                                    if (Turn == False and (self.cells[(oldMatrixPosX + x_dif, oldMatrixPosY + y_dif)].cget('background')) == 'pink') or (
                                            Turn == True and 'k' in pos and (self.cells[(oldMatrixPosX + x_dif, oldMatrixPosY + y_dif)].cget('background')) == 'pink'):
                                        pass
                                    else:
                                        self.cells[(
                                            oldMatrixPosX + x_dif, oldMatrixPosY + y_dif)].configure(background='blue')
                                        self.simulMoveMatrixPre.append(
                                            (oldMatrixPosX, oldMatrixPosY, pos))
                                        self.simulMoveMatrix.append(
                                            (oldMatrixPosX + x_dif, oldMatrixPosY + y_dif, pos))

                                if ((str(self.getPieceFrmPos(oldMatrixPosX +
                                                             x_dif +
                                                             1, oldMatrixPosY +
                                                             y_dif +
                                                             1))[:-
                                                                 1] == 'W') and self.gameState.isBlackTurn and (str(self.getPieceFrmPos(oldMatrixPosX +
                                                                                                                                        x_dif +
                                                                                                                                        1, oldMatrixPosY +
                                                                                                                                        y_dif +
                                                                                                                                        1))[1:] != 'k')):
                                    break

                                if ((str(self.getPieceFrmPos(oldMatrixPosX +
                                                             x_dif +
                                                             1, oldMatrixPosY +
                                                             y_dif +
                                                             1))[:-
                                                                 1] == 'B') and self.gameState.isBlackTurn == False and (str(self.getPieceFrmPos(oldMatrixPosX +
                                                                                                                                                 x_dif +
                                                                                                                                                 1, oldMatrixPosY +
                                                                                                                                                 y_dif +
                                                                                                                                                 1))[1:] != 'k')):
                                    break

                            except Exception as e:
                                pass

            # Now we check if we have any drops. We only take the 8 squares
            # surrounding the king as those are the ones that matter anyways.
            return 1
        else:
            return 0

    def simulateMove(
            self,
            oldMatrixPosXlocal,
            oldMatrixPosYlocal,
            pos,
            newMatrixPosXlocal,
            newMatrixPosYlocal,
            iteration):
        # Get current pre-move position we are moving to
        old_state_pos = self.getPieceFrmPos(
            newMatrixPosXlocal + 1, newMatrixPosYlocal + 1)

        self.gameState.gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal] = pos
        self.gameState.gameMatrix[oldMatrixPosXlocal][oldMatrixPosYlocal] = 0
        self.cells[(oldMatrixPosXlocal, oldMatrixPosYlocal)].configure(text='')

        # Check for checks
        # This method. Is. perfect.
        if not self.gameState.isCheck:
            # Does our move reveal a check for the other team?
            self.gameState.isBlackTurn = not self.gameState.isBlackTurn
            for i in range(0, self.gameState.board_size):
                for j in range(0, self.gameState.board_size):
                    p = self.getPieceFrmPos(i + 1, j + 1)
                    if p != 0:
                        self.isKingUnderCheck(i, j, p)

                        if self.gameState.isCheck:
                            print('ILLEGAL MOVE: Reveals check')
                            self.gameState.AIMessage = 'ILLEGAL'
                            break

                if self.gameState.isCheck:
                    break
            self.gameState.isBlackTurn = not self.gameState.isBlackTurn

        if not self.gameState.isCheck:
            # Does our move give a check?
            for i in range(0, self.gameState.board_size):
                for j in range(0, self.gameState.board_size):
                    p = self.getPieceFrmPos(i + 1, j + 1)
                    if p != 0:
                        self.isKingUnderCheck(i, j, p)

        else:
            # Does our move get us out of a check?
            print(
                'Now that the opponents move has been made, lets check if check is still valid')
            self.gameState.isBlackTurn = not self.gameState.isBlackTurn
            for i in range(0, self.gameState.board_size):
                for j in range(0, self.gameState.board_size):
                    p = self.getPieceFrmPos(i + 1, j + 1)
                    if p != 0:
                        self.isKingUnderCheck(i, j, p)

            # reminder: [y axis][x axis]
            if self.gameState.isBlackTurn:
                kingcolor = self.cells[self.getPosFromPiece(
                    'Wk')].cget('background')
            else:
                kingcolor = self.cells[self.getPosFromPiece(
                    'Bk')].cget('background')

            if (kingcolor == 'cyan'):
                print('Still in check, Restart that move')
                old_fill = old_state_pos
                if old_fill == 0:
                    old_fill = ''

                print(
                    'Resetting old position: ' +
                    str(old_fill) +
                    ' as move ' +
                    str(pos) +
                    ' is illegal')
                self.gameState.AIMessage = 'ILLEGAL'
                # Load back or direct drop?
                if (self.gameState.board_size):
                    self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(
                        text=upsidedown.convChartoUpsideDown(str(old_fill)[-1:]))
                    self.cells[(oldMatrixPosXlocal, oldMatrixPosYlocal)].configure(
                        text=upsidedown.convChartoUpsideDown(str(pos)[-1:]))
                else:
                    self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(
                        text=str(old_fill)[-1:])
                    self.cells[(oldMatrixPosXlocal, oldMatrixPosYlocal)].configure(
                        text=str(pos)[-1:])

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

                if (self.gameState.isBlackTurn):
                    self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(
                        text=upsidedown.convChartoUpsideDown(str(old_fill)[-1:]))
                    self.cells[(oldMatrixPosXlocal, oldMatrixPosYlocal)].configure(
                        text=upsidedown.convChartoUpsideDown(str(pos)[-1:]))
                else:
                    self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(
                        text=str(old_fill)[-1:])
                    self.cells[(oldMatrixPosXlocal, oldMatrixPosYlocal)].configure(
                        text=str(pos)[-1:])

                self.gameState.isBlackTurn = not self.gameState.isBlackTurn
                self.gameState.gameMatrix[newMatrixPosXlocal][newMatrixPosYlocal] = old_state_pos
                self.gameState.gameMatrix[oldMatrixPosXlocal][oldMatrixPosYlocal] = pos
                self.resetBoardGraphics()

                self.softReset()

                print('King is out of check, continue play')
                self.gameState.isCheck = False
                return False

        if (self.gameState.isBlackTurn):
            self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)
                       ].configure(text=pos[-1:])
        else:
            self.cells[(newMatrixPosXlocal, newMatrixPosYlocal)].configure(
                text=upsidedown.convChartoUpsideDown(pos[-1:]))
        #Reset
        self.resetBoardGraphics()

        self.gameState.newMatrixPosX = None
        self.gameState.newMatrixPosY = None
        self.gameState.oldMatrixPosX = None
        self.gameState.oldMatrixPosY = None
        self.gameState.pieceSelected = None

        if (self.gameState.isBlackTurn):
            self.turnIndicator.configure(text='White Turn')
            self.gameState.isBlackTurn = False
        else:
            self.turnIndicator.configure(text='Black Turn')
            self.gameState.isBlackTurn = True

        self.gameState.possibleMoveMatrix *= 0
        return False

#This file is an abstraction of the AI agent
#It passes game data to the model, which returns the move to play
class AI_watcher(Thread, spem, logic):
    def __init__(
            self,
            event,
            gameState,
            cells,
            turnIndicator,
            dropBlacks,
            dropWhites,
            dropBlacksPieces,
            dropWhitePieces,
            CheckIndicator):
        Thread.__init__(self)
        self.stopped = event
        self.gameState = gameState
        self.cells = cells
        self.turnIndicator = turnIndicator
        self.dropBlacks = dropBlacks
        self.dropWhites = dropWhites
        self.dropBlacksPieces = dropBlacksPieces
        self.dropWhitePieces = dropWhitePieces
        self.simulMoveMatrix = []
        self.simulMoveMatrixPre = []
        self.CheckIndicator = CheckIndicator

        f = open('ext_data/load_game.txt', 'r+')
        f.truncate(0)
        f.close()
        f = open('ext_data/movetoplay.txt', 'r+')
        f.truncate(0)
        f.close()
    
    def getPlayersColor(self):
        if (self.gameState.playerSelected == 'Black'):
            return True
        else:
            return False
    def resetPotentialMovePositions(self):
        print('Clearing moveposition')
        csvObj = csvUtil()
        csvObj.createHeaders('ml/pharoah2/moveposition.csv')

    def run(self):
        while not self.stopped.wait(5):
            # Grab record sheet so far...
            try:
                illegalMoveList = []
                self.resetPotentialMovePositions()
                if (self.gameState.isBlackTurn != self.getPlayersColor()):
                    #Reset the potential moves
                    dropBlackState = []
                    dropWhiteState = []
                    try:
                        dropBlackState = list(filter(('0').__ne__, self.gameState.dropBlackPcs))
                    except:
                        pass
                    try:
                       dropWhiteState = list(filter(('0').__ne__, self.gameState.dropWhitePcs))
                    except:
                        pass
                    self.gameState.AIMessage = 'LEGAL'

                    while True:
                        mg = moveGeneration()
                        moveToPlay, moveToCheck = mg.GenMoves(
                                self.gameState.gameMatrix,
                                not self.getPlayersColor(), dropBlackState,
                                    dropWhiteState, illegalMoveList)                                 
                                                                 
                        print('MOVE TO PLAY IS:', moveToPlay)
                        mg.writeMoveToBuffer(moveToPlay, "ext_data/movetoplay.txt")
                        self.gameState.AIMessage = 'LEGAL'
                        print('Checking if a move is loaded by the AI')
                        if os.stat("ext_data/movetoplay.txt").st_size != 0:
                            print('There is a move! Let us load it')
                            logic.PlayAIMove(self)
                            f = open('ext_data/load_game.txt', 'r+')
                            f.truncate(0)
                            f.close()
                            f = open('ext_data/movetoplay.txt', 'r+')
                            f.truncate(0)
                            f.close()
                            
                        
                        if self.gameState.AIMessage == 'ILLEGAL':
                            illegalMoveList.append(moveToCheck)
                        else:
                            self.gameState.AIMessage == 'LEGAL'
                            break
                 


                '''
                elif (self.gameState.isBlackTurn == self.getPlayersColor()):
                    #Reset the potential moves
                    dropBlackState = []
                    dropWhiteState = []
                    try:
                        dropBlackState = list(filter(('0').__ne__, self.gameState.dropBlackPcs))
                    except:
                        pass
                    try:
                       dropWhiteState = list(filter(('0').__ne__, self.gameState.dropWhitePcs))
                    except:
                        pass
                    self.gameState.AIMessage = 'LEGAL'

                    while True:
                        mg = moveGeneration()
                        moveToPlay, moveToCheck = mg.GenMoves(
                                self.gameState.gameMatrix,
                                self.getPlayersColor(), dropBlackState,
                                    dropWhiteState, illegalMoveList)                                 
                                                                 
                        print('MOVE TO PLAY IS:', moveToPlay)
                        mg.writeMoveToBuffer(moveToPlay, "ext_data/movetoplay.txt")
                        self.gameState.AIMessage = 'LEGAL'
                        print('Checking if a move is loaded by the AI')
                        if os.stat("ext_data/movetoplay.txt").st_size != 0:
                            print('There is a move! Let us load it')
                            logic.PlayAIMove(self)
                            f = open('ext_data/load_game.txt', 'r+')
                            f.truncate(0)
                            f.close()
                            f = open('ext_data/movetoplay.txt', 'r+')
                            f.truncate(0)
                            f.close()
                            
                        
                        if self.gameState.AIMessage == 'ILLEGAL':
                            illegalMoveList.append(moveToCheck)
                        else:
                            self.gameState.AIMessage == 'LEGAL'
                            break
                
                '''
            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                print(e)
                print('Game has not started yet or AI has not started making a move')
