import glob, os, sys
from ml_util import ml_util

class processMoves():
    def setDMflag(self):
        pass 
    
    def run(self):
        log = ''
        FILENAME = ''
        for file in glob.glob("storage/*.csa"):
            fileRead = open(file, 'r')
            FILENAME = file
            print(FILENAME)
            log = fileRead.readlines()

            index = 0
            for l in range(1,len(log)):
                if len(log[l]) == 2:
                    print('Index: ' + str(l))
                    index = l + 1

            movesExtractedArray = []
            movesDoneArray = []
            #00 is funny
            #is it drop?!
            for l in range(index,len(log) - 1):
                movesDoneArray.append(log[l])
                if (log[l][1] == '0') and (log[l][2] == '0'):
                    try:
                        if '+' in log[l]:
                            turn = '☖'
                        else:
                            turn = '☗'


                        end_x = log[l][3]
                        end_y = ml_util().numberToLetter((int(log[l][4]) - 1))

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
                        movesExtractedArray.append((turn + pc + '*' + end_x + end_y))
                    except Exception as e:
                        print(e)

                else:
                    try:
                        if '+' in log[l]:
                            turn = '☖'
                        else:
                            turn = '☗'
                        
                        origin_x = log[l][1]
                        origin_y = ml_util().numberToLetter((int(log[l][2]) - 1))
                        end_x = log[l][3]
                        end_y = ml_util().numberToLetter((int(log[l][4]) - 1))

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
                            pc_mutate = 'P'
                            tmp = []
                            for j in range(0, len(movesExtractedArray)):
                                if pc_mutate in str(movesExtractedArray[j]) or ('+' + pc_mutate) in str(movesExtractedArray[j]):
                                    if turn in str(movesExtractedArray[j]):
                                        if (str(movesDoneArray[j][3]) + str(movesDoneArray[j][4])) == (str(log[l][1]) + str(log[l][2])):
                                            print(movesExtractedArray[j])
                                            tmp.append(movesExtractedArray[j])
                            
                            if (pc_mutate in tmp[len(tmp) - 1]):
                                if '+' in tmp[len(tmp) - 1]:
                                    pc = '+' + pc_mutate
                                else:
                                    pc = pc_mutate
                                    end_y = end_y + '+'                       
                            elif (('+' + pc_mutate) in tmp[len(tmp) - 1]):
                                pc = '+' + pc_mutate

                        if 'NY' in log[l]:
                            pc_mutate = 'L'
                            tmp = []
                            for j in range(0, len(movesExtractedArray)):
                                if pc_mutate in str(movesExtractedArray[j]) or ('+' + pc_mutate) in str(movesExtractedArray[j]):
                                    if turn in str(movesExtractedArray[j]):
                                        if (str(movesDoneArray[j][3]) + str(movesDoneArray[j][4])) == (str(log[l][1]) + str(log[l][2])):
                                            print(movesExtractedArray[j])
                                            tmp.append(movesExtractedArray[j])
                            
                            if (pc_mutate in tmp[len(tmp) - 1]):
                                if '+' in tmp[len(tmp) - 1]:
                                    pc = '+' + pc_mutate
                                else:
                                    pc = pc_mutate
                                    end_y = end_y + '+'                       
                            elif (('+' + pc_mutate) in tmp[len(tmp) - 1]):
                                pc = '+' + pc_mutate

                        if 'NK' in log[l]:
                            pc_mutate = 'N'
                            tmp = []
                            for j in range(0, len(movesExtractedArray)):
                                if pc_mutate in str(movesExtractedArray[j]) or ('+' + pc_mutate) in str(movesExtractedArray[j]):
                                    if turn in str(movesExtractedArray[j]):
                                        if (str(movesDoneArray[j][3]) + str(movesDoneArray[j][4])) == (str(log[l][1]) + str(log[l][2])):
                                            print(movesExtractedArray[j])
                                            tmp.append(movesExtractedArray[j])
                            
                            if (pc_mutate in tmp[len(tmp) - 1]):
                                if '+' in tmp[len(tmp) - 1]:
                                    pc = '+' + pc_mutate
                                else:
                                    pc = pc_mutate
                                    end_y = end_y + '+'                       
                            elif (('+' + pc_mutate) in tmp[len(tmp) - 1]):
                                pc = '+' + pc_mutate
                                
                        if 'NG' in log[l]:
                            pc_mutate = 'S'
                            tmp = []
                            for j in range(0, len(movesExtractedArray)):
                                if pc_mutate in str(movesExtractedArray[j]) or ('+' + pc_mutate) in str(movesExtractedArray[j]):
                                    if turn in str(movesExtractedArray[j]):
                                        if (str(movesDoneArray[j][3]) + str(movesDoneArray[j][4])) == (str(log[l][1]) + str(log[l][2])):
                                            print(movesExtractedArray[j])
                                            tmp.append(movesExtractedArray[j])
                            
                            if (pc_mutate in tmp[len(tmp) - 1]):
                                if '+' in tmp[len(tmp) - 1]:
                                    pc = '+' + pc_mutate
                                else:
                                    pc = pc_mutate
                                    end_y = end_y + '+'                       
                            elif (('+' + pc_mutate) in tmp[len(tmp) - 1]):
                                pc = '+' + pc_mutate

                        if 'UM' in log[l]:
                            pc_mutate = 'B'
                            tmp = []
                            for j in range(0, len(movesExtractedArray)):
                                if pc_mutate in str(movesExtractedArray[j]) or ('+' + pc_mutate) in str(movesExtractedArray[j]):
                                    if turn in str(movesExtractedArray[j]):
                                        if (str(movesDoneArray[j][3]) + str(movesDoneArray[j][4])) == (str(log[l][1]) + str(log[l][2])):
                                            print(movesExtractedArray[j])
                                            tmp.append(movesExtractedArray[j])
                            
                            if (pc_mutate in tmp[len(tmp) - 1]):
                                if '+' in tmp[len(tmp) - 1]:
                                    pc = '+' + pc_mutate
                                else:
                                    pc = pc_mutate
                                    end_y = end_y + '+'                       
                            elif (('+' + pc_mutate) in tmp[len(tmp) - 1]):
                                pc = '+' + pc_mutate                

                                
                            

                        if 'RY' in log[l]:
                            pc_mutate = 'R'
                            tmp = []
                            for j in range(0, len(movesExtractedArray)):
                                if pc_mutate in str(movesExtractedArray[j]) or ('+' + pc_mutate) in str(movesExtractedArray[j]):
                                    if turn in str(movesExtractedArray[j]):
                                        if (str(movesDoneArray[j][3]) + str(movesDoneArray[j][4])) == (str(log[l][1]) + str(log[l][2])):
                                            print(movesExtractedArray[j])
                                            tmp.append(movesExtractedArray[j])
                            
                            if (pc_mutate in tmp[len(tmp) - 1]):
                                if '+' in tmp[len(tmp) - 1]:
                                    pc = '+' + pc_mutate
                                else:
                                    pc = pc_mutate
                                    end_y = end_y + '+'                       
                            elif (('+' + pc_mutate) in tmp[len(tmp) - 1]):
                                pc = '+' + pc_mutate

                        #print(turn + pc + origin_x + origin_y + end_x + end_y)
                        movesExtractedArray.append((turn + pc + origin_x + origin_y + end_x + end_y))
                    except Exception as e:
                        print(e)

            for l in range(0, len(movesExtractedArray)):
                print(str(l + 1) + ":" + movesExtractedArray[l])
                with open (FILENAME + '.txt', 'a') as f: f.write (str(str(l + 1) + ":" + movesExtractedArray[l] + "\n"))


#RUNNING ISSUES:
#69: + is not regiestering?!

processMoves().run()