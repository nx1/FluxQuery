#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 12:14:55 2019

@author: nk7g14
"""

from astroquery.heasarc import Heasarc as h
import logging


def GetObservationList(source_name):
    try:
        logging.debug('Querying Heasarc MAXIMASTER catalogue')
        obs_list = h.query_object(source_name, mission='MAXIMASTER', fields='All')
        return obs_list
    except:
        logging.debug('Failed to get MAXI observation list')
        return None
