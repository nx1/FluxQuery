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
    REFER TO EXCEL FILE
get hardness ratio in hard and soft
    REFER TO EXCEL FILE
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

object_name = 'ngc1313'

mission1 = ['xmmssc', 'XMM']        #XMM
mission2 = ['swiftmastr', 'Swift']  #Swift
mission3 = ['NUMASTER', 'NuSTAR']   #NuSTAR
mission4 = ['CHANMASTER', 'Chandra']#Chandra
mission5 = ['RASS2RXS', 'ROSAT']    #ROSAT
mission6 = ['fermilasp', 'Fermi']   #Fermi
mission7 = ['mpcraw', 'Einstein']   #Einstien
mission8 = ['suzaxislog', 'SUZAKU'] #SUZAKU
mission9 = ['nicermastr', 'NICER'] #SUZAKU




try: 
    table1 = h.query_object(object_name, mission=mission1[0], fields='All')
    table2 = h.query_object(object_name, mission=mission2[0], fields='All')
    table3 = h.query_object(object_name, mission=mission3[0], fields='All')
    table4 = h.query_object(object_name, mission=mission4[0], fields='All')
    table5 = h.query_object(object_name, mission=mission5[0], fields='All')
    table6 = h.query_object(object_name, mission=mission6[0], fields='All')
    table7 = h.query_object(object_name, mission=mission7[0], fields='All')
    table8 = h.query_object(object_name, mission=mission8[0], fields='All')
    table9 = h.query_object(object_name, mission=mission9[0], fields='All')
except TypeError:
    pass

######################XMM FLUXES#######################
softPN = np.asarray(table1['PN_1_FLUX'] + table1['PN_2_FLUX'])
hardPN = np.asarray(table1['PN_3_FLUX'] + table1['PN_4_FLUX'] + table1['PN_5_FLUX'])

######################ROSAT COUNT RATE#################
ROS_CR = np.asarray(table5['COUNT_RATE'])

try:
    plt.scatter(mjd2year(np.array(table1['TIME'])), softPN, 
                marker='x', label=mission1[1]+' soft')
 
    
    plt.scatter(mjd2year(np.array(table1['TIME'])), hardPN, 
                marker='x', label=mission1[1]+' hard')
    
    plt.scatter(mjd2year(np.array(table2['START_TIME'])), 
                np.zeros(len(np.array(table2['START_TIME']))), marker='x', label=mission2[1])
    
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
    
    plt.scatter(mjd2year(np.array(table9['TIME'])), 
                np.zeros(len(np.array(table9['TIME']))), marker='x', label=mission9[1])  
except NameError:
    pass   


plt.ylim(0,1.1*np.nanmax(np.concatenate((softPN, hardPN))))

plt.title(object_name)
plt.xlabel('TIME')
plt.ylabel('Flux')
plt.legend()
