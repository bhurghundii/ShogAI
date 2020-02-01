#☖G6i5h
#Get all available moves so far
#class AIListener():
import random, copy
import itertools
import csv
from ml.demo.test_reuseModel import evaluatePositions

class moveGeneration():
    def getPossibleMoves(self, oldMatrixPosX, oldMatrixPosY, pos, gameMatrix, isBlackTurn):
        localMatrix = copy.deepcopy(gameMatrix)
        possibleMoveMatrix = []
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
                                    possibleMoveMatrix.append((oldMatrixPosX, oldMatrixPosY, oldMatrixPosX + x_dif, oldMatrixPosY + y_dif, pos, list(localMatrix)))

                            if ((str(gameMatrix[oldMatrixPosX + x_dif][oldMatrixPosY + y_dif])[:-1] != 'W') and isBlackTurn == False):
                                localMatrix[oldMatrixPosX + x_dif][oldMatrixPosY + y_dif] = pos
                                localMatrix[oldMatrixPosX][oldMatrixPosY] = 0
                                if (oldMatrixPosX >= 0 and oldMatrixPosY >= 0 and (oldMatrixPosX + x_dif) >= 0 and (oldMatrixPosY + y_dif) >= 0):
                                    possibleMoveMatrix.append((oldMatrixPosX, oldMatrixPosY, oldMatrixPosX + x_dif, oldMatrixPosY + y_dif, pos, list(localMatrix)))

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
        return possibleMoveMatrix

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

    def GenMoves(self, gameMatrix, isBlack):
        #Iterate through gameMatrix
        possibleMoves = []

        print(isBlack)
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
        
        possibleStates = ''
        for possibleUnconvertedGameSates in possibleMoves:
            self.convertPossibleMovesIntoNumericalForm(possibleUnconvertedGameSates[5])
        

        #randomIndex = self.pickARandomMove(len(possibleMoves))
        index = evaluatePositions().run()
        print('SELECTED MOVE: ', index, ' with ', possibleMoves[index])
        #self.convMoveToNotation(possibleMoves[randomIndex][4], False, False, False, possibleMoves[randomIndex][3], possibleMoves[randomIndex][2], possibleMoves[randomIndex][1], possibleMoves[randomIndex][0])
        return (self.convMoveToNotation(possibleMoves[index][4], False, False, False, possibleMoves[index][3], possibleMoves[index][2], possibleMoves[index][1], possibleMoves[index][0]))

    def writeToPotentialMoveCSV(self, array):
        #csvObj = csvUtil()
        #csvObj.createHeaders('moveposition.csv')
        if (len(array) != 120):
            lenToAdd = abs(120 - len(array))
            for extra0 in range(0, lenToAdd):
                array.append(0)
        with open('/home/ubuntu/Documents/Shogi-DISS/src/ml/demo/moveposition.csv', 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',')
            spamwriter.writerow(array)

    def convertPossibleMovesIntoNumericalForm(self, possibleUnconvertedGameSate):
        #possibleMoves[0][5] should is the new gamestate after it's done up
        print('POSSIBLE MOVES ARE', possibleUnconvertedGameSate)  
        possibleGameState = list(itertools.chain.from_iterable(possibleUnconvertedGameSate))
        print(possibleGameState)

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
    
   
    #orgx orgy newx newy pos matrix
    #  0   1   2     3   4    5



