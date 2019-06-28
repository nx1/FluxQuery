#!/usr/bin/env python3
#!/bin/bash
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 14:57:42 2019

@author: nk7g14
Although there have been a number of changes to support Python package
installation in CIAO 4.11, not all use cases are supported. For example,
the Conda and Anaconda package managers are not supported in CIAO 4.11.
http://cxc.harvard.edu/ciao/scripting/
http://cxc.harvard.edu/ciao/scripting/runtool.html
"""

# import subprocess
# subprocess.call(['. /home/nk7g14/ciao-4.11/bin/ciao.bash'], shell=True)
# subprocess.run(['cat /home/nk7g14/ciao-4.11/bin/contrib/VERSION.CIAO_scripts'], shell=True)


# from ciao_contrib.runtool import *

from astroquery.heasarc import Heasarc as h
import logging


def GetObservationList(source_name):
    try:
        logging.debug('Querying Heasarc CHANMASTER catalogue')
        obs_list = h.query_object(source_name, mission='CHANMASTER', fields='All')
        return obs_list
    except:
        logging.debug('Failed to get Chandra observation list')
        return None