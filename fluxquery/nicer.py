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
import subprocess
from pathlib import Path
import pandas as pd
import numpy as np
import re

import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.time import Time

import auxil as aux


class NICER:
    def __init__(self):
        super(NICER, self).__init__()
        self.NICER_OBS_LIST = aux.GetObservationList(self.SOURCE_NAME, 'nicermastr')
        
        
    def NICER_AppendFolderToObsList(self):
        '''
        The NiCER data archive saves the observations in folders with the
        structure of DDDD-MM and so in order to find the right folder
        for a given observation we need to convert MJD into this format.
        '''
        logging.debug('Appending DDDD-MM to NICER observation_list')
        time_column = np.array(self.NICER_OBS_LIST['TIME'], dtype=float)
        times = Time(time_column, format='mjd')
        times_iso = times.iso
        for i, time in enumerate(times_iso):
            result = re.findall(r'\d\d\d\d-\d\d', time)[0]
            result = result.replace('-', '_')
            times_iso[i] = result
        self.NICER_OBS_LIST['FOLDER'] = times_iso #Corresponding folder for fetching data

        
    def NICER_DownloadEventFiles(self):
        '''
        Downloads all cleaned event files from NiCER Archive
        '''
        cwd = os.getcwd()   #Current Working Directory
        if self.NICER_OBS_LIST == None:
            return logging.debug('No observation_list found, nothing to download')
        else:
            pass
    
        for row in self.NICER_OBS_LIST:
            obsID = row['OBSID']
            try:
                logging.debug('Tying to find FOLDER column')
                folder = row['FOLDER']
            except:
                logging.debug('Could not find FOLDER column, appending')
                self.NICER_AppendFolderToObsList()
            logging.debug('Downloading %s', obsID)
            url_cl_evt = 'https://heasarc.gsfc.nasa.gov/FTP/nicer/data/obs/{}/{}/xti/event_cl/ni{}_0mpu7_cl.evt.gz'.format(folder, obsID, obsID)
            url_cl_savepath = '{}/sources/{}/nicer/xti/ni{}_0mpu7_cl.evt.gz'.format(cwd, self.SOURCE_NAME, obsID)
            
            url_orb = 'https://heasarc.gsfc.nasa.gov/FTP/nicer/data/obs/{}/{}/auxil/ni{}.orb.gz'.format(folder, obsID, obsID)
            url_orb_savepath = '{}/sources/{}/nicer/xti/ni{}.orb.gz'.format(cwd, self.SOURCE_NAME, obsID)
            aux.FetchFile(url_cl_evt, url_cl_savepath)
            aux.FetchFile(url_orb, url_orb_savepath)

    def NICER_xselect(self):
        lc_path = 'sources/{}/nicer/xti/lightcurve.lc'.format(self.SOURCE_NAME)
        if Path(lc_path).is_file():
            return logging.debug('Nicer lightcurve file already exists: %s', lc_path)
        else:
            pass
        home_dir = os.getcwd()
        os.chdir('sources/{}/nicer/xti'.format(self.SOURCE_NAME))
        
        #TODO MAKE THESE PARAMETERS AJUSTABLE POSSIBLY in object settings
        binsize = 100   #Binsize in seconds
        low_cutoff = 200 #Low end cutoff frequency in eV
        high_cutoff = 1000 #High end cutoff frequency in eV
        
        script_file = open('script.xcm', 'w')
    
        script_text = '''NICER
    read events "@file.ls"
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
    
    def NICER_GetZeroTime(self):
        """
        Obtains the earliest time
        """
        time_column = np.array(self.NICER_OBS_LIST['TIME'], dtype=float)
        zero_time = np.min(time_column)
        return zero_time
    
    def NICER_ReadLightCurve(self):
        df = pd.DataFrame()
        zero_time = self.NICER_GetZeroTime()
        lightcurve_path = 'sources/{}/nicer/xti/lightcurve.lc'.format(self.SOURCE_NAME)
        data = fits.open(lightcurve_path)
        
        time = np.array(data[1].data['TIME'], dtype='float')
        time_mjd = aux.s2mjd(time) + zero_time
        
        df['TIME'] = time
        df['TIME_MJD'] = time_mjd
        df['RATE'] = np.array(data[1].data['RATE'], dtype='float')
        df['RATE_ERROR'] = np.array(data[1].data['ERROR'], dtype='float')
        self.LIGHTCURVE_NICER = df
        return df

    def NICER_CleanUpgzFiles(self):
        logging.debug('Cleaning NICER gz files')
        aux.UnzipAllgzFiles('sources/{}/nicer/xti'.format(self.SOURCE_NAME))
        aux.RemoveAllgzFiles('sources/{}/nicer/xti'.format(self.SOURCE_NAME))

    def NICER_PlotLightCurve(self):
        self.NICER_AppendFolderToObsList()
        self.NICER_DownloadEventFiles()
        self.NICER_CleanUpgzFiles()
        aux.CreateListFile('sources/{}/nicer/xti'.format(self.SOURCE_NAME), 'evt')
        self.NICER_xselect()
        lc = self.NICER_ReadLightCurve()
        
        plt.figure(figsize=(15,4))
        plt.errorbar(x=lc['TIME_MJD'], y=lc['RATE'], yerr=lc['RATE_ERROR'],
                     capsize=0.5, marker='None', ls='none', label='NiCER')
        plt.title('NiCER : ' + self.SOURCE_NAME)
        plt.xlabel('Time (MJD)')
        plt.ylabel('RATE')
