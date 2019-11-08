from googletrans import Translator
import glob, os
from ml_util import ml_util

#7: ☖P-7e
for file in glob.glob("*.txt"):
    fileRead = open(file, 'r')
    log = fileRead.readlines()
    #translator = Translator()
    #print(translator.translate(log))

index = 0
for l in range(1,len(log)):
    if len(log[l]) == 2:
        print('Index: ' + str(l))
        index = l + 1

for l in range(index,len(log)):
    if '+' in log[l]:
        turn = '☗'
    else:
        turn = '☖'

    origin_x = log[l][1]
    origin_y = ml_util().numberToLetter(int(log[l][2]))
    end_x = log[l][3]
    end_y = ml_util().numberToLetter(int(log[l][4]))

    if 'FU' in log[l]:
        pc = 'P'
    if 'KY' in log[l]:
        pc = 'L'
    if 'KE' in log[l]:
        pc = 'N'
    if 'GI' in log[l]:
        pc = 'S'
    if 'KI' in log[l]:
        pc = 'G'
    if 'KA' in log[l]:
        pc = 'B'
    if 'KY' in log[l]:
        pc = 'L'
    if 'HI' in log[l]:
        pc = 'R'
    if 'OU' in log[l]:
        pc = 'K'
    if 'TO' in log[l]:
        pc = '+P'
    if 'NY' in log[l]:
        pc = '+N'
    if 'NK' in log[l]:
        pc = '+L'
    if 'NG' in log[l]:
        pc = '+S'
    if 'UM' in log[l]:
        pc = '+B'
    if 'RY' in log[l]:
        pc = '+R'


    print('Turn: ' + log[l])
    print(turn, pc , origin_x, origin_y, end_x, end_y)
