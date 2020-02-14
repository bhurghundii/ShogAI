# -*- coding: utf-8 -*-
#Grab files from directory
#USE PYTHON 2
import glob
import subprocess
import os
import shutil


path = ''

files = [f for f in glob.glob(path + "storage/*.txt")]

for f in files:
    line = subprocess.check_output(['tail', '-1', f])
    #print(str(f).replace('.txt', ''))
    if '☖' in line:
        #Put it into Black
        originalfile = str(f)
        shutil.move(originalfile.replace('.txt', ''), "black/" + originalfile.replace('.txt', ''))
        shutil.move(f, "black/" + str(f))
    else:
        originalfile = str(f)
        shutil.move(originalfile.replace('.txt', ''), "white/" + originalfile.replace('.txt', ''))
        shutil.move(f, "white/" + str(f))
