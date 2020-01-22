#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 14:41:30 2019

@author: nk7g14
"""
import pandas as pd
import auxil as aux
import os
import requests

import logging
import re
from astropy.io import fits
import numpy as np
from pathlib import Path
import glob


logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s -- %(message)s')
class RXTE:
    def __init__(self):
        super(RXTE, self).__init__()
        self.RXTE_OBS_LIST = aux.GetObservationList(self.SOURCE_NAME, 'xtemaster')

    def _RXTE_DownloadObservation(self, obsID):
        print('Downloading RXTE observation:', obsID)
        filepath = '/sources/{}/rxte/{}.tar'.format(self.SOURCE_NAME, obsID)
        #RXTE observation IDS have a structure like XXXXX-XX-XX-XX
        #and are saved in folders on the archive with the first bit XXXXX with
        #a P in front of it.
        first_bit = obsID.split('-')[0]
        filepath_folder = 'P' + first_bit #Extracted OBSid folder
        
        tar_exists = Path(filepath).is_file()
        folder_exists = Path(filepath_folder).is_file()
        
        if tar_exists or folder_exists:
            print('Folder or tar file already exists, not downloading.')
        else:
            url = 'http://heasarc.gsfc.nasa.gov/cgi-bin/W3Browse/xteTar.pl?obsid={}&prnb={}'.format(obsID, first_bit)
            myfile = requests.get(url, allow_redirects=True)
            cwd = os.getcwd()
            open(cwd + filepath, 'wb').write(myfile.content)
    
    def RXTE_DownloadAllObservations(self):
        for obsID in self.RXTE_OBS_LIST['OBSID']:
            self._RXTE_DownloadObservation(obsID)

            
            
    def RXTE_GetCountsVpXPcu(self, xfl_file):
        df = pd.DataFrame()
        time = np.array(xfl_file[1].data['Time'], dtype=float)
        count1 = np.array(xfl_file[1].data['VpX1LCntPcu0'], dtype=float)
        count2 = np.array(xfl_file[1].data['VpX1RCntPcu0'], dtype=float)
        count3 = np.array(xfl_file[1].data['VpX1LCntPcu1'], dtype=float)
        count4 = np.array(xfl_file[1].data['VpX1RCntPcu1'], dtype=float)
        count5 = np.array(xfl_file[1].data['VpX1LCntPcu2'], dtype=float)
        count6 = np.array(xfl_file[1].data['VpX1RCntPcu2'], dtype=float)
        count7 = np.array(xfl_file[1].data['VpX1LCntPcu3'], dtype=float)
        count8 = np.array(xfl_file[1].data['VpX1RCntPcu3'], dtype=float)
        count9 = np.array(xfl_file[1].data['VpX1LCntPcu4'], dtype=float)
        count10 = np.array(xfl_file[1].data['VpX1RCntPcu4'], dtype=float)
    
        df['Time'] = time
        df['VpX1LCntPcu0'] = count1
        df['VpX1RCntPcu0'] = count2
        df['VpX1LCntPcu1'] = count3
        df['VpX1RCntPcu1'] = count4
        df['VpX1LCntPcu2'] = count5
        df['VpX1RCntPcu2'] = count6
        df['VpX1LCntPcu3'] = count7
        df['VpX1RCntPcu3'] = count8
        df['VpX1LCntPcu4'] = count9
        df['VpX1RCntPcu4'] = count10
        return df
    
    def RXTE_GetCountsQ6VPcu(self, xfl_file):
        df = pd.DataFrame()
        time = np.array(xfl_file[1].data['Time'], dtype=float)
        count1 = np.array(xfl_file[1].data['Q6VxVpXeCntPcu0'], dtype=float)
        count2 = np.array(xfl_file[1].data['Q6VxVpXeCntPcu1'], dtype=float)
        count3 = np.array(xfl_file[1].data['Q6VxVpXeCntPcu2'], dtype=float)
        count4 = np.array(xfl_file[1].data['Q6VxVpXeCntPcu3'], dtype=float)
        count5 = np.array(xfl_file[1].data['Q6VxVpXeCntPcu4'], dtype=float)
    
        df['Time'] = time
        df['Q6VxVpXeCntPcu0'] = count1
        df['Q6VxVpXeCntPcu1'] = count2
        df['Q6VxVpXeCntPcu2'] = count3
        df['Q6VxVpXeCntPcu3'] = count4
        df['Q6VxVpXeCntPcu4'] = count5
        return df
    
    def RXTE_GetCountsXPcu(self, xfl_file):
        df = pd.DataFrame()
        time = np.array(xfl_file[1].data['Time'], dtype=float)
        count1 = np.array(xfl_file[1].data['X1LX2LCntPcu0'], dtype=float)
        count2 = np.array(xfl_file[1].data['X1RX2RCntPcu0'], dtype=float)
        count3 = np.array(xfl_file[1].data['X2LX2RCntPcu0'], dtype=float)
        count4 = np.array(xfl_file[1].data['X2LX3LCntPcu0'], dtype=float)
        count5 = np.array(xfl_file[1].data['X2RX3RCntPcu0'], dtype=float)
        count6 = np.array(xfl_file[1].data['X3LX3RCntPcu0'], dtype=float) 
    
        df['Time'] = time
        df['X1LX2LCntPcu0'] = count1
        df['X1RX2RCntPcu0'] = count2
        df['X2LX2RCntPcu0'] = count3
        df['X2LX3LCntPcu0'] = count4
        df['X2RX3RCntPcu0'] = count5
        df['X3LX3RCntPcu0'] = count6
        return df
    
    def RXTE_GetcountsGood(self, xfl_file):
        df = pd.DataFrame()
        time = np.array(xfl_file[1].data['Time'])
        count_good_1 = np.array(xfl_file[1].data['evXEgood_PCU0'], dtype=float)
        count_good_2 = np.array(xfl_file[1].data['evXEgood_PCU1'], dtype=float)
        count_good_3 = np.array(xfl_file[1].data['evXEgood_PCU2'], dtype=float)
        count_good_4 = np.array(xfl_file[1].data['evXEgood_PCU3'], dtype=float)
        count_good_5 = np.array(xfl_file[1].data['evXEgood_PCU4'], dtype=float)
    
        df['Time'] = time
        df['evXEgood_PCU0'] = count_good_1
        df['evXEgood_PCU1'] = count_good_2
        df['evXEgood_PCU2'] = count_good_3
        df['evXEgood_PCU3'] = count_good_4
        df['evXEgood_PCU4'] = count_good_5
        return df
    
    def RXTE_GetCounts(self, xfl_file):
        #Tempoarily removed good counts as for some observations don't have em
        countsVpX = self.RXTE_GetCountsVpXPcu(xfl_file)
        counts6VP = self.RXTE_GetCountsQ6VPcu(xfl_file)
        countsXP = self.RXTE_GetCountsXPcu(xfl_file)
        #counts_good = self.RXTE_GetcountsGood(xfl_file)
    
        #mapping = [countsVpX, counts6VP, countsXP, counts_good]
        mapping = [countsVpX, counts6VP, countsXP]
        df = pd.concat(mapping, axis=1)
        df = df.loc[:, ~df.columns.duplicated()] #Drop duplicate time columns
        return df
    
    def RXTE_GetAllCounts(self):
        '''
        Runs through all stdprod folders and obtains the flux for each obsID
        returns a dictionary containing all the flux dataframes
        '''
        walk = os.walk('sources/{}/rxte'.format(self.SOURCE_NAME))

        obsIDregex = re.compile(r'\d{5}-\d{2}-\d{2}-\d{2}')
        df_dict = {}

        gz_files = glob.glob('sources/{}/rxte/*/*/stdprod/*.xfl.gz'.format(self.SOURCE_NAME))
        xfl_files = glob.glob('sources/{}/rxte/*/*/stdprod/*.xfl'.format(self.SOURCE_NAME))

        len(gz_files)
        len(xfl_files)

        for walk_iter in walk:
            if 'stdprod' in walk_iter[0]:
                result = obsIDregex.search(walk_iter[0])
                obsID = result.group()
                logging.debug('Getting counts rxte %s', obsID)
                aux.UnzipAllgzFiles(walk_iter[0])
                xfl_search = glob.glob(walk_iter[0] + '/*.xfl')[0]
                xfl_file = fits.open(xfl_search)
                count_df = self.RXTE_GetCounts(xfl_file)
                df_dict[obsID] = count_df
        return df_dict

    def RXTE_MergeDataframeDictionary(self, df_dict):
        df = pd.concat(df_dict.values(), ignore_index=True)
        df = df.sort_values(by=['Time'])
        df = df.reset_index(drop=True)
        return df


    def RXTE_GetLightcurve(self):
        df_dict = self.RXTE_GetAllCounts()
        df = self.RXTE_MergeDataframeDictionary(df_dict)
        self.LIGHTCURVE_RXTE = df
        return df


    def RXTE_Complete(self):
        self.RXTE_DownloadAllObservations()
        aux.UnzipalltarFiles('sources/{}/rxte'.format(self.SOURCE_NAME))
        aux.RemoveAlltarFiles('sources/{}/rxte'.format(self.SOURCE_NAME))
        lc = self.RXTE_GetLightcurve()
        lc.plot(x='Time')
        return lc
