#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 12:22:30 2019

@author: nk7g14
This file contains scripts for 'FluxQuery' for the swift telescope.
"""
import re
import os
import logging
import glob
import pandas as pd
import numpy as np

from tqdm import tqdm
from astropy.io import fits

import auxil as aux

class SWIFT:
    def __init__(self):
        super(SWIFT, self).__init__()
        self.swift_obs_list = aux.GetObservationList(self.source_name, 'swiftmastr')


    def SWIFT_CreateSaveDirectories(source_name):
        os.makedirs('sources', exist_ok=True)
        os.makedirs('sources/{}'.format(source_name), exist_ok=True)
        os.makedirs('sources/{}/swift'.format(source_name), exist_ok=True)
        os.makedirs('sources/{}/swift/xrt'.format(source_name), exist_ok=True)
        os.makedirs('sources/{}/swift/uvot'.format(source_name), exist_ok=True)
        os.makedirs('sources/{}/swift/uvot/img'.format(source_name), exist_ok=True)
        os.makedirs('sources/{}/swift/uvot/cat'.format(source_name), exist_ok=True)
    
    
    def SWIFT_DownloadEventFiles(source_name, observation_ids):
        '''
        Downloads (level 2) Screened event files for given list of observation IDs
        '''
        cwd = os.getcwd()   #Current Working Directory
    
        for obsID in observation_ids:
            url_xrt = 'http://www.swift.ac.uk/archive/reproc/{}/xrt/event/sw{}xpcw3po_cl.evt.gz'.format(obsID, obsID)
            savedir_xrt = '{}/sources/{}/swift/xrt/sw{}xpcw3po_cl.evt.gz'.format(cwd, source_name, obsID)
    
            url_uvot_cat = 'http://www.swift.ac.uk/archive/reproc/{}/uvot/products/sw{}u.cat.gz'.format(obsID, obsID)
            savedir_uvot_cat = '{}/sources/{}/swift/uvot/cat/sw{}u.cat.gz'.format(cwd, source_name, obsID)
    
            url_uvot_img = 'http://www.swift.ac.uk/archive/reproc/{}/uvot/image/sw{}uuu_sk.img.gz'.format(obsID, obsID)
            savedir_uvot_img = '{}/sources/{}/swift/uvot/img/sw{}uuu_sk.img.gz'.format(cwd, source_name, obsID)
    
            aux.FetchFile(url_xrt, savedir_xrt)
            aux.FetchFile(url_uvot_cat, savedir_uvot_cat)
            aux.FetchFile(url_uvot_img, savedir_uvot_img)
           # aux.FetchFile('http://www.swift.ac.uk/archive/reproc/%s/uvot/image/sw%suuu_rw.img.gz' % (obsID,obsID),
           #           '%s/%s/uvot/img/sw%suuu_rw.img.gz' % (cwd, source_name, obsID))
    
    
    def SWIFT_CleanUpgzFiles(source_name):
        aux.UnzipAllgzFiles('sources/{}/swift/xrt'.format(source_name))
        aux.RemoveAllgzFiles('sources/{}/swift/xrt'.format(source_name))
    
        aux.UnzipAllgzFiles('sources/{}/swift/uvot/img'.format(source_name))
        aux.RemoveAllgzFiles('sources/{}/swift/uvot/img'.format(source_name))
    
        aux.UnzipAllgzFiles('sources/{}/swift/uvot/cat'.format(source_name))
        aux.RemoveAllgzFiles('sources/{}/swift/uvot/cat'.format(source_name))
    
    
    def SWIFT_GetStartTimes(self):
        obsID = np.array(self.swift_obs_list['OBSID'], dtype='str')
        start_time = np.array(self.swift_obs_list['START_TIME'])
        df_starts = pd.DataFrame()
        df_starts['OBSID'] = obsID
        df_starts['START_TIME'] = start_time
        return df_starts


    def SWIFT_UVOT_GetObsIDFromCatFile(self, file):
        return re.findall(r'\d{11}', file)[0] #Regex pattern to find 11 digits


    def SWIFT_UVOT_GetFluxesFromCatFile(self, file, radius):
        df = pd.DataFrame()
        data = fits.open(file)

        df['FLUX'] = np.array(data[1].data['FLUX'], dtype=float)
        df['FLUX_ERR'] = np.array(data[1].data['FLUX_ERR'], dtype=float)
        df['REFID'] = np.array(data[1].data['REFID'], dtype=float)
        df['RA'] = np.array(data[1].data['RA'], dtype=float)
        df['DEC'] = np.array(data[1].data['DEC'], dtype=float)
        df['RA_ERR'] = np.array(data[1].data['RA_ERR'], dtype=float)
        df['DEC_ERR'] = np.array(data[1].data['DEC_ERR'], dtype=float)

        #Filtering to only include source
        df = df[df['RA_ERR'] < 1]   #Remove large errors
        df = df[df['DEC_ERR'] < 1]  #Remove large errors

        df = df[df['RA'] > self.source_ra-radius]
        df = df[df['RA'] < self.source_ra+radius]

        df = df[df['DEC'] > self.source_dec-radius]
        df = df[df['DEC'] < self.source_dec+radius]
        return df

    def SWIFT_UVOT_GetAllFluxes(self):
        cat_file_path = 'sources/{}/swift/uvot/cat/*.cat'.format(self.source_name)
        cat_files = glob.glob(cat_file_path)
        logging.debug('Looking for prebuilt swift_uvot flux df')
        try:
            df = pd.read_csv('sources/{}/swift/uvot/cat/flux_df.csv'.format(self.source_name))
            logging.debug('Found: %s' % cat_file_path)
            return df
        except FileNotFoundError:
            logging.debug('Could not find prebuilt swift_uvot flux df')

        search_radius = 0.1

        start_times = self.SWIFT_GetStartTimes()

        rows = []
        logging.debug('Getting all fluxes for Swift UVOT from .cat files')
        for file in tqdm(cat_files):
            obsID = self.SWIFT_UVOT_GetObsIDFromCatFile(file)
            flux_df = self.SWIFT_UVOT_GetFluxesFromCatFile(file, search_radius)
            mean_flux = np.mean(flux_df['FLUX'])
            mean_flux_err = np.mean(flux_df['FLUX_ERR'])    #TODO Check this

            mask = start_times['OBSID'] == obsID
            try:
                start = start_times[mask]['START_TIME'].values[0]
            except:
                start = None

            rows.append([obsID, start, mean_flux, mean_flux_err])
            # print(obsID, start, mean_flux, mean_flux_err)

        df = pd.DataFrame.from_records(rows)
        df.columns = ['OBSID', 'START_TIME', 'MEAN_FLUX', 'MEAN_FLUX_ERR']
        df = df.sort_values(by=['START_TIME'])
        df.to_csv('sources/{}/swift/uvot/cat/flux_df.csv'.format(self.source_name))
        return df
