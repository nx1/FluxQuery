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
from tqdm import tqdm

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
    coords = SkyCoord.from_name(source_name)
    source_ra = coords.ra.deg
    source_dec = coords.dec.deg
    
    cat_files = glob.glob('sources/{}/swift/uvot/cat/*.cat'.format(source_name))
    try:
        logging.debug('Looking for prebuilt swift_uvot flux df')
        df = pd.read_csv('sources/{}/swift/uvot/cat/flux_df.csv'.format(source_name))
        return df
    except FileNotFoundError:
        logging.debug('Could not find prebuilt swift_uvot flux df')
        pass
        
    # source_ra = 49.58333   #NGC1313 HARDCODED
    # source_dec = -66.48639 #NGC1313 HARDCODED
    search_radius = 0.1
    
    catobsID = swift.GetObservationID(source_name)
    observation_list = swift.GetObservationList(source_name)
    start_times = swift.GetStartTimes(observation_list)
    
    rows = []
    logging.debug('Getting all fluxes for Swift UVOT from .cat files')
    for file in tqdm(cat_files):
        obsID = GetObsIDFromCatFile(file)
        flux_df = GetFluxesFromCatFile(file, source_ra, source_dec, search_radius)
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
    df.to_csv('sources/{}/swift/uvot/cat/flux_df.csv'.format(source_name))
    return df
