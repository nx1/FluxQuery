#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 15:13:02 2019

@author: nk7g14
for more info:
    https://heasarc.gsfc.nasa.gov/docs/nustar/analysis/
    https://heasarc.gsfc.nasa.gov/docs/nustar/analysis/nustar_swguide.pdf

The Nustar public data archive may be accessed at:
    http://heasarc.gsfc.nasa.gov/FTP/nustar/data/obs/
"""
import os
from ftplib import FTP
import glob

from tqdm import tqdm

import auxil as aux


class NUSTAR:
    def __init__(self):
        super(NUSTAR, self).__init__()
        self.SOURCE_NAME = 'NGC1313' #TODO remove when done
        self.NUSTAR_OBS_LIST = aux.GetObservationList(self.SOURCE_NAME, 'NUMASTER')
        self.LIGHTCURVE_SWIFT_UVOT = None
        
    def NUSTAR_DownloadObservations(self):
        ftp = FTP('heasarc.gsfc.nasa.gov')
        ftp.login()
        pbar = tqdm(self.NUSTAR_OBS_LIST)
        for row in pbar:

            cycle = '0' + row['CYCLE'].strip()
            obsid = row['OBSID']

            path = 'nustar/data/obs/{}/{}/{}/hk'.format(cycle, obsid[0], obsid)
            files = ftp.nlst(path)
            pbar.set_description('Downloading NuSTAR: %s' % obsid)
            for file in tqdm(files):
                filename = file.split('/')[-1]
                os.makedirs('sources/{}/nustar/{}'.format(self.SOURCE_NAME, obsid), exist_ok=True)
                savedir = './sources/{}/nustar/{}/'.format(self.SOURCE_NAME, obsid) + filename
                with open(savedir, "wb") as fileout:
                    ftp.retrbinary("RETR "+file, fileout.write)
            
        ftp.quit()

    def NUSTAR_CleanUpgzFiles(self):
        obs_folders = glob.glob('sources/{}/nustar/*'.format(self.SOURCE_NAME))
        for folder in tqdm(obs_folders):
            aux.UnzipAllgzFiles(folder)
            aux.RemoveAllgzFiles(folder)
        return

#TODO Figure out how to create only lightcurves from cl evt products.
#Currently I'm able to create all products using 'nuproducts' however this
#is kinda slow and I also don't need spectra and everything else.
#The problem is that you cannot use normal xselect methods to create the lc
#apparently.
        
#Another thing to note is that after creating the lightcurve using nuproducts
#I still had to use 'lcurve' to bin the output data


ngc1313 = NUSTAR()
# ngc1313.NUSTAR_DownloadObservations()
ngc1313.NUSTAR_CleanUpgzFiles()
