#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 10:41:07 2019

@author: nk7g14
"""
from astroquery.heasarc import Heasarc as h
import logging


def GetObservationList(source_name):
    try:
        logging.debug('Querying Heasarc RASS2RXS catalogue')
        obs_list = h.query_object(source_name, mission='RASS2RXS', fields='All')
        return obs_list
    except:
        logging.debug('Failed to get ROSAT observation list')
        return None