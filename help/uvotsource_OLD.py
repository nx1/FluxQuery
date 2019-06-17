#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 11:10:24 2019

@author: nk7g14
"""

import subprocess
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np


s2year = lambda times: times/60/60/24/365.25

def uvotsource():
    lines = tuple(open("file.ls", 'r'))
    
    for i in lines:
            print(i)
            
            subprocess.call(['uvotsource',
                            'image='+i,
                            'srcreg=src.reg',
                            'bkgreg=bkg.reg',
                            'sigma=3.0',
                            'outfile=image.fits'])

fig, ax1 = plt.subplots()
    
data = fits.open('image.fits')
#remove big boys
mask=data[1].data['MAG']!=99
data[1].data=data[1].data[mask]


zerotime = s2year(160653541)
sort=np.argsort(data[1].data['TSTART'])
ax1.set_ylim(0.99*min(data[1].data['MAG']), 1.05*max(data[1].data['MAG']))
ax1.plot(s2year(data[1].data['TSTART'][sort])-zerotime + 2006 ,data[1].data['MAG'][sort])

'''
ax2 = ax1.twinx()
lc = fits.open('/home/nk7g14/Desktop/gitbox/FluxQuery/NGC1313/xrt/output.lc')
ax2.plot(s2year(lc[1].data['TIME'])+2009.637, np.log(lc[1].data['RATE1']), color='red')
#ax2.set_ylim(0.0,1.1*np.nanmax(lc[1].data['RATE1']))
ax2.set_navigate(False)
'''
uvotsource image=sw00036555112uuu_sk.img srcreg=src.reg bkgreg=bkg.reg sigma=3.0 outfile=image.fits