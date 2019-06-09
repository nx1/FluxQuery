#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 12:21:30 2019

@author: nk7g14
FluxQuery is an attempt to provide long term x-ray light curves for a given
source by querying a variety of x-ray missions, historical and current.

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
"""

''' USEFUL COMMANDS
h.query_mission_list()
table.colnames
table.show_in_browser(jsviewer=True)
'''

'''
Missions with time given as ['TIME']:
    xmmssc, NUMASTER, CHANMASTER, RASS2RXS, fermilasp, suzaxislog, nicermastr
Missions with time given as ['START_TIME']:
    swiftmastr, mpcraw
    
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
'''

import xmm
import swift

source_name = 'NGC1313'

xmm.XMMComplete(source_name)
swift.SWIFTXRTComplete(source_name)