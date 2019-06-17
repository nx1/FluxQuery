#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 13:13:53 2019

@author: nk7g14
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob

import swift
import swift_uvot_plotter
import auxil as aux

source_name = 'NGC1313'
flux_df = swift_uvot_plotter.GetAllFluxes(source_name)

path = '/home/nk7g14/Desktop/gitbox/FluxQuery/sources/NGC1313/swiftxrt_from_UKSSDC/lcfiles_NGC1313/USERPROD_152.78.1.75_1560181266852/lc'
os.listdir(path)
df = pd.read_csv(path + '/lc.qdp', sep='\t')
df.columns = ['MJD', 't_err1', 't_err2', 'Rate', 'Ratepos', 'Rateneg', 'OBSID']
lc_uv = pd.DataFrame()
lc_xrt = pd.DataFrame()


lc_xrt['TIME'] = df['MJD']
lc_xrt['FLUX'] = df['Rate']
lc_xrt['FLUX_ERR'] = df['Ratepos']

max_xrt = max(lc_xrt['FLUX'])

lc_uv['TIME'] = flux_df['START_TIME']
lc_uv['FLUX'] = max_xrt*flux_df['MEAN_FLUX']/max(flux_df['MEAN_FLUX'])
lc_uv['FLUX_ERR'] = max_xrt*flux_df['MEAN_FLUX_ERR']/max(flux_df['MEAN_FLUX'])



#GETTING RID OF EARLY PARTS
lc_uv = lc_uv[lc_uv['TIME'] > 56000]
lc_xrt = lc_xrt[lc_xrt['TIME'] > 56000]



'''
#NORMALISING TO ONE
lc_xrt['FLUX'] = lc_xrt['FLUX'] / max(lc_xrt['FLUX'])
lc_uv['FLUX'] = lc_uv['FLUX'] / max(lc_uv['FLUX'])

lc_xrt['FLUX_ERR'] = lc_xrt['FLUX_ERR'] / max(lc_xrt['FLUX'])
lc_uv['FLUX_ERR'] = lc_uv['FLUX_ERR'] / max(lc_uv['FLUX'])
'''

#XRT LIGHTCURVE FROM SSDC
plt.errorbar(lc_xrt['TIME'], lc_xrt['FLUX'], yerr=lc_xrt['FLUX_ERR'],
             capsize=0.5, marker='None', ls='none', label='xrt')
plt.legend()

#UVOT LIGHTCURVE FROM MY METHOD
plt.errorbar(lc_uv['TIME'], lc_uv['FLUX'], yerr=lc_uv['FLUX_ERR'],
             capsize=0.5, marker='None', ls='none', label='uv')
plt.legend()







'''
bin_size = 100

uv_time_min = min(lc_uv['TIME'])
uv_time_max = max(lc_uv['TIME'])

xrt_time_min = min(lc_uv['TIME'])
xrt_time_max = max(lc_uv['TIME'])


low = uv_time_min


#Create UV/XRAY flux correlation
bin_size = 50
for i in np.arange(uv_time_min, uv_time_max, bin_size):
    df_cut_uv = lc_uv
    df_cut_xrt = lc_xrt

    high = i
    print('low', 'high', 'i')
    print(low, high, i)


    df_cut_uv = df_cut_uv[df_cut_uv['TIME'] > low]
    df_cut_uv = df_cut_uv[df_cut_uv['TIME'] < high]
    df_cut_uv_flux = np.mean(df_cut_uv['FLUX'])

    df_cut_xrt = df_cut_xrt[df_cut_xrt['TIME'] > low]
    df_cut_xrt = df_cut_xrt[df_cut_xrt['TIME'] < high]
    df_cut_xrt_flux = np.mean(df_cut_xrt['FLUX'])

    print(df_cut_uv_flux)
    low = i
    plt.xlabel('xrt_flux')
    plt.ylabel('uv_flux')

    plt.scatter(df_cut_xrt_flux, df_cut_uv_flux, c='red', s=2.0)
'''
