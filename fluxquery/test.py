#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 11:58:07 2019

@author: nk7g14
"""

import os
import logging
from collections import OrderedDict

from astropy.coordinates import SkyCoord

import auxil as aux
import xmm
import swift
import nicer

class Source(xmm.XMM, swift.SWIFT, nicer.NICER):
    def __init__(self, source_name):
        self.source_name = source_name
        self._CreateSaveDirectories()
        coords = SkyCoord.from_name(source_name)
        self.source_ra = coords.ra.deg
        self.source_dec = coords.dec.deg
        super(Source, self).__init__()
        
    def __repr__(self):
        return 'Source(%r RA: %r DEC: %r)' % (self.source_name,
                      self.source_ra, self.source_dec)
        
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
            observation_list = aux.GetObservationList(self.source_name, mission)
            observation_lists[mission_name] = observation_list
        
        print('============================================================')
        print('Results for source:', self.source_name)
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
        os.makedirs('sources/{}'.format(self.source_name), exist_ok=True)
        #SWIFT Directories
        os.makedirs('sources/{}/swift'.format(self.source_name), exist_ok=True)
        os.makedirs('sources/{}/swift/xrt'.format(self.source_name), exist_ok=True)
        os.makedirs('sources/{}/swift/uvot'.format(self.source_name), exist_ok=True)
        os.makedirs('sources/{}/swift/uvot/img'.format(self.source_name), exist_ok=True)
        os.makedirs('sources/{}/swift/uvot/cat'.format(self.source_name), exist_ok=True)
        #NiCER directories
        os.makedirs('sources/{}/nicer'.format(self.source_name), exist_ok=True)
        os.makedirs('sources/{}/nicer/xti'.format(self.source_name), exist_ok=True)
        #RXTE directories
        os.makedirs('sources/{}/rxte'.format(self.source_name), exist_ok=True)
    
ngc1313 = Source('NGC1313')
# ngc5408 = Source('ngc5408')

