s = ['-2', '-3', '-4', '-5', '-10', '-5', '-4', '-3', '-2', 0, '-5', 0, 0, 0, 0, 0, '-5', 0, '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '1', '1', '1', '1', '1', '1', '1', '1', '1', 0, '5', 0, 0, 0, 0, 0, '5', 0, '2', '3', '4', '5', '10', '5', '4', '3', '2', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
p = [1]

#We get whoever won the game from reading the csa files
class generateLabels():
    def run(self, FILEPATH):
        #Read file and get the lines
        csaFile  = open(FILEPATH, "r")
        csaLines = (csaFile.readlines())
        #Check lines for the end condition / wins
        #TODO: Work it for non surrender situation as well
        for lineIndex in range(0, len(csaLines)):
            if '%TORYO' in csaLines[lineIndex]:
                if (csaLines[lineIndex - 1][0]) == '+':
                    label = 1
                    return (label)
                else:
                    label = 0
                    return (label)

#USAGE
'''
FILEPATH = 'tmp-1-0.csa'
print(generateLabels().run(FILEPATH))
'''