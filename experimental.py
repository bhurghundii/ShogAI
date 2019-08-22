import numpy as np
import itertools

with open('movesets.txt') as f:
    content = f.readlines()
    for index in range(len(content)):
        piece = content[index].split('=')[0]
        movesets = content[index].split('=')[1]
        #cast movesets to array
        possiblemovelayouts =  eval(movesets)


        for j in range(len(possiblemovelayouts)):
            x_range = (possiblemovelayouts[j])[0]
            y_range = (possiblemovelayouts[j])[1]


            expansion_x = 0
            expansion_y = 0

            if ':' in (possiblemovelayouts[j])[0]:
                lowrange = x_range.split(':')[1]
                highrange = x_range.split(':')[0]
                expansion_x = range(int(lowrange), int(highrange) + 1)
            else:
                expansion_x = (possiblemovelayouts[j])[0]

            if ':' in (possiblemovelayouts[j])[1]:
                lowrange = y_range.split(':')[1]
                highrange = y_range.split(':')[0]
                expansion_y = range(int(lowrange), int(highrange) + 1)
            else:
                expansion_y = (possiblemovelayouts[j])[1]

            list3 = [[x,y] for x in expansion_x for y in expansion_y]
            print piece + '=' + str(list3)

            print '\n'
