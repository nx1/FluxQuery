#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 15:13:02 2019

@author: nk7g14
for more info:
    https://heasarc.gsfc.nasa.gov/docs/nustar/analysis/
    https://heasarc.gsfc.nasa.gov/docs/nustar/analysis/nustar_swguide.pdf
"""
from astroquery.heasarc import Heasarc as h
import logging


def GetObservationList(source_name):
    try:
        logging.debug('Querying Heasarc XTEMASTER catalogue')
        obs_list = h.query_object(source_name, mission='NUMASTER', fields='All')
        return obs_list
    except:
        logging.debug('Failed to get NuSTAR observation list')
        return None