#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 11:14:31 2019

@author: nk7g14
This file contains functions used to gather information from the
Neutron Star Interior Composition Explorer (NiCER) telescope on board the ISS
Nicer data may be found at:
    https://heasarc.gsfc.nasa.gov/FTP/nicer/data/obs/
    or
    ftp://heasarc.gsfc.nasa.gov/nicer/data/obs/
"""
import os
import logging
import re
import numpy as np
from astroquery.heasarc import Heasarc as h
from astropy.time import Time

import auxil as aux

def GetObservationListNICER(source_name):
    '''
    Obtains the list of observation from the nicer master catalogue on Heasarc
    '''
    try:
        obs_list = h.query_object(source_name, mission='nicermastr', fields='All')
        time_column = np.array(obs_list['TIME'], dtype=float)
        times = Time(time_column, format='mjd') #converting mjd to YEAR-MONTH
        times_iso = times.iso                   #Format for data download
        for i, time in enumerate(times_iso):
            result = re.findall(r'\d\d\d\d-\d\d', time)[0]
            result = result.replace('-', '_')
            times_iso[i] = result
        obs_list['FOLDER'] = times_iso #Corresponding folder for fetching data
        return obs_list
    except:
        logging.debug('Failed to get XMM observation list')


def DownloadEventFiles(source_name):
    '''
    #TODO Maybe change source_name to obs_list? not sure what is better atm
    Downloads all cleaned event files from NiCER Archive
    '''
    cwd = os.getcwd()   #Current Working Directory
    obs_list = GetObservationListNICER(source_name)

    for row in obs_list:
        obsID = row['OBSID']
        folder = row['FOLDER']

        url_cl_evt = 'https://heasarc.gsfc.nasa.gov/FTP/nicer/data/obs/{}/{}/xti/event_cl/ni{}_0mpu7_cl.evt.gz'.format(folder, obsID, obsID)
        url_cl_savepath = '{}/sources/{}/nicer/xti/ni{}_0mpu7_cl.evt.gz'.format(cwd, source_name, obsID)
        aux.FetchFile(url_cl_evt, url_cl_savepath)


def CreateSaveDirectories():
    os.makedirs('sources', exist_ok=True)
    os.makedirs('sources', exist_ok=True)
    os.makedirs('sources/{}'.format(source_name), exist_ok=True)
    os.makedirs('sources/{}/nicer'.format(source_name), exist_ok=True)
    os.makedirs('sources/{}/nicer/xti'.format(source_name), exist_ok=True)
    
def CleanUpgzFiles():
    aux.UnzipAllgzFiles('sources/{}/nicer/xti'.format(source_name))
    aux.RemoveAllgzFiles('sources/{}/nicer/xti'.format(source_name))


source_name = 'NGC1313'
CreateSaveDirectories()
DownloadEventFiles(source_name)
