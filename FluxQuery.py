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

object_name = 'NGC6946'

mission1 = ['xmmssc', 'XMM']        #XMM
mission2 = ['SWUVOTSSOB', 'Swift']  #Swift
mission3 = ['NUMASTER', 'NuSTAR']   #NuSTAR
mission4 = ['CHANMASTER', 'Chandra']#Chandra
mission5 = ['RASS2RXS', 'ROSAT']    #ROSAT
mission6 = ['fermilasp', 'Fermi']   #Fermi
mission7 = ['mpcraw', 'Einstein']   #Einstien
mission8 = ['suzaxislog', 'SUZAKU'] #SUZAKU




try: 
    table1 = h.query_object(object_name, mission=mission1[0], fields='All')
    table2 = h.query_object(object_name, mission=mission2[0], fields='All')
    table3 = h.query_object(object_name, mission=mission3[0], fields='All')
    table4 = h.query_object(object_name, mission=mission4[0], fields='All')
    table5 = h.query_object(object_name, mission=mission5[0], fields='All')
    table6 = h.query_object(object_name, mission=mission6[0], fields='All')
    table7 = h.query_object(object_name, mission=mission7[0], fields='All')
    table8 = h.query_object(object_name, mission=mission8[0], fields='All')
except TypeError:
    pass


try:
    plt.scatter(mjd2year(np.array(table1['TIME'])), 
                np.zeros(len(np.array(table1['TIME']))), marker='x', label=mission1[1])
    plt.scatter(mjd2year(np.array(table2['TIME'])), 
                np.zeros(len(np.array(table2['TIME']))), marker='x', label=mission2[1])
    plt.scatter(mjd2year(np.array(table3['TIME'])), 
                np.zeros(len(np.array(table3['TIME']))), marker='x', label=mission3[1])
    plt.scatter(mjd2year(np.array(table4['TIME'])), 
                np.zeros(len(np.array(table4['TIME']))), marker='x', label=mission4[1])
    plt.scatter(mjd2year(np.array(table5['TIME'])), 
                np.zeros(len(np.array(table5['TIME']))), marker='x', label=mission5[1])
    plt.scatter(mjd2year(np.array(table6['TIME'])), 
                np.zeros(len(np.array(table6['TIME']))), marker='x', label=mission6[1])
    plt.scatter(mjd2year(np.array(table7['START_TIME'])), 
                np.zeros(len(np.array(table7['START_TIME']))), marker='x', label=mission7[1])      
    plt.scatter(mjd2year(np.array(table8['TIME'])), 
                np.zeros(len(np.array(table8['TIME']))), marker='x', label=mission8[1])  
except NameError:
    pass

plt.title(object_name)
plt.xlabel('TIME')
plt.legend()
