import pytest
import sys, os
from tkinter import IntVar
#Set path directory
sys.path.append("..")

#Import class we want to test
import menugui

def test_menugui_reset_ext_data_file1():
	#Change working directory
	os.chdir('..')
	print(os.getcwd())
	menugui.reset_ext_data_file('load_game.txt')
	filesize = os.path.getsize('ext_data/load_game.txt')
	assert filesize == 0, "test passed"

