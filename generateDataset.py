from gameinitializer import GameInitializer
import sys, os, traceback
from ml.generateCSV import csvUtil as csvUtil

#/home/ubuntu/Documents/Shogi-DISS/src/ml/storage/tmp-2-6.csa.txt

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv[1]))
file = str(sys.argv[1])
try:

   print ('Preparing to load from ' + file) 
   f = open(file, "r")
   replaygame = f.read()
   f.close()

   f = open('ext_data/load_game.txt', "w")
   f.write(replaygame)
   f.close()
   #TODO: AUTOMATIC FULL RUN SO WE CAN SPEED THIS SHIT
   print(os.getcwd())

   GameInitializer().run(True, False, None, file, True)


except Exception as e:
   traceback.print_exc(file=sys.stdout)
   print('Caught exception CTRL-C: Terminating ShogAI gracefully')