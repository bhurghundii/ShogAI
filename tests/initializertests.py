import pytest
import sys, os
from tkinter import IntVar
#Set path directory
sys.path.append("..")

#Import class we want to test
from gameinitializer import GameInitializer, GameManager

#Check if we can get a board_size
def test_GameInitializer_readConfig_boardsize():
	#Change working directory
	os.chdir('..')
	boardsize = GameInitializer().readConfig()
	assert boardsize == 9,"test passed"

#Check if we can get settings
def test_GameInitializer_readConfig_allconfigs():
	#Change working directory
	os.chdir('..')
	config = GameInitializer().readConfig()
	assert config.board_size == 9,"test passed"
	assert config.debug == 1,"test passed"
	assert config.showgame == 1, "test passed"

#Check if we can get settings
def test_GameManager_setGameMatrix1():
	#Change working directory
	os.chdir('..')
	gamematrix = GameManager(9).setGameMatrix(9)
	print(gamematrix)
	assert gamematrix == 9,"test passed"


