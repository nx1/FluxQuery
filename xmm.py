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

def GetObservationListXMM(object_name):
    try:
        obs_list = h.query_object(object_name, mission='xmmssc', fields='All')
        return obs_list
    except:
        print('Failed to get XMM observation list')

def GetStartAndEndTimesXMM(observation_list):
    start_time = np.array(observation_list['TIME'])
    end_time = np.array(observation_list['END_TIME'])
    
    start_end = pd.DataFrame()
    start_end['START_TIME'] = start_time
    start_end['END_TIME'] = end_time
    return start_end
        
def GetFluxXMM_PN(observation_list):
    pn_flux = pd.DataFrame()
    pn1 = np.array(observation_list['PN_1_FLUX'])
    pn2 = np.array(observation_list['PN_2_FLUX'])
    pn3 = np.array(observation_list['PN_3_FLUX'])
    pn4 = np.array(observation_list['PN_4_FLUX'])
    pn5 = np.array(observation_list['PN_5_FLUX'])
    pn8 = np.array(observation_list['PN_8_FLUX'])
    pn9 = np.array(observation_list['PN_9_FLUX'])
    
    pn_flux['PN_1_FLUX'] = pn1
    pn_flux['PN_2_FLUX'] = pn2
    pn_flux['PN_3_FLUX'] = pn3
    pn_flux['PN_4_FLUX'] = pn4
    pn_flux['PN_5_FLUX'] = pn5
    pn_flux['PN_8_FLUX'] = pn8
    pn_flux['PN_9_FLUX'] = pn9
    return pn_flux

def GetFluxXMM_MOS1(observation_list):
    mos1_flux = pd.DataFrame()
    mos1_1 = np.array(observation_list['M1_1_FLUX'])
    mos1_2 = np.array(observation_list['M1_2_FLUX'])
    mos1_3 = np.array(observation_list['M1_3_FLUX'])
    mos1_4 = np.array(observation_list['M1_4_FLUX'])
    mos1_5 = np.array(observation_list['M1_5_FLUX'])
    mos1_8 = np.array(observation_list['M1_8_FLUX'])
    mos1_9 = np.array(observation_list['M1_9_FLUX'])
    
    mos1_flux['M1_1_FLUX'] = mos1_1
    mos1_flux['M1_2_FLUX'] = mos1_2
    mos1_flux['M1_3_FLUX'] = mos1_3
    mos1_flux['M1_4_FLUX'] = mos1_4
    mos1_flux['M1_5_FLUX'] = mos1_5
    mos1_flux['M1_8_FLUX'] = mos1_8
    mos1_flux['M1_9_FLUX'] = mos1_9

    return mos1_flux

def GetFluxXMM_MOS2(observation_list):
    mos2_flux = pd.DataFrame()
    mos2_1 = np.array(observation_list['M2_1_FLUX'])
    mos2_2 = np.array(observation_list['M2_2_FLUX'])
    mos2_3 = np.array(observation_list['M2_3_FLUX'])
    mos2_4 = np.array(observation_list['M2_4_FLUX'])
    mos2_5 = np.array(observation_list['M2_5_FLUX'])
    mos2_8 = np.array(observation_list['M2_8_FLUX'])
    mos2_9 = np.array(observation_list['M2_9_FLUX'])
    
    mos2_flux['M2_1_FLUX'] = mos2_1
    mos2_flux['M2_2_FLUX'] = mos2_2
    mos2_flux['M2_3_FLUX'] = mos2_3
    mos2_flux['M2_4_FLUX'] = mos2_4
    mos2_flux['M2_5_FLUX'] = mos2_5
    mos2_flux['M2_8_FLUX'] = mos2_8
    mos2_flux['M2_9_FLUX'] = mos2_9
    return mos2_flux
    
def GetFluxXMM(observation_list):
    '''
    For this mission, the fluxes for XMM are given for the basic bands:
        Flux band 1 = 0.2 - 0.5 keV (soft)
        Flux band 2 = 0.5 - 1.0 keV (soft)
        Flux band 3 = 1.0 - 2.0 keV (soft)
        Flux band 4 = 2.0 - 4.5 keV (hard)
        Flux band 5 = 4.5 - 12.0 keV (hard)
        
    We also have the broad energy bands given by:
        Flux band 6 = 0.2 - 2.0 keV (N/A)
        Flux band 7 = 2.0 - 12.0 keV (N/A)
        Flux band 8 = 0.2 - 12.0 keV
        Flux band 9 = 0.5 - 4.5 keV
    '''
    flux_pn = GetFluxXMM_PN(observation_list)
    flux_mos1 = GetFluxXMM_MOS1(observation_list)
    flux_mos2 = GetFluxXMM_MOS2(observation_list)
    mapping = [flux_pn, flux_mos1, flux_mos2]
    all_fluxes = pd.concat(mapping, axis=1)
    return all_fluxes

def PlotAllFluxesXMM(observation_list):
    flux = GetFluxXMM(observation_list)
    flux.plot()

def XMMComplete(source_name):
    observation_list = GetObservationListXMM(source_name)
    start_end = GetStartAndEndTimesXMM(observation_list)
    aux.PlotStartAndEndTimes(start_end)
    PlotAllFluxesXMM(observation_list)