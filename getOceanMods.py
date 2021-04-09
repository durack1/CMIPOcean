#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 14:49:10 2021

@author: durack1
"""

import datetime
import pdb
import shlex
import subprocess

#%% Get time
timeNow = datetime.datetime.now()
timeFormat = timeNow.strftime('%Y-%m-%d')
timeFormatDir = timeNow.strftime('%y%m%d')
print(timeFormat)

#%% Define MIPs and iterate
keys = ['C4MIP', 'CMIP', 'DAMIP', 'FAFMIP', 'HighResMIP', 'OMIP', 'PMIP',
        'ScenarioMIP']
for key in keys:
    print(key)
    cmd = ''.join(['python ./esgfQueryModels.py --project=CMIP6'
                   ' --activity_id=', key, ' --variable_id=tos'])
    cmd = shlex.split(cmd)
    print(cmd)
    process = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    stdout,stderr = process.communicate()
    pdb.set_trace()
    stdout,stderr