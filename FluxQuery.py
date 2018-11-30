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

'''
Name of Source
Desired Catalogs/Archives:
    HEASARC
    SDSS
    
Desired Mission(s)
    XMM-DR8:    xmmssc    http://xmmssc.irap.omp.eu/Catalogue/3XMM-DR8/3XMM_DR8.html
    SWUVOTSSOB:  SWUVOTSSOB https://heasarc.gsfc.nasa.gov/w3browse/all/swuvotssob.html
    use the swift one with observation IDs

get start time column:
    XMM-DR8:'TIME'
    SWUVOTSSOB: 'TIME' (UT)
    
get fluxes in hard and soft
    XMM-DR8:    
        soft: 
            ['PN_1_FLUX]    0.2-0.5
            + ['PN_2_FLUX'] 0.5-1.0
                        
        hard:
            ['PN_3_FLUX]    1.0-2.0  
            + ['PN_4_FLUX'] 2.0-4.5
            + ['PN_5_FLUX'] 4.5-12.0
                             
    SWUVOTSSOB:
get hardness ratio in hard and soft
    XMM-DR8:    
        soft: 
            ['PN_HR1']      0.2 - 0.5 and 0.5 - 1.0
        hard:
            ['PN_HR2']      0.5-1.0 and 1.0-2.0
            + ['PN_HR3']    1.0-2.0 and 2.0-4.5
            + ['PN_HR4']    2.0-4.5 and 4.5-12.0
                
    SWUVOTSSOB:

plotem

'''

##############USEFUL COMMANDS####################
'''
h.query_mission_list()
table.colnames
table.show_in_browser(jsviewer=True)
'''

def mjd2year(times):    #Converts mjd time to decimal years
    return Time(times, format='mjd').decimalyear


h = Heasarc()



object_name = 'NGC1313'

mission = 'xmmssc'
mission2 = 'SWUVOTSSOB'

table = h.query_object(object_name, mission=mission, fields='All')
table2 = h.query_object(object_name, mission=mission2, fields='All')

plt.title(object_name)
plt.xlabel('TIME')

plt.scatter(mjd2year(np.array(table['TIME'])), 
            np.zeros(len(np.array(table['TIME']))), marker='x', label=mission)

plt.scatter(mjd2year(np.array(table2['TIME'])), 
            np.zeros(len(np.array(table2['TIME']))), marker='x', label=mission2)
plt.legend()
