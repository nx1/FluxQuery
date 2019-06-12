#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 12:24:26 2019

@author: nk7g14
This file hold various auxilery functions used in FluxQuery.
"""
import matplotlib.pyplot as plt
import os
import urllib.request
import shutil
import glob
from astropy.time import Time
import gzip
import tarfile
import logging

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s -- %(message)s')

mjd2year = lambda times: Time(times, format='mjd').decimalyear
s2year = lambda times: times/60/60/24/365.25

def PlotStartAndEndTimes(start_end):
    '''
    Plots horizontal lines for the start and end time of a given array.
    start_end: pandas dataframe of two columns with start and end times
    '''
    plt.xlabel('Time (MJD)')
    plt.ylabel('Flux')
    for index, row in start_end.iterrows():
        plt.scatter(row['START_TIME'], 1)
        plt.hlines(1, row['START_TIME'], row['END_TIME'])
             
def FetchFile(url, path):
    '''
    retrieves the file from a given URL
    path: Save Location
    '''
    try:
        urllib.request.urlretrieve(url, path)
    except urllib.error.HTTPError:
        logging.debug('could not find:', url)
        pass
    
def UnzipAllgzFiles(path):
    '''
    Unzips all the gz files in a given path
    '''
    gz_files = glob.glob(path + '/*.gz')
    for file in gz_files:
        with gzip.open(file, 'rb') as f_in:
            with open(file[:-3], 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

def RemoveAllgzFiles(path):
    '''
    Removes all gz files in a given path
    '''
    gz_files = glob.glob(path + '/*.gz')
    for file in gz_files:
        os.remove(file)

def UnzipAndRemoveAllgzFiles(path):
    UnzipAllgzFiles(path)
    RemoveAllgzFiles(path)
    
def UnzipalltarFiles(path):
    cwd = os.getcwd()
    os.chdir(path)
    tar_files = glob.glob('*.tar')
    for file in tar_files:
        logging.debug(file)
        file = tarfile.open(name=file, mode='r')
        file.extractall()
        file.close()
    os.chdir(cwd)

def RemoveAlltarFiles(path):
    '''
    Removes all tar files in a given path
    '''
    cwd = os.getcwd()
    os.chdir(path)
    tar_files = glob.glob('*.tar')
    for file in tar_files:
        os.remove(file)
    os.chdir(cwd)
    
def UnzipAndRemoveAlltarFiles(path):
    UnzipalltarFiles(path)
    RemoveAlltarFiles(path)
    
def CreateEventListFile(path):
    '''
    Creates list file of all event files .evt in directory for use in Xselect
    '''
    evt_files = glob.glob(path + '/*.evt')
    f = open('{}/file.ls'.format(path), 'w+')
    for path in evt_files:
        filename = path.split('/')[-1]
        f.write(filename +'\n')
    f.close()