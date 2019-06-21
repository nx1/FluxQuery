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


The source position (in the XRT co-ordinate frame) used for these products was:
RA (J2000.0) = 49.5839 degrees, Dec (J2000.0) =-66.4864 degrees.
'''

import xmm
import swift
import auxil as aux

source_name = 'NGC1313'
def XMMComplete(source_name):
    observation_list = xmm.GetObservationListXMM(source_name)
    if observation_list == None:
        print('Observation list not found, exiting.')
    else:
        xmm.PlotAllFluxesXMM(source_name, observation_list)#

def SWIFTXRTComplete(source_name):
    observation_list = swift.GetObservationList(source_name)
    start_end = swift.GetStartAndEndTimes(observation_list)
    aux.PlotStartAndEndTimes(start_end)

def SWIFTUVOTComplete(source_name):
    observation_list = swift.GetObservationList(source_name)
    start_end = swift.GetStartAndEndTimes(observation_list)
    aux.PlotStartAndEndTimes(start_end)




XMMComplete(source_name)
# SWIFTXRTComplete(source_name)