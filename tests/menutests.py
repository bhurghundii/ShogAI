import pytest
import sys, os
from tkinter import IntVar
#Set path directory
sys.path.append("..")

#Import class we want to test
import menugui

'''
TEST REMOVED AS THIS TEST DOESN'T ENFORCE GOOD PEP8 STANDARDS
THE FUNCTION TO TEST DOESN'T NEED RETURNS WHEN IT'S VOID 

def test_menugui_reset_ext_data_file1():
	#Change working directory
	os.chdir('..')
	print(os.getcwd())
	menugui.reset_ext_data_file('load_game.txt')
	filesize = os.path.getsize('ext_data/load_game.txt')
	assert filesize == 0, "test passed"
'''

'''
In light of this, it might be worth researching mock
It mocks print statements
'''