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

    for obsID in observations:
        if xrt==True:
            url_xrt = 'http://www.swift.ac.uk/archive/reproc/{}/xrt/event/sw{}xpcw3po_cl.evt.gz'.format(obsID,obsID)
            savedir_xrt = '{}/sources/{}/swift/xrt/sw{}xpcw3po_cl.evt.gz'.format(cwd,source_name,obsID)
            aux.FetchFile(url_xrt, savedir_xrt)
        if uvot==True:
            url_uvot_cat = 'http://www.swift.ac.uk/archive/reproc/{}/uvot/products/sw{}u.cat.gz'.format(obsID, obsID)
            savedir_uvot_cat = '{}/sources/{}/swift/uvot/cat/sw{}u.cat.gz'.format(cwd, source_name, obsID)
            
            url_uvot_img = 'http://www.swift.ac.uk/archive/reproc/{}/uvot/image/sw{}uuu_sk.img.gz'.format(obsID,obsID)
            savedir_uvot_img = '{}/sources/{}/swift/uvot/img/sw{}uuu_sk.img.gz'.format(cwd, source_name, obsID)
            
            aux.FetchFile(url_uvot_cat, savedir_uvot_cat)
            aux.FetchFile(url_uvot_img, savedir_uvot_img)
       # aux.FetchFile('http://www.swift.ac.uk/archive/reproc/%s/uvot/image/sw%suuu_rw.img.gz' % (obsID,obsID),
       #           '%s/%s/uvot/img/sw%suuu_rw.img.gz' % (cwd, source_name, obsID))

def CreateSaveDirectories():
    os.mkdir('sources')
    os.mkdir('sources/{}'.format(source_name))
    os.mkdir('sources/{}/swift'.format(source_name))
    os.mkdir('sources/{}/swift/xrt'.format(source_name))
    os.mkdir('sources/{}/swift/uvot'.format(source_name))
    os.mkdir('sources/{}/swift/uvot/img'.format(source_name))
    os.mkdir('sources/{}/swift/uvot/cat'.format(source_name))

def CleanUpgzFiles():
    aux.UnzipAndRemoveAllgzFiles('sources/{}/swift/xrt'.format(source_name))
    aux.UnzipAndRemoveAllgzFiles('sources/{}/swift/uvot/img'.format(source_name))
    aux.UnzipAndRemoveAllgzFiles('sources/{}/swift/uvot/cat'.format(source_name))

def Complete():
    observation_IDs = swift.GetObservationID(source_name)
    CreateSaveDirectories()
    DownloadEventFiles(observation_IDs)
    CleanUpgzFiles()
    aux.CreateEventListFile('sources/{}/swift/xrt'.format(source_name))

source_name = 'NGC300'
Complete()