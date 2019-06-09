#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 14:41:30 2019

@author: nk7g14
"""
import os

import auxil as aux
import requests

def GetObservationListRXTE(object_name):
    try:
        obs_list = h.query_object(object_name, mission='XTEMASTER', fields='All')
        return obs_list
    except:
        print('Failed to get RXTE observation list')

def CreateSaveDirectories():
    aux.CreateDir(source_name)
    aux.CreateDir('{}/rxte'.format(source_name))
    
def DownloadRXTEObservation(obsID, source_name):
    #Attempt 2
    first_bit = obsID.split('-')
    url = 'http://heasarc.gsfc.nasa.gov/cgi-bin/W3Browse/xteTar.pl?obsid={}&prnb={}'.format(obsID, first_bit)
    myfile = requests.get(url, allow_redirects=True)
    cwd = os.getcwd()
    open(cwd + '/{}/rxte/{}.tar'.format(source_name,obsID), 'wb').write(myfile.content)
    

source_name = 'GRS1915+105'

obs_list = GetObservationListRXTE(source_name)
CreateSaveDirectories()

for observation in obs_list:
    DownloadRXTEObservation(observation, source_name)
