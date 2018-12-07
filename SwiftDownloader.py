#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 13:56:29 2018

@author: nk7g14
"""
from astroquery.heasarc import Heasarc
import numpy as np
import urllib.request


h = Heasarc()


sourceName = 'NGC1313'
mission = 'swiftmastr'



def Downloader(sourceName, mission):
    query = h.query_object(sourceName, mission, fields='OBSID')
    obsIDs = np.array(query['OBSID'], dtype='str')
    return obsIDs


    
frog = Downloader(sourceName, mission)

for i in frog:
    try:
        url = 'http://www.swift.ac.uk/archive/reproc/%s/xrt/event/sw%sxpcw3po_cl.evt.gz' % (i,i)
        urllib.request.urlretrieve(url, '%s.gz' %i)
    except urllib.error.HTTPError:
        print('could not find:', i)
        pass
        
    