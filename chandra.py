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

import subprocess
subprocess.call(['. /home/nk7g14/ciao-4.11/bin/ciao.bash'], shell=True)
subprocess.run(['cat /home/nk7g14/ciao-4.11/bin/contrib/VERSION.CIAO_scripts'], shell=True)


# from ciao_contrib.runtool import *
