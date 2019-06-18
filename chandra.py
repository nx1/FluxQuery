#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 14:57:42 2019

@author: nk7g14
"""
from ciao_contrib.runtool import *

import subprocess

def LaunchCIAO():
    subprocess.call(['source /home/nk7g14/ciao-4.10/bin/ciao.bash'], shell=True)
LaunchCIAO()