#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 12:15:37 2019

@author: nk7g14
"""
from astroquery.heasarc import Heasarc as h
import logging


def GetObservationList(source_name):
    try:
        logging.debug('Querying Heasarc SUZAMASTER catalogue')
        obs_list = h.query_object(source_name, mission='SUZAMASTER', fields='All')
        return obs_list
    except:
        logging.debug('Failed to get SUZAKU observation list')
        return None