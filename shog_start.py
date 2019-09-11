# -*- coding: UTF-8 -*-
from shog_gamestate import shog_gamestate
from shog_gui import shog_gui

with open('configure.txt') as f:
    size_board = int(f.read())

class GameManager():

    def __init__(self, board_size):
        self.board_width = board_size
        self.board_height = board_size

    def run(self):
        #Load game board from standardlayout.txt and place here
        gameMatrix = [[0 for  x in range(self.board_width)] for y in range(self.board_height)]
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


            gameState = shog_gamestate(board_size, gameMatrix)
            gameState.run()

            boardGraphic = shog_gui(gameState)
            shog_gui.drawInitialBoard(boardGraphic)

def readConfig():
    #Read the config file to see what settings are to be sets
    #Expansion?
    with open('configure.txt') as f:
        configContent = f.read()
    board_size = int(configContent)
    return board_size

if __name__ == '__main__':
    print('Doing warm up functions like checking settings and params')
    board_size = readConfig()
    gameInstanceBegins = GameManager(board_size)
    gameInstanceBegins.run()
