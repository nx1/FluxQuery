#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 16:47:36 2018

@author: nk7g14
"""

from astropy.io import fits
import matplotlib.pyplot as plt


lc=fits.open('NGC300/output.lc')
plt.scatter(lc[1].data['TIME'], lc[1].data['RATE1'], marker='x')
plt.xlabel('TIME')
plt.ylabel('RATE')