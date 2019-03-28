#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 11:55:54 2018

@author: nk7g14
FluxQuery is an attempt to provide long term x-ray light curves for a given
source by querying a variety of x-ray missions, historical and current.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from astropy.time import Time
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

#Converts mjd time to decimal years
mjd2year = lambda times: Time(times, format='mjd').decimalyear

h = Heasarc()

object_name = 'NGC1313'

'''
Missions with time given as ['TIME']:
    xmmssc, NUMASTER, CHANMASTER, RASS2RXS, fermilasp, suzaxislog, nicermastr
Missions with time given as ['START_TIME']:
    swiftmastr, mpcraw
'''

#Dictionary for storing missions
M = {
     'XMM': 'xmmssc', 
     'Swift': 'swiftmastr', 
     'NuSTAR': 'NUMASTER', 
     'Chandra': 'CHANMASTER', 
     'ROSAT': 'RASS2RXS', 
     'Fermi': 'fermilasp', 
     'Einstein': 'mpcraw', 
     'SUZAKU': 'suzaxislog', 
     'NICER': 'nicermastr', 
     'SWIFTUV': 'swuvotssob',
     }  

T = {}  #Dictonary for storing table from queries

for i in M: #Running through mission dictionary and obtaining associated tables
    try:
        T[i] = h.query_object(object_name, mission=M[i], fields='All')
    except TypeError:   #Exception if there are no found observations
        print('TypeError:', i, '| probably due to no observation of source')
        pass
    
for i in T: #Running through tables to plot 
    try:
        if i == 'XMM':
            softPN = np.asarray(T[i]['PN_1_FLUX'] + T[i]['PN_2_FLUX'])
            hardPN = np.asarray(T[i]['PN_3_FLUX'] + T[i]['PN_4_FLUX'] + T[i]['PN_5_FLUX'])
            
            plt.scatter(mjd2year(np.array(T[i]['TIME'])), softPN,
                            marker='x', label= i + ' soft')
            plt.scatter(mjd2year(np.array(T[i]['TIME'])), hardPN,
                            marker='x', label=i +' hard')

        else:
            plt.scatter(mjd2year(np.array(T[i]['TIME'])),
                        np.zeros(len(np.array(T[i]['TIME']))), marker='x', label=i)
        
    except NameError:
        print('NameError:', i)
        pass
    
    except KeyError:
        print('KeyError, trying to use table header START_TIME')
        plt.scatter(mjd2year(np.array(T[i]['START_TIME'])),
                    np.zeros(len(np.array(T[i]['START_TIME']))), marker='x', label=i)
 

plt.ylim(0,1.1*np.nanmax(np.concatenate((softPN, hardPN))))

plt.title(object_name)
plt.xlabel('TIME')
plt.ylabel('Flux')
plt.legend()
