#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  7 15:00:41 2019

@author: nk7g14
"""

from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import os
from astroquery.heasarc import Heasarc
from astropy.time import Time


mjd2year = lambda times: Time(times, format='mjd').decimalyear
s2year = lambda times: times/60/60/24/365.25

h = Heasarc()

def GetObsIDs(sourceName, mission):
    query = h.query_object(sourceName, mission, fields='OBSID')
    obsIDs = np.array(query['OBSID'], dtype='str')
    query = h.query_object(sourceName, mission, fields='START_TIME')
    startTime = np.array(query['START_TIME'], dtype='float')
    return obsIDs, startTime

sourceName = 'NGC1313'
mission = 'swiftmastr'


catobsID, start = GetObsIDs(sourceName, mission)

listDir = os.listdir('%s/uvot/cat' %(sourceName))

flux=np.empty(len(listDir))
fluxErr=np.empty(len(listDir))
starts=np.empty(len(listDir))
obsID=[]


for i, j in zip(listDir, range(len(listDir))):
    #MAKE SURE YOU DON'T HAVE ANY OTHER FILES IN THE DIR
    print(j, '/', len(listDir))
    obsID.append(i[2:-5])
    print('opening file:', i, 'obsID:', obsID[j])
    data=fits.open('%s/uvot/cat/%s' %(sourceName, i))
    flux[j] = np.mean(data[1].data['FLUX'])
    fluxErr[j] = np.mean(data[1].data['FLUX_ERR'])
    print('Found Fluxes:', flux[j])
    starts[j] = mjd2year(start[np.where(catobsID==obsID[j])])
    print('Corresponding start time:', starts[j])
    
    
fig, ax1 = plt.subplots()

ax1.scatter(starts ,flux , marker='x', color='violet')
ax1.set_ylim(0.0,1.1*np.nanmax(flux))
ax1.set_xlabel('Time')
ax1.set_ylabel('Flux x-ray')
plt.title('%s' %sourceName)

ax2 = ax1.twinx()
ax2.set_ylabel('Flux uv')
lc=fits.open('%s/xrt/output.lc' %sourceName)
ax2.scatter(s2year(lc[1].data['TIME'])+2009.637, lc[1].data['RATE1'], marker='x', color='black')
ax2.set_ylim(0.0,1.1*np.nanmax(lc[1].data['RATE1']))