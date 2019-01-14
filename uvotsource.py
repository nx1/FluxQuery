#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 11:10:24 2019

@author: nk7g14
"""

import subprocess

#def uvotsource(file):
    
    
    

lines = tuple(open("file.ls", 'r'))

for i in lines:
        print(i)
        subprocess.run('uvotsource image=%s srcreg=src.reg bkgreg=bkg.reg sigma=3.0 outfile=image.fits, ' %i, shell=True)
