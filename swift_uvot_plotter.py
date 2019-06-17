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
from astroquery.heasarc import Heasarc as h
from astropy.time import Time
import glob
import re
import pandas as pd
import logging
import swift
from astropy.coordinates import SkyCoord

def GetObsIDFromCatFile(file):
    return re.findall(r'\d{11}', file)[0] #Regex pattern to find 11 digits

def GetFluxesFromCatFile(file, source_ra, source_dec, radius):
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

    df = df[df['RA'] > source_ra-radius]
    df = df[df['RA'] < source_ra+radius]

    df = df[df['DEC'] > source_dec-radius]
    df = df[df['DEC'] < source_dec+radius]
    return df

def GetAllFluxes(source_name):
    logging.warn('CURRENTLY USING HARDCODED RA/DEC')
    # coords = SkyCoord.from_name(source_name)
    # source_ra = coords.ra.deg
    # source_dec = coords.dec.deg
    rows = []
    cat_files = glob.glob('sources/{}/swift/uvot/cat/*.cat'.format(source_name))
    source_ra = 49.58333   ##NGC1313 HARDCODED
    source_dec = -66.48639 #NGC1313 HARDCODED
    search_radius = 0.1
    catobsID = swift.GetObservationID(source_name)
    observation_list = swift.GetObservationList(source_name)
    start_times = swift.GetStartTimes(observation_list)
    
    for file in cat_files:
        obsID = GetObsIDFromCatFile(file)
        flux_df = GetFluxesFromCatFile(file, source_ra, source_dec, search_radius)
        mean_flux = np.mean(flux_df['FLUX'])
        mean_flux_err = np.mean(flux_df['FLUX_ERR'])

        mask = start_times['OBSID'] == obsID
        try:
            start = start_times[mask]['START_TIME'].values[0]
        except:
            start = None

        rows.append([obsID, start, mean_flux, mean_flux_err])
        print(obsID, start, mean_flux, mean_flux_err)

    df = pd.DataFrame.from_records(rows)
    df.columns = ['OBSID', 'START_TIME', 'MEAN_FLUX', 'MEAN_FLUX_ERR']
    df = df.sort_values(by=['START_TIME'])
    return df




# flux_df = complete('NGC1313')
# plt.errorbar(flux_df['START_TIME'], flux_df['MEAN_FLUX'],
#              yerr=flux_df['MEAN_FLUX_ERR'], capsize=0.5, marker='None', ls='none')
    

#Open cat file.
#Get obsID
#Get flux and error
#Find matching obsID and start time.
#The RA and DEC for each observation varies over the course of the observation
#It may be a good idea to attempt to constrain the fluxes we take to only those
#which are looking a the source :/


'''
flux=np.empty(len(cat_files))
fluxErr=np.empty(len(cat_files))
starts=np.empty(len(cat_files))
obsID=[]


for i, j in zip(cat_files, range(len(cat_files))):
    #MAKE SURE YOU DON'T HAVE ANY OTHER FILES IN THE DIR
    logging.debug(j, '/', len(cat_files))
    obsID.append(i[2:-5])   #Extract observationID from .cat filename
    logging.debug('opening file:', i, 'obsID:', obsID[j])
    data=fits.open('sources/%s/uvot/cat/%s' %(source_name, i))  #Open the cat file
    flux[j] = np.mean(np.array(data[1].data['FLUX'])             #Obtain the flux from the fits file
    fluxErr[j] = np.mean(np.array(data[1].data['FLUX_ERR'])      #and the flux error
    logging.debug('Found Fluxes:', flux[j])                     
    starts[j] = mjd2year(start[np.where(catobsID==obsID[j])])   #find the associated start time for that paticular obsID
    logging.debug('Corresponding start time:', starts[j])           
    
    
fig, ax1 = plt.subplots()

ax1.scatter(starts ,flux , marker='x', color='violet')
ax1.set_ylim(0.0,1.1*np.nanmax(flux))
ax1.set_xlabel('Time')
ax1.set_ylabel('Flux x-ray')
plt.title('%s' %source_name)

ax2 = ax1.twinx()
ax2.set_ylabel('Flux uv')
lc=fits.open('sources/%s/xrt/output.lc' %source_name)
ax2.scatter(s2year(lc[1].data['TIME'])+2009.637, lc[1].data['RATE1'], marker='x', color='black')
ax2.set_ylim(0.0,1.1*np.nanmax(lc[1].data['RATE1']))
'''