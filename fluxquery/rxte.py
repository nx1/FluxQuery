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
from astroquery.heasarc import Heasarc as h
import logging
import re
from astropy.io import fits
import numpy as np
from pathlib import Path
import glob
from datetime import datetime

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s -- %(message)s')

def GetObservationList(source_name):
    try:
        logging.debug('Querying Heasarc XTEMASTER catalogue')
        obs_list = h.query_object(source_name, mission='XTEMASTER', fields='All')
        return obs_list
    except:
        logging.debug('Failed to get RXTE observation list')
        return None

def CreateSaveDirectories():
    os.makedirs('sources', exist_ok=True)
    os.makedirs('sources/{}'.format(source_name), exist_ok=True)
    os.makedirs('sources/{}/rxte'.format(source_name), exist_ok=True)

def DownloadRXTEObservation(obsID, source_name):
    logging.debug('Downloading RXTE observation: %s', obsID)
    filepath = '/sources/{}/rxte/{}.tar'.format(source_name,obsID)
    first_bit = obsID.split('-')[0]
    filepath_folder = 'P' + first_bit #Extracted OBSid folder
    
    tar_exists = Path(filepath).is_file()
    folder_exists = Path(filepath_folder).is_file()
    
    if Path(filepath).is_file() or filepath_folder:
        logging.debug('Folder or tar file already exists, not downloading.')
    else:
        first_bit = obsID.split('-')[0]
        url = 'http://heasarc.gsfc.nasa.gov/cgi-bin/W3Browse/xteTar.pl?obsid={}&prnb={}'.format(obsID, first_bit)
        myfile = requests.get(url, allow_redirects=True)
        cwd = os.getcwd()
        open(cwd + filepath, 'wb').write(myfile.content)

def GetCountsVpXPcu(xfl_file):
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

def GetCountsQ6VPcu(xfl_file):
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

def GetCountsXPcu(xfl_file):
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

def GetcountsGood(xfl_file):
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

def GetCounts(xfl_file):
    #Tempoarily removed good counts as for some observations don't have em
    countsVpX = GetCountsVpXPcu(xfl_file)
    counts6VP = GetCountsQ6VPcu(xfl_file)
    countsXP = GetCountsXPcu(xfl_file)
    #counts_good = GetcountsGood(xfl_file)

    #mapping = [countsVpX, counts6VP, countsXP, counts_good]
    mapping = [countsVpX, counts6VP, countsXP]
    df = pd.concat(mapping, axis=1)
    df = df.loc[:, ~df.columns.duplicated()] #Drop duplicate time columns
    return df

def GetAllCounts():
    '''
    Runs through all stdprod folders and obtains the flux for each obsID
    returns a dictionary containing all the flux dataframes
    '''
    walk = os.walk('sources/{}/rxte'.format(source_name))
    
    obsIDregex = re.compile(r'\d{5}-\d{2}-\d{2}-\d{2}')
    df_dict = {}
    
    gz_files = glob.glob('sources/{}/rxte/*/*/stdprod/*.xfl.gz'.format(source_name))
    xfl_files = glob.glob('sources/{}/rxte/*/*/stdprod/*.xfl'.format(source_name))
    
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
            count_df = GetCounts(xfl_file)
            df_dict[obsID] = count_df
    return df_dict

def MergeDataframeDictionary(df_dict):
    df = pd.concat(df_dict.values(), ignore_index=True)
    df = df.sort_values(by=['Time'])
    df = df.reset_index(drop=True)
    return df

def RXTEComplete():
    obs_list = GetObservationList(source_name)
    CreateSaveDirectories()

    for observation in obs_list['OBSID']:
        DownloadRXTEObservation(observation, source_name)
    aux.UnzipalltarFiles('sources/{}/rxte'.format(source_name))
    aux.RemoveAlltarFiles('sources/{}/rxte'.format(source_name))
    df_dict = GetAllCounts()
    df = MergeDataframeDictionary(df_dict)
    df.plot(x='Time')
    return df

# source_name = 'GRS1915+105'
# df = RXTEComplete()
    