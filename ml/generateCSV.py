import csv
from ml.generateLabels import generateLabels
class csvUtil():
    def __init__(self, gameFileName):
        self.gameFileName = gameFileName

    def createFeatureCSV(self, feature):
        with open('features.csv', 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ')
            spamwriter.writerow([feature])
    
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
csvObj.createFeatureCSV('1,1,0,1')
csvObj.createLabelCSV(csvObj.getOriginalFile())
'''