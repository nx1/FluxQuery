#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 13:56:29 2018

@author: nk7g14
Downloads, unzips and then creates a list file for use in Xspec for a given
source name and mission.

The event cleaned event files are downloaded from: 
    http://www.swift.ac.uk/archive/
"""
from astroquery.heasarc import Heasarc
import numpy as np
import urllib.request
import os
import gzip
import shutil

h = Heasarc()

sourceName = 'NGC1313'
mission = 'swiftmastr'


def GetObsIDs(sourceName, mission):
    '''
    Returns array of observation IDS for a given sourceName and Mission
    Currently only works for missions with column name ['OBSID']
    '''
    query = h.query_object(sourceName, mission, fields='OBSID')
    obsIDs = np.array(query['OBSID'], dtype='str')
    return obsIDs


def CreateDir(Target):
    try:
        os.mkdir(Target)
        print("Directory", Target, " Created")
    except FileExistsError:
        print("Directory", Target, " already exists")
        
def FetchFile(url, saveLoc):
    try:
        urllib.request.urlretrieve(url, saveLoc)
    except urllib.error.HTTPError:
        print('could not find:', url)
        pass
        
    
def DownloadEventFiles(observations, xrt=True, uvot=True):
    '''
    Downloads (level 2) Screened event files for given list of observation IDs
    '''
    cwd = os.getcwd()   #Current Working Directory

    for i in observations:
        FetchFile('http://www.swift.ac.uk/archive/reproc/%s/xrt/event/sw%sxpcw3po_cl.evt.gz' % (i,i),
                  '%s/%s/xrt/sw%sxpcw3po_cl.evt.gz' % (cwd, sourceName, i))
        
        FetchFile('http://www.swift.ac.uk/archive/reproc/%s/uvot/products/sw%su.cat.gz' % (i,i),
                  '%s/%s/uvot/cat/sw%su.cat.gz' % (cwd, sourceName, i))

        FetchFile('http://www.swift.ac.uk/archive/reproc/%s/uvot/image/sw%suuu_rw.img.gz' % (i,i),
                  '%s/%s/uvot/img/sw%suuu_rw.img.gz' % (cwd, sourceName, i))
        
        FetchFile('http://www.swift.ac.uk/archive/reproc/%s/uvot/image/sw%suuu_sk.img.gz' % (i,i),
                  '%s/%s/uvot/img/sw%suuu_sk.img.gz' % (cwd, sourceName, i))
        
def UnzipAndRemove(path):
    '''
    Unzips all gz files in directory if given path and then removes 
    associated .gz files
    '''
    listDir = os.listdir(path)
    for i in listDir:
        with gzip.open('%s/%s' % (path, i), 'rb') as f_in:
            with open('%s/%s' % (path, i[:-3]), 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove('%s/%s' % (path, i))
    
        
def CreateListFile(path):
    '''
    Creates list file of all event files in directory for use in Xselect
    '''
    listDir = os.listdir(path)
    f = open("%s/file.ls" % path,"w+")
    for i in listDir:
         f.write(i +'\n')
    f.close()
      
    
    
obs=GetObsIDs(sourceName, mission)

CreateDir(sourceName)
CreateDir('%s/xrt' %(sourceName))
CreateDir('%s/uvot' %(sourceName))
CreateDir('%s/uvot/img' %(sourceName))
CreateDir('%s/uvot/cat' %(sourceName))
    
DownloadEventFiles(obs)

UnzipAndRemove('%s/xrt' %sourceName)
UnzipAndRemove('%s/uvot/img' %sourceName)
UnzipAndRemove('%s/uvot/cat' %sourceName)

CreateListFile('%s/xrt' %(sourceName))
CreateListFile('%s/uvot/img' %sourceName)
CreateListFile('%s/uvot/cat' %sourceName)
