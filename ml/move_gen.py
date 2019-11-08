#☖G6i5h
#Get all available moves so far
#class AIListener():
import random

def getPossibleMoves(oldMatrixPosX, oldMatrixPosY, pos, gameMatrix, isBlackTurn):
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
                            possibleMoveMatrix.append((oldMatrixPosX, oldMatrixPosY, oldMatrixPosX + x_dif, oldMatrixPosY + y_dif, pos))

                        if ((str(gameMatrix[oldMatrixPosX + x_dif][oldMatrixPosY + y_dif])[:-1] != 'W') and isBlackTurn == False):
                            possibleMoveMatrix.append((oldMatrixPosX, oldMatrixPosY, oldMatrixPosX + x_dif, oldMatrixPosY + y_dif, pos))

                        if ((str(gameMatrix[oldMatrixPosX + x_dif][oldMatrixPosY + y_dif])[:-1] == 'W') and isBlackTurn == True):
                            break

                        if ((str(gameMatrix[oldMatrixPosX + x_dif][oldMatrixPosY + y_dif])[:-1] == 'B') and isBlackTurn == False):
                            break
                    except Exception as e:
                        print(e)
                        print('Move not on board so ignoring')
    #Remove duplicates
    possibleMoveMatrix = list(dict.fromkeys(possibleMoveMatrix))

    #Remove negatives
    possibleMoveMatrix = [item for item in possibleMoveMatrix if item[0] >= 0 and item[1] >= 0]
    print(possibleMoveMatrix)
    return possibleMoveMatrix
    #print(pos, (oldMatrixPosX), (oldMatrixPosY), oldMatrixPosX + x_dif + 1, oldMatrixPosY + y_dif + 1)

def convMoveToNotation(moveToPlay):
    #Add move to convert into standard notation

#TEST CASE
gameMatrix = [['Wl', 'Wn', 'Ws', 'Wg', 'Wk', 'Wg', 'Ws', 'Wn', 'Wl'], [0, 'Wr', 0, 0, 0, 0, 0, 'Wb', 0], ['Wp', 'Wp', 'Wp', 'Wp', 'Wp', 'Wp', 'Wp', 'Wp', 'Wp'], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 'Bp', 0, 0, 0, 0, 0], ['Bp', 'Bp', 'Bp', 0, 'Bp', 'Bp', 'Bp', 'Bp', 'Bp'], [0, 'Bb', 0, 0, 0, 0, 0, 'Br', 0], ['Bl', 'Bn', 'Bs', 'Bg', 'Bk', 'Bg', 'Bs', 'Bn', 'Bl']]

#Iterate through gameMatrix
possibleMoves = []
for i in range(0, 9):
            for j in range(0, 9):
                pos = (gameMatrix[i][j])
                try:
                    if pos[:-1] == 'W':
                        gameTurn = False
                    else:
                        gameTurn = True
                    print(pos)
                    possibleMoves += getPossibleMoves(i,j, pos, gameMatrix, gameTurn)
                except:
                    pass

print(possibleMoves[random.randint(0,len(possibleMoves) - 1)] )
