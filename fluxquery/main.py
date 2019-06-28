#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 12:21:30 2019

______ _            _____                       
|  ___| |          |  _  |                      
| |_  | |_   ___  _| | | |_   _  ___ _ __ _   _ 
|  _| | | | | \ \/ / | | | | | |/ _ \ '__| | | |
| |   | | |_| |>  <\ \/' / |_| |  __/ |  | |_| |
\_|   |_|\__,_/_/\_\\_/\_\\__,_|\___|_|   \__, |
                                           __/ |
                                          |___/	0.1

@author: nk7g14
FluxQuery is an attempt to provide long term x-ray light curves for a given
source by querying a variety of x-ray missions, historical and current.

USEFUL COMMANDS
h.query_mission_list()
table.colnames
table.show_in_browser(jsviewer=True)

"""

'''

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
import matplotlib.pyplot as plt
import pandas as pd
import logging

import auxil as aux
import xmm
import swift
import swift_downloader
import swift_uvot
import nicer
import rxte
import nustar
import chandra
import rosat
import maxi
import suzaku
import integral

logging.basicConfig(level=logging.NOTSET, format=' %(asctime)s -- %(message)s')

def Query(source_name):
    #TODO find a way of putting this crap in a loop
    xmm_observation_list = xmm.GetObservationList(source_name)
    swift_observation_list = swift.GetObservationList(source_name)
    nicer_observation_list = nicer.GetObservationList(source_name)
    rxte_observation_list = rxte.GetObservationList(source_name)
    nustar_observation_list = nustar.GetObservationList(source_name)
    chandra_observation_list = chandra.GetObservationList(source_name)
    rosat_observation_list = rosat.GetObservationList(source_name)
    suzaku_observation_list = suzaku.GetObservationList(source_name)
    maxi_observation_list = maxi.GetObservationList(source_name)
    integral_observation_list = integral.GetObservationList(source_name)
    
    
    obs_list_array = [xmm_observation_list, swift_observation_list,
                      nicer_observation_list, rxte_observation_list,
                      nustar_observation_list, chandra_observation_list,
                      rosat_observation_list, suzaku_observation_list,
                      maxi_observation_list, integral_observation_list]
    
    mission_names_array = ['XMM-Newton', 'Swift', 'NiCER', 'RXTE', 'NuSTAR',
                     'Chandra', 'ROSAT', 'SUZAKU', 'MAXI', 'INTEGRAL']
    
    print('============================================================')
    print('Results for source:', source_name)
    header = ['Mission', '#Observations', 'Earliest obs', 'Latest obs']
    spacing = '{:<15} {:<15} {:<15} {:<15}'
                        
    print(spacing.format(*header))
    
    for obs_list, mission_name in zip(obs_list_array, mission_names_array):
        
        earliest_mjd, latest_mjd = aux.GetEarliestAndLatestFromObsList(obs_list)
        earliest = round(aux.mjd2year(earliest_mjd), 3)
        latest = round(aux.mjd2year(latest_mjd), 3)
        try:
            row = [mission_name, len(obs_list), earliest, latest]
        except TypeError: #Nontype has no length
            row = [mission_name, 'N/A', 'N/A', 'N/A']
        print(spacing.format(*row))
    print('============================================================')
    
    
def PlotAllFluxes(source_name):
    Query(source_name)
    def PlotAllFluxesXMM(source_name):
        observation_list = xmm.GetObservationList(source_name)
        if observation_list == None:
            return print('Observation list not found, exiting.')
        else:
            pass
        start_end = xmm.GetStartAndEndTimesXMM(observation_list)
        flux = xmm.GetFluxXMM(observation_list)
        
        df = pd.concat([start_end, flux], axis=1)
        df = df.sort_values(by='START_TIME')

        flux_bands = [1, 2, 3, 4, 5, 8, 9]
        for i in flux_bands:
            pn_flux = 'PN_{}_FLUX'.format(i)
            pn_flux_err = 'PN_{}_FLUX_ERROR'.format(i)
            mos1_flux = 'M1_{}_FLUX'.format(i)
            mos1_flux_err = 'M1_{}_FLUX_ERROR'.format(i)
            
            mos2_flux = 'M2_{}_FLUX'.format(i)
            mos2_flux_err = 'M2_{}_FLUX_ERROR'.format(i)
            
            ax[0].errorbar(df['START_TIME'], df[pn_flux], yerr=df[pn_flux_err],
                         capsize=0.5, marker='None', ls='none', label=pn_flux)
            ax[1].errorbar(df['START_TIME'], df[mos1_flux], yerr=df[mos1_flux_err],
                         capsize=0.5, marker='None', ls='none', label=mos1_flux)
            ax[2].errorbar(df['START_TIME'], df[mos2_flux], yerr=df[mos2_flux_err],
                         capsize=0.5, marker='None', ls='none', label=mos2_flux)
    
        ax[0].set_ylabel('XMM PN \n Flux $\mathrm{erg \ s^{-1}}$')
        ax[1].set_ylabel('XMM MOS1 \n Flux $\mathrm{erg \ s^{-1}}$')
        ax[2].set_ylabel('XMM MOS2 \n Flux $\mathrm{erg \ s^{-1}}$')

        # ax[0].legend()
        # ax[1].legend()
        # ax[2].legend()
    
    def PlotAllFluxesSWIFTUVOT(source_name):
        flux_df = swift_uvot.GetAllFluxes(source_name)
        
        ax[3].set_ylabel('SWIFT UVOT \n Flux $\mathrm{erg \ s^{-1} \ cm^{-2} \ angstrom^{-1}}$')
        ax[3].errorbar(flux_df['START_TIME'], flux_df['MEAN_FLUX'],
                      yerr=flux_df['MEAN_FLUX_ERR'], capsize=0.5, marker='None', ls='none')
        
    def PlotAllFluxesNICER(source_name):
        lc = nicer.ReadLightCurve(source_name)
        ax[4].set_ylabel('NICER \n Counts')
        ax[4].set_xlabel('Time (MJD)')
        ax[4].errorbar(x=lc['TIME_MJD'], y=lc['RATE'], yerr=lc['RATE_ERROR'],
                 capsize=0.5, marker='None', ls='none', label='NiCER')
    
    
    fig, ax = plt.subplots(5, sharex=True, num=0)
    plt.suptitle(source_name)
    PlotAllFluxesXMM(source_name)
    PlotAllFluxesSWIFTUVOT(source_name)
    PlotAllFluxesNICER(source_name)

def NICERComplete(source_name):
    nicer.CreateSaveDirectories(source_name)
    nicer.DownloadEventFiles(source_name)
    nicer.CleanUpgzFiles(source_name)
    aux.CreateListFile('sources/{}/nicer/xti'.format(source_name), 'evt')
    nicer.xselect(source_name)


#FOR NGC1313 SPECIFY SPECIFIC COOORDS!
source_name = 'NGC1313'
# swift_downloader.Complete(source_name)
# NICERComplete(source_name)
# PlotAllFluxes(source_name)
Query(source_name)