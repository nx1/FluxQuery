#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 12:24:26 2019

@author: nk7g14
This file hold various auxilery functions used in FluxQuery.
"""

import os
import urllib.request
import shutil
import glob
import sys
import time
from pathlib import Path
import gzip
import tarfile
import logging

from astropy.time import Time
import matplotlib.pyplot as plt


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

def reporthook(count, block_size, total_size):
    '''
    report hook used for urllib progress
    '''
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration))
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" %
                    (percent, progress_size / (1024 * 1024), speed, duration))

def FetchFile(url, path):
    '''
    retrieves the file from a given URL
    path: Save Location
    '''
    path_no_gz = path.replace('.gz', '')
    path_no_tar = path.replace('.tar', '')
    path_no_targz = path.replace('.tar.gz', '')

    path_is_file = Path(path).is_file()
    gz_is_file = Path(path_no_gz).is_file()
    tar_is_file = Path(path_no_tar).is_file()
    targz_is_file = Path(path_no_targz).is_file()

    try:
        if path_is_file or gz_is_file or tar_is_file or targz_is_file:
            logging.debug('%s already exists, not downloading.', path)
        else:
            urllib.request.urlretrieve(url, path, reporthook)
    except urllib.error.HTTPError:
        logging.debug('could not find: %s', url)
        pass

def UnzipAllgzFiles(path):
    '''
    Unzips all the gz files in a given path
    '''
    gz_files = glob.glob(path + '/*.gz')
    for file in gz_files:
        logging.debug('Unzipping %s', file)
        with gzip.open(file, 'rb') as f_in:
            with open(file[:-3], 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

def RemoveAllgzFiles(path):
    '''
    Removes all gz files in a given path
    '''
    gz_files = glob.glob(path + '/*.gz')
    for file in gz_files:
        logging.debug('Removing %s', file)
        os.remove(file)

def UnzipalltarFiles(path):
    '''
    Unzips all tar files in a given path
    '''
    tar_files = glob.glob(path + '/*.tar')
    for file in tar_files:
        logging.debug('Unzipping %s', file)
        file = tarfile.open(name=file, mode='r')
        file.extractall()
        file.close()

def RemoveAlltarFiles(path):
    '''
    Removes all tar files in a given path
    '''
    tar_files = glob.glob(path + '/*.tar')
    for file in tar_files:
        logging.debug('Removing %s', file)
        os.remove(file)

def CreateListFile(path, extension):
    '''
    Creates list file of all event files .evt in directory for use in Xselect
    extension to be specified as 'txt' or 'evt' aka no dots or anything
    '''
    evt_files = glob.glob(path + '/*' + extension)
    f = open('{}/file.ls'.format(path), 'w+')
    for file in evt_files:
        filename = file.split('/')[-1]
        f.write(filename +'\n')
    f.close()
