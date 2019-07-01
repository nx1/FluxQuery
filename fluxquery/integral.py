#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 12:43:04 2019

@author: nk7g14
"""
from astroquery.heasarc import Heasarc as h
import logging

def GetObservationList(source_name):
    try:
        logging.debug('Querying Heasarc intscwpub catalogue')
        obs_list = h.query_object(source_name, mission='intscwpub', fields='All',
                                  resultmax=2000)
        return obs_list
    except:
        logging.debug('Failed to get integral observation list')
        return None