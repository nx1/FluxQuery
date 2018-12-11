#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 13:56:29 2018

@author: nk7g14
"""
from astroquery.heasarc import Heasarc
import numpy as np
import urllib.request
import os
import gzip
import shutil



h = Heasarc()


sourceName = 'NGC300'
mission = 'swiftmastr'




def GetObsIDs(sourceName, mission):
    '''
    Returns array of observation IDS for a given sourceName and Mission
    Currently only works for missions with column name ['OBSID']
    '''
    query = h.query_object(sourceName, mission, fields='OBSID')
    obsIDs = np.array(query['OBSID'], dtype='str')
    return obsIDs


def DownloadEventFiles(observations):
    '''
    Downloads (level 2) Screened event files for given list of observation IDs
    '''
    cwd = os.getcwd()   #Current Working Directory

    try:
        # Create target Directory
        os.mkdir(sourceName)
        print("Directory " , sourceName ,  " Created ") 
    except FileExistsError:
        print("Directory " , sourceName ,  " already exists")
    
    
    counter = 0
    for i in observations:
        try:
            url = 'http://www.swift.ac.uk/archive/reproc/%s/xrt/event/sw%sxpcw3po_cl.evt.gz' % (i,i)
            urllib.request.urlretrieve(url, '%s/%s/sw%sxpcw3po_cl.evt.gz' % (cwd ,sourceName, i))
        except urllib.error.HTTPError:
            print('could not find:', i)
            counter += 1
            pass
    
    print('Total Downloaded:', len(observations) - counter, '/', len(observations))


def UnzipAndRemove(sourceName):
    '''
    Unzips all gz files in directory if given sourcename and then removes 
    associated .gz files
    '''
    listDir = os.listdir(sourceName)
    for i in listDir:
        with gzip.open('%s/%s' % (sourceName, i), 'rb') as f_in:
            with open('%s/%s' % (sourceName, i[:-3]), 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove('%s/%s' % (sourceName, i))
        
def CreateListFile(sourceName):
    '''
    Creates list file of all event files in directory for use in Xselect
    '''
    listDir = os.listdir(sourceName)
    f = open("%s/file.ls" % sourceName,"w+")
    for i in listDir:
         f.write(i +'\n')
    f.close() 
        
obs=GetObsIDs(sourceName, mission)
DownloadEventFiles(obs)
UnzipAndRemove(sourceName)
CreateListFile(sourceName)
