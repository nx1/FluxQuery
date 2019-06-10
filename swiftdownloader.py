#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 13:56:29 2018

@author: nk7g14
Downloads, unzips and then creates a list file for use in Xspec for a given
source name and mission.

The event cleaned event files are downloaded from: 
    http://www.swift.ac.uk/archive/
    eg: http://www.swift.ac.uk/archive/reproc/00031442166/
"""
from astroquery.heasarc import Heasarc
import os
import logging
import swift
import auxil as aux

h = Heasarc()

def DownloadEventFiles(observations, xrt=True, uvot=True):
    '''
    Downloads (level 2) Screened event files for given list of observation IDs
    '''
    cwd = os.getcwd()   #Current Working Directory

    for i in observations:
        if xrt==True:
            aux.FetchFile('http://www.swift.ac.uk/archive/reproc/%s/xrt/event/sw%sxpcw3po_cl.evt.gz' % (i,i),
                      '%s/sources/%s/xrt/sw%sxpcw3po_cl.evt.gz' % (cwd, source_name, i))
        if uvot==True:
            aux.FetchFile('http://www.swift.ac.uk/archive/reproc/%s/uvot/products/sw%su.cat.gz' % (i,i),
                      '%s/sources/%s/uvot/cat/sw%su.cat.gz' % (cwd, source_name, i))
            aux.FetchFile('http://www.swift.ac.uk/archive/reproc/%s/uvot/image/sw%suuu_sk.img.gz' % (i,i),
                      '%s/sources/%s/uvot/img/sw%suuu_sk.img.gz' % (cwd, source_name, i))
       # aux.FetchFile('http://www.swift.ac.uk/archive/reproc/%s/uvot/image/sw%suuu_rw.img.gz' % (i,i),
       #           '%s/%s/uvot/img/sw%suuu_rw.img.gz' % (cwd, source_name, i))

def CreateSaveDirectories():
    aux.CreateDir(sources)
    aux.CreateDir('sources/{}'.format(source_name))
    aux.CreateDir('sources/{}/xrt'.format(source_name))
    aux.CreateDir('sources/{}/uvot'.format(source_name))
    aux.CreateDir('sources/{}/uvot/img'.format(source_name))
    aux.CreateDir('sources/{}/uvot/cat'.format(source_name))

def CleanUpgzFiles():
    aux.UnzipAndRemoveAllgzFiles('sources/{}/xrt'.format(source_name))
    aux.UnzipAndRemoveAllgzFiles('sources/{}/uvot/img'.format(source_name))
    aux.UnzipAndRemoveAllgzFiles('sources/{}/uvot/cat'.format(source_name))

def Complete():
    observation_IDs = swift.GetObservationIDSWIFT(source_name)
    CreateSaveDirectories()
    DownloadEventFiles(observation_IDs)
    CleanUpgzFiles()
    aux.CreateEventListFile('sources/{}/xrt'.format(source_name))

source_name = 'NGC300'
Complete()