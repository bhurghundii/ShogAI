'''
This script uses ShogAI's playing ability to generate a set of features and labels
ARG 1 : The name of file to extract and analysis
'''

from gameinitializer import GameInitializer
import sys, os, traceback
from ml.generateCSV import csvUtil as csvUtil

file = str(sys.argv[1])
try:

   print ('Preparing to load from ' + file) 
   f = open(file, "r")
   replaygame = f.read()
   f.close()

   f = open('ext_data/load_game.txt', "w")
   f.write(replaygame)
   f.close()
   print(os.getcwd())

   GameInitializer().run(True, False, None, file, True)


except Exception as e:
   traceback.print_exc(file=sys.stdout)
   print('Caught exception CTRL-C: Terminating ShogAI gracefully')