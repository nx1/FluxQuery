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
    swuvotssc: TIME
    
get fluxes in hard and soft
    XMM-DR8:    
        soft: 
            ['PN_1_FLUX]    0.2-0.5
            + ['PN_2_FLUX'] 0.5-1.0
                        
        hard:
            ['PN_3_FLUX]    1.0-2.0  
            + ['PN_4_FLUX'] 2.0-4.5
            + ['PN_5_FLUX'] 4.5-12.0
                             
    swuvotssc:
get hardness ratio in hard and soft
    XMM-DR8:    
        soft: 
            ['PN_HR1']      0.2 - 0.5 and 0.5 - 1.0
        hard:
            ['PN_HR2']      0.5-1.0 and 1.0-2.0
            + ['PN_HR3']    1.0-2.0 and 2.0-4.5
            + ['PN_HR4']    2.0-4.5 and 4.5-12.0
                
    swuvotssc:

plotem

'''

##############USEFUL COMMANDS####################
'''
h.query_mission_list()
table.colnames
table.show_in_browser(jsviewer=True)

'''

h = Heasarc()

object_name = 'NGC1313'
missions = ['SWUVOTSSOB', 'xmmssc']
mission = 'SWUVOTSSOB'

table = h.query_object(object_name, mission=mission, fields='All')

