#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 12:21:30 2019

@author: nk7g14
FluxQuery is an attempt to provide long term x-ray light curves for a given
source by querying a variety of x-ray missions, historical and current.

How it will work:
    fluxquery.query('NGC1313') #Returns a missions and observations etc
    fluxquery.xray.lightcurve('NGC1313')
    fluxquery

USEFUL COMMANDS
h.query_mission_list()
table.colnames
table.show_in_browser(jsviewer=True)

Missions with time given as ['TIME']:
    xmmssc, NUMASTER, CHANMASTER, RASS2RXS, fermilasp, suzaxislog, nicermastr
Missions with time given as ['START_TIME']:
    swiftmastr, mpcraw
    
The source position (in the XRT co-ordinate frame) used for these products was:
RA (J2000.0) = 49.5839 degrees, Dec (J2000.0) =-66.4864 degrees.

______ _            _____                       
|  ___| |          |  _  |                      
| |_  | |_   ___  _| | | |_   _  ___ _ __ _   _ 
|  _| | | | | \ \/ / | | | | | |/ _ \ '__| | | |
| |   | | |_| |>  <\ \/' / |_| |  __/ |  | |_| |
\_|   |_|\__,_/_/\_\\_/\_\\__,_|\___|_|   \__, |
                                           __/ |
                                          |___/	0.1
"""
#TODO change function names to lowercase_underscore
import matplotlib.pyplot as plt
import pandas as pd
import logging
from collections import OrderedDict

import auxil as aux
import xmm
import swift
import swift_downloader
import swift_uvot
import nicer

logging.basicConfig(level=logging.NOTSET, format=' %(asctime)s -- %(message)s')
logger = logging.getLogger('my-logger')
logger.propagate = False

def Query(source_name):
    missions = OrderedDict([
            ('XMM-Newton','xmmssc'),
            ('Swift','swiftmstr'),
            ('NiCER', 'nicermastr'),
            ('RXTE', 'xtemaster'),
            ('NuSTAR', 'numaster'),
            ('Chandra', 'chanmaster'),
            ('ROSAT', 'rass2rxs'),
            ('SUZAKU', 'suzamaster'),
            ('MAXI', 'maximaster'),
            ('INTEGRAL', 'intscwpub')
            ])
    
    observation_lists = OrderedDict()
    
    for mission_name, mission in missions.items():
        observation_list = aux.GetObservationList(source_name, mission)
        observation_lists[mission_name] = observation_list
    
    print('============================================================')
    print('Results for source:', source_name)
    header = ['Mission', '#Observations', 'Earliest obs', 'Latest obs']
    spacing = '{:<15} {:<15} {:<15} {:<15}'
    print(spacing.format(*header))
    
    for mission_name, observation_list in observation_lists.items():
        earliest_mjd, latest_mjd = aux.GetEarliestAndLatestFromObsList(observation_list)
        earliest = round(aux.mjd2year(earliest_mjd), 3)
        latest = round(aux.mjd2year(latest_mjd), 3)
        try:
            row = [mission_name, len(observation_list), earliest, latest]
        except TypeError: #Nontype has no length
            row = [mission_name, 'N/A', 'N/A', 'N/A']
        print(spacing.format(*row))
    print('============================================================')


def PlotAllFluxes(source_name):    
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
                         capsize=0.5, marker='None', ls='none', label=pn_flux, c='b')
            ax[1].errorbar(df['START_TIME'], df[mos1_flux], yerr=df[mos1_flux_err],
                         capsize=0.5, marker='None', ls='none', label=mos1_flux, c='b')
            ax[2].errorbar(df['START_TIME'], df[mos2_flux], yerr=df[mos2_flux_err],
                         capsize=0.5, marker='None', ls='none', label=mos2_flux, c='b')
    
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
# source_name = 'NGC1313'
# swift_downloader.Complete(source_name)
# NICERComplete(source_name)
# PlotAllFluxes(source_name)
# Query(source_name)