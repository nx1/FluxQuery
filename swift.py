#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 12:22:30 2019

@author: nk7g14
"""
import pandas as pd
import numpy as np
from astroquery.heasarc import Heasarc

import auxil as aux

h = Heasarc()

def GetObservationListSWIFTXRT(object_name):
    try:
        obs_list = h.query_object(object_name, mission='swiftmastr', fields='All')
        return obs_list
    except:
        print('Failed to get Swift observation list')

def GetObservationIDSWIFT(object_name):
    '''
    Returns array of observation IDS for a given sourceName and Mission
    Currently only works for missions with column name ['OBSID']
    '''
    query = h.query_object(object_name, 'swiftmastr', fields='OBSID')
    obsIDs = np.array(query['OBSID'], dtype='str')
    return obsIDs
    
def GetStartAndEndTimesSWIFTXRT(observation_list):
    start_time = np.array(observation_list['START_TIME'])
    xrt_exposure = np.array(observation_list['XRT_EXPOSURE']) / (24*3600)
    end_time = start_time + xrt_exposure
    start_end = pd.DataFrame()
    start_end['START_TIME'] = start_time
    start_end['END_TIME'] = end_time
    return start_end

#TODO Find a way of getting swift-xrt fluxes.
    
def SWIFTXRTComplete(source_name):
    observation_list = GetObservationListSWIFTXRT(source_name)
    start_end = GetStartAndEndTimesSWIFTXRT(observation_list)
    aux.PlotStartAndEndTimes(start_end)
