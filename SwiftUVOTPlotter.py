#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  7 15:00:41 2019

@author: nk7g14
SwiftUVOTPlotter.py
Plots the long term light curve for a given source from the UVOT telescope.

Does this by obtaining start times from observation IDS by catalogue query
then obtains flux from output of "uvotsource" command for each ID.
"""

from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import os
from astroquery.heasarc import Heasarc
from astropy.time import Time
import glob
import re
import pandas as pd

import swift

h = Heasarc()

source_name = 'NGC1313'
observation_list = swift.GetObservationList(source_name)
catobsID = swift.GetObservationID(source_name)
start = swift.GetStartTimes(observation_list)

cat_files = glob.glob('{}/uvot/cat/*.cat'.format(source_name))

def GetObsIDFromCatFile(file):
    return re.findall(r'\d{11}', file) #Regex pattern to find 11 digits

def GetFluxesFromCatFile(file):
    data = fits.open(file)
    flux = data[1].data['FLUX']
    flux_err = data[1].data['FLUX_ERR']
    flux_df = pd.DataFrame()
    flux_df['FLUX'] = flux
    flux_df['FLUX_ERR'] = flux_err
    return flux_df



for file in cat_files:
    obsID = GetObsIDFromCatFile(file)
    flux_df = GetFluxesFromCatFile(file)
    print(obsID, np.mean(flux_df['FLUX']))
    
#Open cat file.
#Get obsID
#Get flux and error
#Find matching obsID and start time.
#The RA and DEC for each observation varies over the course of the observation
#It may be a good idea to attempt to constrain the fluxes we take to only those
#which are looking a the source :/

plt.scatter(ra,dec)



flux=np.empty(len(cat_files))
fluxErr=np.empty(len(cat_files))
starts=np.empty(len(cat_files))
obsID=[]


for i, j in zip(cat_files, range(len(cat_files))):
    #MAKE SURE YOU DON'T HAVE ANY OTHER FILES IN THE DIR
    print(j, '/', len(cat_files))
    obsID.append(i[2:-5])   #Extract observationID from .cat filename
    print('opening file:', i, 'obsID:', obsID[j])
    data=fits.open('%s/uvot/cat/%s' %(source_name, i))  #Open the cat file
    flux[j] = np.mean(data[1].data['FLUX'])             #Obtain the flux from the fits file
    fluxErr[j] = np.mean(data[1].data['FLUX_ERR'])      #and the flux error
    print('Found Fluxes:', flux[j])                     
    starts[j] = mjd2year(start[np.where(catobsID==obsID[j])])   #find the associated start time for that paticular obsID
    print('Corresponding start time:', starts[j])           
    
    
fig, ax1 = plt.subplots()

ax1.scatter(starts ,flux , marker='x', color='violet')
ax1.set_ylim(0.0,1.1*np.nanmax(flux))
ax1.set_xlabel('Time')
ax1.set_ylabel('Flux x-ray')
plt.title('%s' %source_name)

ax2 = ax1.twinx()
ax2.set_ylabel('Flux uv')
lc=fits.open('%s/xrt/output.lc' %source_name)
ax2.scatter(s2year(lc[1].data['TIME'])+2009.637, lc[1].data['RATE1'], marker='x', color='black')
ax2.set_ylim(0.0,1.1*np.nanmax(lc[1].data['RATE1']))