convMove = '☗B1i3g+'
isPromote = None
isDrop = None
print (convMove)
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
    convMove = convMove.replace('*', '')
    isDrop = True

#If piece is promoted, parse differently
if ('+' in convMove[0]):
    #Get Piece
    pos += (convMove[1].upper())
    convMove = (convMove.replace('+', ''))
    convMove = convMove.replace(convMove[0], '')
else:
    #Get Piece
    pos += (convMove[0].lower())
    convMove = convMove.replace(convMove[0], '')

#Autopromote piece if it is required

if ('+' in convMove[len(convMove) - 1]):
    isPromote = True
    convMove = (convMove.replace('+', ''))

print(convMove)
convMove = convMove.strip()
'''
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
'''
