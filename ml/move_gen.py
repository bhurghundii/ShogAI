#☖G6i5h
#Get all available moves so far
#class AIListener():
import random, copy

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
            
        randomIndex = self.pickARandomMove(len(possibleMoves))
        self.convMoveToNotation(possibleMoves[randomIndex][4], False, False, False, possibleMoves[randomIndex][3], possibleMoves[randomIndex][2], possibleMoves[randomIndex][1], possibleMoves[randomIndex][0])
        return (self.convMoveToNotation(possibleMoves[randomIndex][4], False, False, False, possibleMoves[randomIndex][3], possibleMoves[randomIndex][2], possibleMoves[randomIndex][1], possibleMoves[randomIndex][0]))

    #orgx orgy newx newy pos matrix
    #  0   1   2     3   4    5



