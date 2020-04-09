#☖G6i5h
#Get all available moves so far
#class AIListener():
import random, copy
import itertools
import csv, traceback, sys, subprocess
import itertools, random
from tensorflow.keras.models import load_model
import numpy as np

classifier = load_model('/home/ubuntu/Documents/Shogi-DISS/src/ml/pharoah2/model_single.h5')
autoencoder = load_model('/home/ubuntu/Documents/Shogi-DISS/src/ml/pharoah2/autoencoder.h5')


# load model


import math
import logging
logging.basicConfig(level=logging.DEBUG)
import scipy.io as sio # The library to deal with .mat
from sklearn.metrics import classification_report
import tensorflow as tf
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
import datetime

class moveGeneration():

    def getPossibleMoves(self, oldMatrixPosX, oldMatrixPosY, pos, gameMatrix, isBlackTurn):
        localMatrix = copy.deepcopy(gameMatrix)
        possibleMoveMatrix = []
        dropMove = promoteMove = False
        #So we get every move available on the board
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
                            if ((str(gameMatrix[oldMatrixPosX + x_dif][oldMatrixPosY + y_dif])[:-1] == 'B') and isBlackTurn == True):
                                break

                            if ((str(gameMatrix[oldMatrixPosX + x_dif][oldMatrixPosY + y_dif])[:-1] == 'W') and isBlackTurn == False):
                                break

                            if ((str(gameMatrix[oldMatrixPosX + x_dif][oldMatrixPosY + y_dif])[:-1] != 'B') and isBlackTurn == True):
                                localMatrix[oldMatrixPosX + x_dif][oldMatrixPosY + y_dif] = pos
                                localMatrix[oldMatrixPosX][oldMatrixPosY] = 0
                                if (oldMatrixPosX >= 0 and oldMatrixPosY >= 0 and (oldMatrixPosX + x_dif) >= 0 and (oldMatrixPosY + y_dif) >= 0):
                                    possibleMoveMatrix.append((oldMatrixPosX, oldMatrixPosY, oldMatrixPosX + x_dif, oldMatrixPosY + y_dif, pos, list(localMatrix), dropMove, promoteMove))

                                    #Check if the oldmatrix or the new one is in the enemy area to give an option to promote
                                    if (isBlackTurn and ((oldMatrixPosX + x_dif) <= 2 or (oldMatrixPosX + x_dif) <= 2)):
                                        possibleMoveMatrix.append((oldMatrixPosX, oldMatrixPosY, oldMatrixPosX + x_dif, oldMatrixPosY + y_dif, pos.upper(), list(localMatrix), dropMove, True))
                    
                                    if (isBlackTurn == False and ((oldMatrixPosX + x_dif >= 6) or (oldMatrixPosX + x_dif) >= 6)):
                                        possibleMoveMatrix.append((oldMatrixPosX, oldMatrixPosY, oldMatrixPosX + x_dif, oldMatrixPosY + y_dif, pos.upper(), list(localMatrix), dropMove, True))


                            if ((str(gameMatrix[oldMatrixPosX + x_dif][oldMatrixPosY + y_dif])[:-1] != 'W') and isBlackTurn == False):
                                localMatrix[oldMatrixPosX + x_dif][oldMatrixPosY + y_dif] = pos
                                localMatrix[oldMatrixPosX][oldMatrixPosY] = 0
                                if (oldMatrixPosX >= 0 and oldMatrixPosY >= 0 and (oldMatrixPosX + x_dif) >= 0 and (oldMatrixPosY + y_dif) >= 0):
                                    possibleMoveMatrix.append((oldMatrixPosX, oldMatrixPosY, oldMatrixPosX + x_dif, oldMatrixPosY + y_dif, pos, list(localMatrix), dropMove, promoteMove))

                                    #Check if the oldmatrix or the new one is in the enemy area to give an option to promote
                                    if (isBlackTurn and ((oldMatrixPosX + x_dif) <= 2 or (oldMatrixPosX + x_dif) <= 2)):
                                        possibleMoveMatrix.append((oldMatrixPosX, oldMatrixPosY, oldMatrixPosX + x_dif, oldMatrixPosY + y_dif, pos.upper(), list(localMatrix), dropMove, True))
                    
                                    if (isBlackTurn == False and ((oldMatrixPosX + x_dif >= 6) or (oldMatrixPosX + x_dif) >= 6)):
                                        possibleMoveMatrix.append((oldMatrixPosX, oldMatrixPosY, oldMatrixPosX + x_dif, oldMatrixPosY + y_dif, pos.upper(), list(localMatrix), dropMove, True))

                            if ((str(gameMatrix[oldMatrixPosX + x_dif][oldMatrixPosY + y_dif])[:-1] == 'W') and isBlackTurn == True):
                                break

                            if ((str(gameMatrix[oldMatrixPosX + x_dif][oldMatrixPosY + y_dif])[:-1] == 'B') and isBlackTurn == False):
                                break
                        except Exception as e:
                            pass
        #Remove duplicates
        #possibleMoveMatrix = list(dict.fromkeys(possibleMoveMatrix))
    
        #Remove negatives
        possibleMoveMatrix = [item for item in possibleMoveMatrix if item[0] >= 0 and item[1] >= 0]

        #Get the moves that are available by dropping

        return (possibleMoveMatrix)

    #getPossibleDrops(i,j, dropWhitePcs, gameMatrix, isBlack)
    def getPossibleDrops(self, oldMatrixPosX, oldMatrixPosY, dropPcs, gameMatrix, isBlackTurn):
        #Grab a copy of the gamematrix
        localMatrix = copy.deepcopy(gameMatrix)
        possibleMoveMatrix = []
        dropMove = True
        promoteMove = False
        try:
            #Check if the space we are going to drop to is empty
            if (str(localMatrix[oldMatrixPosX][oldMatrixPosY]) == '0'):
                #We try and check if a piece can be dropped using all the available pieces
                for DropPiece in dropPcs:
                    if 'n' in DropPiece:
                        if (oldMatrixPosY <= 1 and isBlackTurn) or (
                                oldMatrixPosY >= 7 and isBlackTurn == False):
                            pass
                        else:
                            localMatrix[oldMatrixPosX][oldMatrixPosY] = DropPiece
                            possibleMoveMatrix.append((oldMatrixPosX, oldMatrixPosY, oldMatrixPosX, oldMatrixPosY, DropPiece, list(localMatrix), dropMove, promoteMove))
                    #Check if drop location is legal for lance
                    elif 'l' in DropPiece:
                        if (oldMatrixPosY == 0 and isBlackTurn) or (
                                oldMatrixPosY == 8 and isBlackTurn == False):
                                pass
                        else:
                            localMatrix[oldMatrixPosX][oldMatrixPosY] = DropPiece
                            possibleMoveMatrix.append((oldMatrixPosX, oldMatrixPosY, oldMatrixPosX, oldMatrixPosY, DropPiece, list(localMatrix), dropMove, promoteMove))
                    #This makes sure pawns are legal
                    # no 2 pawn rule
                    elif 'p' in DropPiece:
                        if (oldMatrixPosY == 0 and isBlackTurn) or (
                                oldMatrixPosY == 8 and isBlackTurn == False):
                            print('Too deep for pawn')
                            
                        else:
                            colMat = []
                            for y in range(0, 9):
                                colMat.append(localMatrix[y][oldMatrixPosY])

                            pawnTeam = 'p'
                            if isBlackTurn:
                                pawnTeam = 'B' + pawnTeam
                            else:
                                pawnTeam = 'W' + pawnTeam

                            if pawnTeam in colMat:
                                print('There is a pawn on this column')
                                

                            else:
                                # get pos of king
                                kingTeam = 'k'
                                if isBlackTurn:
                                    kingTeam = 'W' + kingTeam
                                else:
                                    kingTeam = 'B' + kingTeam

                                localMatrix[oldMatrixPosX][oldMatrixPosY] = DropPiece
                                possibleMoveMatrix.append((oldMatrixPosX, oldMatrixPosY, oldMatrixPosX, oldMatrixPosY, DropPiece, list(localMatrix), dropMove, promoteMove))
                    #If the piece we want to drop isn't a pawn, lance or knight
                    #There isn't a problem so it doesn't matter.
                    elif 'p' not in DropPiece and 'l' not in DropPiece and 'n' not in DropPiece:
                        localMatrix[oldMatrixPosX][oldMatrixPosY] = DropPiece
                        possibleMoveMatrix.append((oldMatrixPosX, oldMatrixPosY, oldMatrixPosX, oldMatrixPosY, DropPiece, list(localMatrix), dropMove, promoteMove))
        except Exception as e:
            traceback.print_exc(file=sys.stdout)                 
            print (e)

        
        #Remove duplicates
       
        #Get the moves that are available by dropping
        #print('possiblemovematrix', possibleMoveMatrix)
        return (possibleMoveMatrix)

    def convMoveToNotation(self, piece, isPromotion, isCapture, isDrop, newMatrixPosY, newMatrixPosX, i = None, j = None):

        if (i == None and j == None):
            return(self.getTurn(piece) + self.getPiece(piece, isPromotion) + self.getSimpleMove(isPromotion, isCapture, isDrop) + self.getCaptureSymbol(isCapture) + self.getDropSymbol(isDrop) + str(self.YValueToShogNotation(newMatrixPosY)) + self.numberToLetter(newMatrixPosX) + self.getPromotionSymbol(isPromotion) + '\n')
        else:
            return(self.getTurn(piece) + self.getPiece(piece, isPromotion) + str(self.YValueToShogNotation(i)) + self.numberToLetter(j) + self.getCaptureSymbol(isCapture) + self.getDropSymbol(isDrop) + str(self.YValueToShogNotation(newMatrixPosY)) + self.numberToLetter(newMatrixPosX) + self.getPromotionSymbol(isPromotion) + '\n')

    def getSimpleMove(self, isPromotion, isCapture, isDrop):
        return (lambda isPromotion, isCapture, isDrop : '-'  if (isPromotion, isCapture, isDrop) == (False, False, False) else '')(isPromotion, isCapture, isDrop)

    def getPiece(self, piece, isPromotion):
        return (lambda piece, isPromotion : '+' + piece[1:].upper() if (piece[1:].isupper() and isPromotion == False) else piece[1:].upper())(piece, isPromotion)

    def getPromotionSymbol(self, isPromotion):
        return (lambda isPromotion : '+' if isPromotion == True else '')(isPromotion)

    def getCaptureSymbol(self, isCapture):
        return (lambda isCapture : 'x' if isCapture == True else '')(isCapture)

    def getDropSymbol(self, isDrop):
        return (lambda isDrop : '*' if isDrop == True else '')(isDrop)

    def getTurn(self, piece):
        return (lambda isTurn : '☖' if isTurn == 'B' else '☗')(piece[:-1])

    def YValueToShogNotation(self, num):
        return 9 - num

    def numberToLetter(self, num):
        return chr(num + 65).lower()
        #Add move to convert into standard notation

    def pickARandomMove(self, length):
         return random.randint(0,length - 1)
    
    def writeMoveToBuffer(self, move, FILEPATH):
        f = open(FILEPATH, "w")
        f.write(move)
        f.close()

    def generatePossibleMovesForTree(self, gameMatrix, isBlack, dropBlackpcs, dropWhitePcs):
        possibleMoves = []
        #Get moves on board already
        for i in range(0, 9):
                    for j in range(0, 9):
                        pos = (gameMatrix[i][j])
                        try:
                            if (pos[:-1] == 'W') and isBlack == False:
                                possibleMoves += self.getPossibleMoves(i,j, pos, gameMatrix, isBlack)
                            elif (pos[:-1] == 'B') and isBlack == True:
                                possibleMoves += self.getPossibleMoves(i,j, pos, gameMatrix, isBlack)
                        except:
                            pass
    
        #Get moves you can drop
        for i in range(0, 9):
                    for j in range(0, 9):
                        try:
                            if isBlack == False:
                                if (len(dropWhitePcs) > 0):
                                    
                                    possibleMoveDrop = self.getPossibleDrops(i,j, dropWhitePcs, gameMatrix, isBlack)
                                    if possibleMoveDrop != None:
                                        possibleMoves += possibleMoveDrop
                            elif isBlack == True:
                                if (len(dropBlackpcs) > 0):
                                    possibleMoves += self.getPossibleDrops(i,j, dropBlackpcs, gameMatrix, isBlack)
                        except Exception as e:
                            print(e)  
        return possibleMoves

    import random
    #TODO: I SUSPECT ITS JUST ACCEPTING THE LAST MOVE FOR SOME REASON

    def alphabetaroot(self, gameMatrix, gamedata, isBlack, dropBlackpcs, dropWhitePcs, depth, alpha, beta, rootmove = None, illegalMoves = None):
        possibleMoves = self.generatePossibleMovesForTree(gameMatrix, isBlack, dropBlackpcs, dropWhitePcs)
        bestMove = float('-inf')
        bestMoveFinal = None
        for possibleUnconvertedGameStates in possibleMoves: 
            value = self.alphabeta(possibleUnconvertedGameStates[5], possibleUnconvertedGameStates, True , dropBlackpcs, dropWhitePcs, depth - 1, alpha, beta, possibleUnconvertedGameStates, illegalMoves)
            if (value > bestMove):
                bestMove = value
                bestMoveFinal = possibleUnconvertedGameStates
        return bestMoveFinal


    def alphabeta(self, gameMatrix, gamedata, isBlack, dropBlackpcs, dropWhitePcs, depth, alpha, beta, rootmove = None, illegalMoves = None):
        if depth <= 0:
            value = loadmodelclass().getlabel(list(self.convertPossibleMovesIntoNumericalForm2(gameMatrix)))
            #score = random.uniform(0, 1)
            #value = alphabeta_data(np.asarray(score), gamedata, rootmove)
            return value

        if (isBlack == True):
            value = float('-inf')
            possibleMoves = self.generatePossibleMovesForTree(gameMatrix, isBlack, dropBlackpcs, dropWhitePcs)
            possibleMoves = [i for i in possibleMoves if i not in illegalMoves]
            for possibleUnconvertedGameStates in possibleMoves: 
                    value = self.alphabeta(possibleUnconvertedGameStates[5], possibleUnconvertedGameStates, True , dropBlackpcs, dropWhitePcs, depth - 1, alpha, beta, possibleUnconvertedGameStates, illegalMoves)
        
                    alpha = max(alpha, value)

                    if alpha >= beta:
                        break

            return value

        else:
            value = float('inf')
            possibleMoves = self.generatePossibleMovesForTree(gameMatrix, isBlack, dropBlackpcs, dropWhitePcs)
            possibleMoves = [i for i in possibleMoves if i not in illegalMoves]

            for possibleUnconvertedGameStates in possibleMoves:
                value = self.alphabeta(possibleUnconvertedGameStates[5], possibleUnconvertedGameStates, False, dropBlackpcs, dropWhitePcs, depth - 1, alpha, beta, possibleUnconvertedGameStates, illegalMoves)          
                beta = min(beta, value)
                #print('A1', np.asarray(alpha.value).flat[0], 'B1', np.asarray(beta.value).flat[0], 'V1', value.value.flat[0])
                if alpha >= beta:
                    break
            return value
    
    def minmax(self, gameMatrix, gamedata, isBlack, dropBlackpcs, dropWhitePcs, depth, alpha, beta, rootmove = None, illegalMoves = None):
        possibleMoves = self.generatePossibleMovesForTree(gameMatrix, isBlack, dropBlackpcs, dropWhitePcs)
        possibleMoves = [i for i in possibleMoves if i not in illegalMoves]
        bestMove = None
        bestScore = 0
        for possibleUnconvertedGameStates in possibleMoves:
            score = alphabeta_data(loadmodelclass().getlabel(list(self.convertPossibleMovesIntoNumericalForm2(possibleUnconvertedGameStates[5]))), gamedata, rootmove)
            if bestScore < score.value.flat[0]:
                bestScore = score.value.flat[0]
                bestMove = possibleUnconvertedGameStates
        
        return bestMove


    def GenMoves(self, gameMatrix, isBlack, dropBlackpcs, dropWhitePcs, illegalMoves = None):
        #Iterate through gameMatrix
        print(gameMatrix)
        alpha = float('-inf')
        beta = float('inf')
        DEPTH = 2
        bestmove = self.alphabetaroot(gameMatrix, None, isBlack, dropBlackpcs, dropWhitePcs, DEPTH, alpha, beta, None, illegalMoves)
        return (self.convMoveToNotation(bestmove[4], bestmove[7], False, bestmove[6], bestmove[3], bestmove[2], bestmove[1], bestmove[0])), bestmove

    def writeToPotentialMoveCSV(self, array):
        #if (len(array) != 120):
        #    lenToAdd = abs(120 - len(array))
        #    for extra0 in range(0, lenToAdd):
        #        array.append(0)
        with open('/home/ubuntu/Documents/Shogi-DISS/src/ml/pharoah2/moveposition.csv', 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',')
            spamwriter.writerow(array)

    def convertPossibleMovesIntoNumericalForm(self, possibleUnconvertedGameSate):
        #possibleMoves[0][5] should is the new gamestate after it's done up
        possibleGameState = list(itertools.chain.from_iterable(possibleUnconvertedGameSate))
        
        #Convert the pieces into equivalent numbers because training  
        #process only uses numbers 
        pc2num = ''
        file = open('ml/eval_pcs.map', 'r')
        pc2num = (file.read().split('\n'))
        file.close()
        convMatrix = []
        for x in possibleGameState:
            for l in pc2num:
                try: 
                    if x[-1:] in l:
                        if x[0] == 'W':
                            convMatrix.append('-' + l.split('=')[1])
                            break
                        elif x[0] == 'B':
                            convMatrix.append(l.split('=')[1])
                            break
                        elif x[0] == '0':
                            convMatrix.append(l.split('=')[1])
                            break
                        
                except:
                    if (x == 0):
                        convMatrix.append(0)
                        break
        self.writeToPotentialMoveCSV(convMatrix)
        return (convMatrix)
    
    def convertPossibleMovesIntoNumericalForm2(self, possibleUnconvertedGameSate):
        whiteDrops, blackDrops = [], []
        '''
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
        '''

        while len(whiteDrops) != 19:
            whiteDrops.append('0')
        while len(blackDrops) != 19:
            blackDrops.append('0')

        possibleUnconvertedGameSate = ([y for x in possibleUnconvertedGameSate for y in x] + whiteDrops + blackDrops)

        pcs = ['Wl', 'Wn', 'Ws', 'Wg', 'Wk', 'Wr', 'Wb', 'Wp', 'Bl', 'Bn', 'Bs', 'Bg', 'Bk', 'Br', 'Bb', 'Bp', 'WL', 'WN', 'WS', 'WR', 'WB', 'WP', 'BL', 'BN', 'BS', 'BR', 'BB', 'BP']
        bitmap = []
        #print(possibleUnconvertedGameSate)
        for pc in pcs: 
            for x in possibleUnconvertedGameSate:
                if x == pc:
                    bitmap.append(1)
                else:
                    bitmap.append(0)
        
        self.writeToPotentialMoveCSV(bitmap)
        return (bitmap)

    #orgx orgy newx newy pos matrix
    #  0   1   2     3   4    5

class loadmodelclass():

    def checkLoad(self):
        return(True)
  
    def getlabel(self, feature):
        m_test = np.asarray(feature)
        X_test = np.reshape(m_test, (1, 3332))
        # Restore it
        # Test
        #1 - because white optimized
        
        Y_pred = classifier.predict(autoencoder.predict(X_test))
        
        return (Y_pred)
    
    def getlabelBatch(self, featureset):
        Y_pred = []
        for feature in featureset:
            print('PERFORMACNE')
            m_test = np.asarray(feature)
            X_test = np.reshape(m_test, (1, 3332))
            # Restore it
            
            # Test
            Y_pred.append((classifier.predict_proba(X_test).flat[0]))                    
        return (Y_pred)
