import csv
try:
    from ml.generateLabels import generateLabels
except:
    from generateLabels import generateLabels

def run_once(f):
        def wrapper(*args, **kwargs):
            if not wrapper.has_run:
                wrapper.has_run = True
                return f(*args, **kwargs)
        wrapper.has_run = False
        return wrapper
        
class csvUtil():
    def __init__(self, gameFileName = None):
        self.gameFileName = gameFileName

    @run_once
    def createHeaders(self, FILENAME):
        with open(FILENAME, 'w') as f:
            w = csv.writer(f)
            w.writerow([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,'Win'])


    def createCombinedCSV(self, feature, FILENAME, CSAFILE):
        with open('training.csv', 'a', newline='') as csvfile:
            genLabel = generateLabels()
            label = (genLabel.run(CSAFILE))
            spamwriter = csv.writer(csvfile, delimiter=',')
            spamwriter.writerow(feature + [label])


    def createFeatureCSV(self, feature):
        with open('features.csv', 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',')
            spamwriter.writerow(feature)
    
    def createLabelCSV(self, FILENAME):
        genLabel = generateLabels()
        label = (genLabel.run(FILENAME))
        with open('labels.csv', 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ')
            spamwriter.writerow([label])
    

    #In case we need more info, this can be set to point to the right game file
    def getOriginalFile(self):
        return self.gameFileName

#USAGE
'''
csvObj = csvUtil('tmp-1-0.csa')
csvObj.createHeaders('training.csv')
'''