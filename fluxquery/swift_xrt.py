#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 10:14:40 2019

@author: nk7g14
"""

import os
import subprocess
import logging
from pathlib import Path

import auxil as aux

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s -- %(message)s')

def CreateRegionFile(ra, dec):
    #TODO https://astropy-regions.readthedocs.io/en/latest/ds9.html
    pass

def CreateLightCurve(source_name, region_file, output_file):
    """
    Calls xselect to create a lightcurve. The full method involves creating
    two lightcurves for the source and background regions then using lcmath
    to subtract one from the other.

    Parameters
    ----------
    source_name : str
        Name of source, used to point to correct folder
    region_file : str
        name of region file including extension

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    lc_path = 'sources/{}/swift/xrt/{}'.format(source_name, output_file)
    region_file = 'sources/{}/swift/xrt/{}'.format(source_name, region_file)
    
    if Path(lc_path).is_file():
        logging.debug('Swift-xrt lightcurve file already exists: %s', lc_path)
        return logging.debug('Failed to build swift-xrt Lightcurve')
    elif not Path(region_file).is_file():
        logging.debug('Region file not found: %s', region_file)
        return logging.debug('Failed to build swift-xrt Lightcurve')
    else:
        pass

    home_dir = os.getcwd()
    os.chdir('sources/{}/swift/xrt'.format(source_name))

    binsize = 100   #Binsize in seconds
    low_cutoff = 200 #Low end cutoff frequency in eV
    high_cutoff = 1000 #High end cutoff frequency in eV

    script_file = open('script.xcm', 'w')

    script_text = '''SWIFT
read event "@file.ls"
./
yes
filter region src.reg
set binsize {}
filter pha_cutoff {} {}
extract curve
save curve {}
exit
n
'''.format(binsize, low_cutoff, high_cutoff, output_file)
    script_file.write(script_text)
    script_file.close()
    subprocess.call(['xselect < script.xcm'], shell=True)
    os.chdir(home_dir)

def lcmath(source_name, src_lc, bkg_lc, output_lc):
    home_dir = os.getcwd()
    os.chdir('sources/{}/swift/xrt'.format(source_name))
    
    script_file = open('lcmath.xcm', 'w')
    script_text = '''{}
    {}
    {}
    1
    1
    no
    '''.format(src_lc, bkg_lc, output_lc)
    script_file.write(script_text)
    script_file.close()
    subprocess.call(['lcmath < lcmath.xcm'], shell=True)
    os.chdir(home_dir)
    
    
source_name = 'NGC1313'
path = 'sources/{}/swift/xrt/'.format(source_name)

aux.CreateListFile(path, 'evt')

# CreateLightCurve('NGC1313', 'src_x1.reg', 'src_x1.lc')
# CreateLightCurve('NGC1313', 'bkg_x1.reg', 'bkg_x1.lc')
# lcmath(source_name, 'src_x1.lc', 'bkg_x1.lc', 'lc_x1.lc')

CreateLightCurve('NGC1313', 'src_x2.reg', 'src_x2.lc')
CreateLightCurve('NGC1313', 'bkg_x2.reg', 'bkg_x2.lc')
lcmath(source_name, 'src_x2.lc', 'bkg_x2.lc', 'lc_x2.lc')

folder = '/home/nk7g14/Desktop/gitbox/FluxQuery/sources/NGC1313/swift/xrt'

x1 = fits.open(folder + '/src_x1.lc')
x2 = fits.open(folder + '/src_x2.lc')

time_x1 = x1[1].data['TIME']
time_x2 = x2[1].data['TIME']

rate_x1 = x1[1].data['RATE']
rate_x2 = x2[1].data['RATE']


rate_err_x1 = x1[1].data['ERROR']
rate_err_x2 = x2[1].data['ERROR']


plt.errorbar(time_x1, rate_x1, yerr=rate_err_x1,
capsize=0.5, marker='None', ls='none', label='x1')


plt.errorbar(time_x2, rate_x2, yerr=rate_err_x2,
capsize=0.5, marker='None', ls='none', label='x2')

plt.legend()

