# -*- coding: UTF-8 -*-
from shog_gamestate import shog_gamestate
from shog_gui import shog_gui

class GameManager():

    def __init__(self, board_size, load = None, AI = None, pc = None, loadFile = None):
        self.playerSelected = pc
        self.board_size = board_size
        self.load = load
        self.AI = AI
        self.loadFile = loadFile

    def run(self):
        #Load game board from standardlayout.txt and place here
        gameMatrix = [[0 for  x in range(self.board_size)] for y in range(self.board_size)]
        with open('standardlayout.txt') as f:
            content = f.readlines()
            if (content[0].split(' ')[0] == '[BLACK]'):
                print ('Setting black')
                for i in range(1, len(content[0].split(' '))):
                    x = list(content[0].split(' ')[i])
                    gameMatrix[int(x[1]) -1][int(x[2]) - 1] = 'B' + x[0].lower()

            if (content[1].split(' ')[0] == '[WHITE]'):
                print ('Setting white')
                for i in range(1, len(content[1].split(' '))):
                    x = list(content[1].split(' ')[i])
                    gameMatrix[int(x[1]) - 1][int(x[2]) - 1] = 'W' + x[0].lower()

            gameState = shog_gamestate(self.board_size, gameMatrix)
            gameState.isLoad = self.load
            gameState.isAI = self.AI

            if (self.loadFile != None):
                gameState.loadFile = self.loadFile

            gameState.playerSelected = self.playerSelected
            boardGraphic = shog_gui(gameState)
            shog_gui.drawInitialBoard(boardGraphic)

class GameInitializer():
    def readConfig(self):
        #Read the config file to see what settings are to be sets
        #Expansion?
        with open('configure.txt') as f:
            configContent = f.readlines()
        board_size = int(configContent[0])
        print(('Setting board size of ' + str(board_size)))
        return board_size
    def run(self, load = None, AI = None, pc = None, loadFile = None):
        print('====================GAME SET UP===========================')
        print('Doing warm up functions like checking settings and params')

        if loadFile != None:
            print("Loading from: ", loadFile)

        if load == True and AI == False:
            print('Loading a game from file selected')
        if load == False and AI == True:
            print('AI selected. Waking up listener')
        if load == False and AI == False:
            print('Vanilla 2P selected')

        board_size = self.readConfig()
        gameInstanceBegins = GameManager(board_size, load, AI, pc, loadFile)
        gameInstanceBegins.run()

if __name__ == '__main__':
    board_size = GameInitializer().readConfig()
    gameInstanceBegins = GameManager(board_size)
    gameInstanceBegins.run()
