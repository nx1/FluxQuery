#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 14:51:29 2019

@author: nk7g14
This for some reason runs fine in the linux terminal but doesn't in the ipython one?
https://heasarc.nasa.gov/ftools/caldb/help/uvotsource.html
"""
import logging
import subprocess
import glob
from astropy.io import fits
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import os

import auxil as aux
import swift

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s -- %(message)s')

home_path = os.getcwd()
img_path = 'sources/NGC1313/swift/uvot/img'

def uvotsource(image_file):
    '''
    Performs the 'uvotsource' command on a given .img file
    '''
    output_file = image_file[:-4] + '.fits'
    subprocess.call(['uvotsource image={} srcreg=src.reg bkgreg=bkg.reg sigma=1.0 outfile=uvotsource/{}'.format(image_file, output_file)], shell=True)

def uvotproduct(image_file):
    '''
    #TODO translate the following into python
    my @in = <file>;
    $t = $in3[0];
    $MET = (($t - 53769.415972)*24*3600) + 160653541.0;
    system "uvotproduct timezero=$MET infile=$dir outfile=$outfile plotfile=$outfile2 srcreg=src.reg bkgreg=bkg.reg batpos=NONE xrtpos=NONE uvotpos=NONE groundpos=NONE reportfile=$rep clobber=yes"; 
    '''
    pass

def GetFluxes(fits_file):
    df = pd.DataFrame()
    data = fits.open(fits_file)
    
    df['MET'] = np.array(data[1].data['MET'], dtype=float) 
    df['TSTART'] = np.array(data[1].data['TSTART'], dtype=float)
    df['TSTOP'] = np.array(data[1].data['TSTOP'], dtype=float)
    df['RAW_TOT_CNTS'] = np.array(data[1].data['RAW_TOT_CNTS'], dtype=float)
    df['RAW_TOT_CNTS_ERR'] = np.array(data[1].data['RAW_TOT_CNTS_ERR'], dtype=float)
    df['RAW_TOT_RATE'] = np.array(data[1].data['RAW_TOT_RATE'], dtype=float)
    df['RAW_TOT_RATE_ERR'] = np.array(data[1].data['RAW_TOT_RATE_ERR'], dtype=float)
    df['MAG'] = np.array(data[1].data['MAG'], dtype=float)
    df['MAG_ERR'] = np.array(data[1].data['MAG_ERR'], dtype=float)
    return df


# os.chdir(img_path)
# img_files = glob.glob('*.img')
# for file in img_files:
#     uvotsource(file)
# os.chdir(home_path)

observation_list = swift.GetObservationList('NGC1313')
start_times = swift.GetStartTimes(observation_list)

path = 'sources/NGC1313/swift/uvot/img'
os.chdir(path)
obs_id_regex = re.compile(r'\d{11}')
output_files = glob.glob('uvotsource/*.fits')
df_dict = {}
for file in output_files:
    print(file)
    obsID = obs_id_regex.search(file).group()
    mask = start_times['OBSID'] == obsID
    try:
        start = start_times[mask]['START_TIME'].values[0]
    except:
        start = None
    print('start', start)
    df_dict[obsID] = GetFluxes(file)
    df_dict[obsID]['START_MJD'] = start

df = pd.concat(df_dict)
df = df.sort_values(by=['TSTART'])

# plt.plot(df['TSTART'], df['MAG'])

'''
#NORMALISING TO ONE
df['RAW_TOT_CNTS'] = df['RAW_TOT_CNTS'] / max(df['RAW_TOT_CNTS'])
df['RAW_TOT_RATE'] = df['RAW_TOT_RATE'] / max(df['RAW_TOT_RATE'])
df['MAG'] = df['MAG'] / max(df['MAG'])

df['RAW_TOT_CNTS_ERR'] = df['RAW_TOT_CNTS_ERR'] / max(df['RAW_TOT_CNTS'])
df['RAW_TOT_RATE_ERR'] = df['RAW_TOT_RATE_ERR'] / max(df['RAW_TOT_RATE'])
df['MAG_ERR'] = df['MAG_ERR'] / max(df['MAG'])
'''

#RAW COUNTS LIGHTCURVE FROM UVOTSOURCE 
plt.errorbar(df['START_MJD'], df['RAW_TOT_CNTS'], yerr=df['RAW_TOT_CNTS_ERR'],
              capsize=0.5, marker='None', ls='none', label='RAW_TOT_CNTS|uvotsource', c='green')
plt.legend()
plt.show()
#TOTAL RATE LIGHTCURVE FROM UVOTSOURCE
plt.errorbar(df['START_MJD'], df['RAW_TOT_RATE'], yerr=df['RAW_TOT_RATE_ERR'],
              capsize=0.5, marker='None', ls='none', label='RAW_TOT_RATE|uvotsource', c='cyan')
plt.legend()

#MAG LIGHTCURVE FROM UVOTSOURCE
df = df[df['MAG_ERR'] < 10]
plt.errorbar(df['START_MJD'], df['MAG'], yerr=df['MAG_ERR'],
             capsize=0.5, marker='None', ls='none', label='MAG|uvotsource', c='blue')
plt.legend()