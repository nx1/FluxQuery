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


If you want to perform more involved analysis and reduce your own data check:
https://heasarc.gsfc.nasa.gov/docs/nicer/data_analysis/nicer_analysis_guide.html

Process for creating a NiCER lightcurve:
    1) Download all the cleaned event files from heasarc
    2) Create list file for use in xselect
    XSELECT:
        3) read events "@file.ls"
        4) set binsize pha_cutoff 200 1200
        5) extract curve
        6) save curve lightcurve.lc
    7) read the output into python.

"""
import os
import logging
from pathlib import Path
import re
import numpy as np
from astroquery.heasarc import Heasarc as h
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.time import Time
import subprocess
import pandas as pd

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
        logging.debug('Failed to get NICER observation list')
        return None


def DownloadEventFiles(source_name):
    '''
    #TODO Maybe change source_name to obs_list? not sure what is better atm
    Downloads all cleaned event files from NiCER Archive
    '''
    cwd = os.getcwd()   #Current Working Directory
    obs_list = GetObservationListNICER(source_name)
    if obs_list == None:
        return logging.debug('No observation_list found, nothing to download')
    else:
        pass

    for row in obs_list:
        obsID = row['OBSID']
        folder = row['FOLDER']
        logging.debug('Downloading %s', obsID)
        url_cl_evt = 'https://heasarc.gsfc.nasa.gov/FTP/nicer/data/obs/{}/{}/xti/event_cl/ni{}_0mpu7_cl.evt.gz'.format(folder, obsID, obsID)
        url_cl_savepath = '{}/sources/{}/nicer/xti/ni{}_0mpu7_cl.evt.gz'.format(cwd, source_name, obsID)
        aux.FetchFile(url_cl_evt, url_cl_savepath)

def xselect(source_name):
    lc_path = 'sources/{}/nicer/xti/lightcurve.lc'.format(source_name)
    if Path(lc_path).is_file():
        return logging.debug('Nicer lightcurve file already exists: %s', lc_path)
    else:
        pass
    home_dir = os.getcwd()
    os.chdir('sources/{}/nicer/xti'.format(source_name))

    binsize = 100   #Binsize in seconds
    low_cutoff = 200 #Low end cutoff frequency in eV
    high_cutoff = 1000 #High end cutoff frequency in eV

    script_file = open('script.xcm', 'w')

    script_text = '''NICER
read event "@file.ls"
./
yes
set binsize {}
filter pha_cutoff {} {}
extract curve
save curve lightcurve.lc
exit
n
'''.format(binsize, low_cutoff, high_cutoff)
    script_file.write(script_text)
    script_file.close()
    subprocess.call(['xselect < script.xcm'], shell=True)
    os.chdir(home_dir)

def GetZeroTime(source_name):
    """
    Obtains the earliest
    """
    obs_list = h.query_object(source_name, mission='nicermastr', fields='All')
    time_column = np.array(obs_list['TIME'], dtype=float)
    zero_time = np.min(time_column)
    return zero_time

def ReadLightCurve(source_name):
    df = pd.DataFrame()
    zero_time = GetZeroTime(source_name)
    lightcurve_path = 'sources/{}/nicer/xti/lightcurve.lc'.format(source_name)
    data = fits.open(lightcurve_path)
    
    time = np.array(data[1].data['TIME'], dtype='float')
    time_mjd = aux.s2mjd(time) + zero_time
    
    df['TIME'] = time
    df['TIME_MJD'] = time_mjd
    df['RATE'] = np.array(data[1].data['RATE'], dtype='float')
    df['RATE_ERROR'] = np.array(data[1].data['ERROR'], dtype='float')
    return df

def PlotLightCurve(source_name):
    lc = ReadLightCurve(source_name)
    plt.errorbar(x=lc['TIME_MJD'], y=lc['RATE'], yerr=lc['RATE_ERROR'],
                 capsize=0.5, marker='None', ls='none', label='NiCER')

def CreateSaveDirectories(source_name):
    logging.debug('Creating NICER save directories')
    os.makedirs('sources', exist_ok=True)
    os.makedirs('sources', exist_ok=True)
    os.makedirs('sources/{}'.format(source_name), exist_ok=True)
    os.makedirs('sources/{}/nicer'.format(source_name), exist_ok=True)
    os.makedirs('sources/{}/nicer/xti'.format(source_name), exist_ok=True)

def CleanUpgzFiles(source_name):
    logging.debug('Cleaning NICER gz files')
    aux.UnzipAllgzFiles('sources/{}/nicer/xti'.format(source_name))
    aux.RemoveAllgzFiles('sources/{}/nicer/xti'.format(source_name))

def Complete():
    CreateSaveDirectories(source_name)
    DownloadEventFiles(source_name)
    CleanUpgzFiles(source_name)
    aux.CreateListFile('sources/{}/nicer/xti'.format(source_name), 'evt')
    xselect(source_name)
    PlotLightCurve(source_name)

# source_name = 'NGC1313'
# Complete()
