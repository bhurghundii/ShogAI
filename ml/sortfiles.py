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
    if '☖' in line:
        #Put it into Black
        shutil.move(f, "black/" + str(f))
    else:
        shutil.move(f, "white/" + str(f))


#line = subprocess.check_output(['tail', '-1', filename])