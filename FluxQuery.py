#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 11:55:54 2018

@author: nk7g14
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from astropy.time import Time
import os
from astroquery.heasarc import Heasarc

#Name of Source
#Desired Catalogs/Archives:
    #HEASARC;
    #SDSS
#Desired Mission(s)
    #XMM-DR8:    xmmssc
    #swuvotssc:  swuvotssc

#get start time column:
    #XMM-DR8:     
    #swuvotssc
#get fluxes
#plotem
#

##############USEFUL COMMANDS####################
'''
h.query_mission_list()
table.colnames

'''

h = Heasarc()

object_name = 'NGC1313'
missions = ['swuvotssc', 'xmmssc']
mission = 'swuvotssc'

table = h.query_object(object_name, mission=mission, fields='All')

