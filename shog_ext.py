# -*- coding: UTF-8 -*-

import datetime
from threading import Timer, Thread, Event

class shog_play_external_moves():

    def isThereAMoveToPlay_ext(self):
        with open('ext_data/movetoplay.txt') as f:
            turnMove = f.read()
        return (lambda turnMove: True if (len(turnMove) != 0) else False)(turnMove)

    def getTurnFromFile(self):
        with open('ext_data/movetoplay.txt') as f:
            turnMove = f.read()
        return turnMove

    def getLengthOfPlay(self):
        with open('ext_data/load_game.txt') as f:
            turnMove = f.readlines()
        return len(turnMove)

    def clearLoadGame(self):
        f = open('ext_data/load_game.txt', "w", encoding='utf-8')
        f.close()

    def convertTurnToGameMatrixCompatible(self):
        convMove = self.getTurnFromFile()

        if ('☗' in convMove):
            IsBlackMove = False
            convMove = convMove.replace('☗', '')
            pos = 'W'
        else:
            IsBlackMove = True
            convMove = convMove.replace('☖', '')
            pos = 'B'

        if ('-' in convMove):
            convMove = convMove.replace('-', '')

        if ('x' in convMove):
            convMove = convMove.replace('x', '')


        if ('*' in convMove):
            convertedMove.append('D')

        if ('+' in convMove[0]):
            #Get Piece
            pos += (convMove[1])
            convMove = convMove.replace(convMove[1], '')
        else:
            #Get Piece
            pos += (convMove[0].lower())
            convMove = convMove.replace(convMove[0], '')

        convMove = convMove.strip()

        if (len(convMove) == 4):
            oldMatrixPosY = (9 - int(convMove[0]))
            oldMatrixPosX = self.LetterToNumber(convMove[1])

            newMatrixPosY = (9 - int(convMove[2]))
            newMatrixPosX = self.LetterToNumber(convMove[3])
        else:
            oldMatrixPosY = None
            oldMatrixPosX = None

            newMatrixPosY = (9 - int(convMove[0]))
            newMatrixPosX = self.LetterToNumber(convMove[1])

        return (IsBlackMove, pos, oldMatrixPosX, oldMatrixPosY, newMatrixPosX, newMatrixPosY)

    def updateMoveToPlayIfNotEmpty(self, turn):
        try:
            with open('ext_data/load_game.txt') as f:
                turnMove = f.readlines()

            movetoreplay = (turnMove[turn][2:].strip())
            f = open('ext_data/movetoplay.txt', "w", encoding='utf-8')
            f.write(movetoreplay)
            f.close()
        except:
            f = open('ext_data/load_game.txt', "w", encoding='utf-8')
            f.close()
            print('Done playing back. Resuming game')

    def LetterToNumber(self, Letter):
        for chrval in range(97, 123):
            if (Letter == chr(chrval)):
                return chrval - 97

    def ShogNotationToY(self, num):
        return 9 - num

        #Now that we got the move... let's grab the matrix and find out who could've made the move!

class shog_recorder():

    def recordMove(self, piece, isPromotion, isCapture, isDrop, newMatrixPosY, newMatrixPosX, i = None, j = None):

        if gameTurn.gameTurn == 0:
            gameTurn().initRecordSheetFile()

        gameTurn.updateGameTurn()

        f = open(gameTurn.recordSheet, "a", encoding='utf-8')

        if (i == None and j == None):
            f.write(str(gameTurn.gameTurn) + ': ' + self.getTurn(piece) + self.getPiece(piece, isPromotion) + self.getSimpleMove(isPromotion, isCapture, isDrop) + self.getCaptureSymbol(isCapture) + self.getDropSymbol(isDrop) + str(self.YValueToShogNotation(newMatrixPosY)) + self.numberToLetter(newMatrixPosX) + self.getPromotionSymbol(isPromotion) + '\n')
        else:
            f.write(str(gameTurn.gameTurn) + ': ' + self.getTurn(piece) + self.getPiece(piece, isPromotion) + str(self.YValueToShogNotation(i)) + self.numberToLetter(j) + self.getCaptureSymbol(isCapture) + self.getDropSymbol(isDrop) + str(self.YValueToShogNotation(newMatrixPosY)) + self.numberToLetter(newMatrixPosX) + self.getPromotionSymbol(isPromotion) + '\n')

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

    def getFileRecord(self):
        return gameTurn.recordSheet

class gameTurn:
    gameTurn = 0
    recordSheet = ''

    @staticmethod
    def updateGameTurn():
        gameTurn.gameTurn += 1

    def initRecordSheetFile(self):
     now = datetime.datetime.now()
     gameTurn.recordSheet = r'records/' + str(now.year) + "_" + str(now.month) + "_" + str(now.day) + "_" + str(now.hour) + "_" + str(now.minute) + "_" + str(now.second) + "-RecordSheet.txt"
     f = open(gameTurn.recordSheet, "w")
