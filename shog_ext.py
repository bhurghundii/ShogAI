# -*- coding: UTF-8 -*-

import datetime

class shog_play_external_moves():

    def getTurnFromFile(self):
        with open('ext_data/movetoplay.txt') as f:
            turnMove = f.read()
        return turnMove

    def convertTurnToGameMatrixCompatible(self):
        convMove = self.getTurnFromFile()
        print convMove


class shog_recorder():

    def recordMove(self, piece, isPromotion, isCapture, isDrop, newMatrixPosY, newMatrixPosX, i = None, j = None):
        if gameTurn.gameTurn == 0:
            gameTurn().initRecordSheetFile()

        gameTurn.updateGameTurn()

        f = open(gameTurn.recordSheet, "a")

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
        return (lambda isTurn : '☗' if isTurn == 'B' else '☖')(piece[:-1])

    def YValueToShogNotation(self, num):
        return 9 - num

    def numberToLetter(self, num):
        return chr(num + 65).lower()

class gameTurn:
    gameTurn = 0
    recordSheet = ''

    @staticmethod
    def updateGameTurn():
        gameTurn.gameTurn += 1

    def initRecordSheetFile(self):
     now = datetime.datetime.now()
     gameTurn.recordSheet = "records/" + str(now.year) + ":" + str(now.month) + ":" + str(now.day) + ":" + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + '-RecordSheet.txt'
     f = open(gameTurn.recordSheet, "w")

shog_play_external_moves().convertTurnToGameMatrixCompatible()
