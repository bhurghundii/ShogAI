# -*- coding: UTF-8 -*-
from gamestate import gamestate
from tkgui import tkgui

class GameManager():
    #This basically just takes the config file settings and the game mode selected by user
    def __init__(self, board_size, load = None, AI = None, playerSelected = None, loadFile = None, autoPlay = None):
        self.playerSelected = playerSelected
        self.board_size = board_size
        self.load = load
        self.AI = AI
        self.loadFile = loadFile
        self.autoPlay = autoPlay

    def setGameMatrix(self, boardsize):
        gameMatrix = [[0 for  x in range(boardsize)] for y in range(boardsize)]
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
        return gameMatrix
        
    def run(self):
        #Load game board from standardlayout.txt and store in the gameMatrix
        #GameMatrix is a textual representation of the game
        gameMatrix = self.setGameMatrix(self.board_size)     

        #Set the persistent gamestate which can be acessed throughout the project
        gameState = gamestate(self.board_size, gameMatrix)
        gameState.isLoad = self.load
        gameState.isAI = self.AI
        gameState.autoPlay = self.autoPlay

        #If the load file setting isn't set, then we ignore any files to load
        #therefore, gamestate.loadfile = None
        if (self.loadFile != None):
            gameState.loadFile = self.loadFile

        #On AI, we can choose the player, so this is where we set the color
        gameState.playerSelected = self.playerSelected
        #Pass the gamestate into the gui class, to draw it
        boardGraphic = tkgui(gameState)
        tkgui.drawInitialBoard(boardGraphic)

class GameInitializer():
    #Read the config file to see what settings are to be sets
    def readConfig(self):
        #TODO: Expansion? At the moment, just recieves boardsize but in other parts of the code
        #We have to keep reading the config file.
        with open('configure.txt') as f:
            configContent = f.readlines()
        board_size = int(configContent[0])
        print(('Setting board size of ' + str(board_size)))
        return board_size

    #Parameters passed in from menugui as per user's choice
    #Sets whether we are going to load a game, or the AI player should wake up
    def run(self, load = None, AI = None, playerSelected = None, loadFile = None, autoPlay = None):
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
        
        #Grab the boardsize.
        #See readconfig()!! NOTE
        board_size = self.readConfig()

        #Pass the settings into the GameManager and begin playing
        gameInstanceBegins = GameManager(board_size, load, AI, playerSelected, loadFile, autoPlay)
        gameInstanceBegins.run()
