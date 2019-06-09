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

def GetObservationList(object_name):
    try:
        obs_list = h.query_object(object_name, mission='swiftmastr', fields='All')
        return obs_list
    except:
        print('Failed to get Swift observation list')

def GetObservationID(object_name):
    '''
    Returns array of observation IDS for a given sourceName and Mission
    Currently only works for missions with column name ['OBSID']
    '''
    query = h.query_object(object_name, 'swiftmastr', fields='OBSID')
    obsIDs = np.array(query['OBSID'], dtype='str')
    return obsIDs
    
def GetStartTimes(observation_list):
    obsID = np.array(observation_list['OBSID'], dtype='str')
    start_time = np.array(observation_list['START_TIME'])
    df_starts = pd.DataFrame()
    df_starts['OBSID'] = obsID
    df_starts['START_TIME'] = start_time
    return df_starts

def GetEndTimes(observation_list):
    start_time = GetStartTimes(observation_list)
    xrt_exposure = np.array(observation_list['XRT_EXPOSURE']) / (24*3600)
    end_time = start_time['START_TIME'] + xrt_exposure
    df_ends = pd.DataFrame()
    df_ends['OBSID'] = start_time['OBSID']
    df_ends['END_TIME'] = end_time
    return df_ends

def GetStartAndEndTimes(observation_list):
    start_time = GetStartTimes(observation_list)
    end_time = GetEndTimes(observation_list)
    start_end = pd.DataFrame()
    start_end['OBSID'] = start_time['OBSID']
    start_end['START_TIME'] = start_time['START_TIME']
    start_end['END_TIME'] = end_time['END_TIME']
    return start_end

#TODO Find a way of getting swift-xrt fluxes.
    
def SWIFTXRTComplete(source_name):
    observation_list = GetObservationList(source_name)
    start_end = GetStartAndEndTimes(observation_list)
    aux.PlotStartAndEndTimes(start_end)
