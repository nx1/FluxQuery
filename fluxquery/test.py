#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 11:58:07 2019

@author: nk7g14
"""

import os
from collections import OrderedDict

from astropy.coordinates import SkyCoord

import auxil as aux
import xmm
import swift
import nicer
import rxte

class Source(xmm.XMM, swift.SWIFT, nicer.NICER, rxte.RXTE):
    def __init__(self, SOURCE_NAME):
        self.SOURCE_NAME = SOURCE_NAME
        self._CreateSaveDirectories()
        coords = SkyCoord.from_name(SOURCE_NAME)
        self.SOURCE_RA = coords.ra.deg
        self.SOURCE_DEC = coords.dec.deg
        
        self.LIGHTCURVE_XMM = None
        self.LIGHTCURVE_SWIFT_UVOT = None
        self.LIGHTCURVE_SWIFT_XRT = None
        self.LIGHTCURVE_NICER = None
        self.LIGHTCURVE_RXTE = None
        self.LIGHTCURVES = [self.LIGHTCURVE_XMM, self.LIGHTCURVE_SWIFT_UVOT,
                            self.LIGHTCURVE_SWIFT_XRT, self.LIGHTCURVE_NICER,
                            self.LIGHTCURVE_RXTE]
        
        super(Source, self).__init__()
        
    def __repr__(self):
        return 'Source(%r RA: %r DEC: %r)' % (self.SOURCE_NAME,
                      self.SOURCE_RA, self.SOURCE_DEC)
        
    def query(self):
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
            observation_list = aux.GetObservationList(self.SOURCE_NAME, mission)
            observation_lists[mission_name] = observation_list
        
        print('============================================================')
        print('Results for source:', self.SOURCE_NAME)
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
        

    def _CreateSaveDirectories(self):
        #Basic directories
        os.makedirs('sources', exist_ok=True)
        os.makedirs('sources/{}'.format(self.SOURCE_NAME), exist_ok=True)
        #SWIFT Directories
        os.makedirs('sources/{}/swift'.format(self.SOURCE_NAME), exist_ok=True)
        os.makedirs('sources/{}/swift/xrt'.format(self.SOURCE_NAME), exist_ok=True)
        os.makedirs('sources/{}/swift/uvot'.format(self.SOURCE_NAME), exist_ok=True)
        os.makedirs('sources/{}/swift/uvot/img'.format(self.SOURCE_NAME), exist_ok=True)
        os.makedirs('sources/{}/swift/uvot/cat'.format(self.SOURCE_NAME), exist_ok=True)
        #NiCER directories
        os.makedirs('sources/{}/nicer'.format(self.SOURCE_NAME), exist_ok=True)
        os.makedirs('sources/{}/nicer/xti'.format(self.SOURCE_NAME), exist_ok=True)
        #RXTE directories
        os.makedirs('sources/{}/rxte'.format(self.SOURCE_NAME), exist_ok=True)


if __name__ == '__main__':
    ngc1313 = Source('NGC1313')
    m82 = Source('M82')
    ngc55 = Source('NGC55')
    ngc300 = Source('NGC300')
    ngc5907 = Source('NGC5907')



'''
#TESTING CODE
for i in dir(ngc1313):
    print('ngc1313.'+i+'()')

ngc1313.NICER_AppendFolderToObsList()
ngc1313.NICER_CleanUpgzFiles()
ngc1313.NICER_Complete()
ngc1313.NICER_DownloadEventFiles()
ngc1313.NICER_GetZeroTime()
ngc1313.NICER_OBS_LIST()
ngc1313.NICER_PlotLightCurve()
ngc1313.NICER_ReadLightCurve()
ngc1313.NICER_xselect()

ngc1313.RXTE_Complete()
ngc1313.RXTE_DownloadAllObservations()
ngc1313.RXTE_GetAllCounts()
ngc1313.RXTE_GetCounts()
ngc1313.RXTE_GetCountsQ6VPcu()
ngc1313.RXTE_GetCountsVpXPcu()
ngc1313.RXTE_GetCountsXPcu()
ngc1313.RXTE_GetcountsGood()
ngc1313.RXTE_MergeDataframeDictionary()
ngc1313.RXTE_OBS_LIST
ngc1313._RXTE_DownloadObservation()

ngc1313.SOURCE_DEC
ngc1313.SOURCE_NAME
ngc1313.SOURCE_RA

ngc1313.SWIFT_CleanUpgzFiles()
ngc1313.SWIFT_CreateSaveDirectories()
ngc1313.SWIFT_DownloadEventFiles()
ngc1313.SWIFT_GetStartTimes()
ngc1313.SWIFT_UVOT_GetAllFluxes()
ngc1313.SWIFT_UVOT_GetFluxesFromCatFile()
ngc1313.SWIFT_UVOT_GetObsIDFromCatFile()

ngc1313.XMM_GetFlux()
ngc1313.XMM_GetFlux_MOS1()
ngc1313.XMM_GetFlux_MOS2()
ngc1313.XMM_GetFlux_PN()
ngc1313.XMM_GetLightcurve()
ngc1313.XMM_GetStartAndEndTimes()
ngc1313.XMM_OBS_LIST

ngc1313._CreateSaveDirectories()


ngc1313.query()
ngc1313.swift_obs_list()
'''