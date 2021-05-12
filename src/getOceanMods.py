#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  4 14:27:40 2021

PJD  6 May 2021     - Add sort by key
PJD 11 May 2021     - Dealt with new directory info

@author: durack1
"""

import datetime
import json
import os
import shutil
from esgfQueryModels import get_dataset_time_data

# %% Get time
timeNow = datetime.datetime.now()
timeFormat = timeNow.strftime('%Y-%m-%d')
timeFormatDir = timeNow.strftime('%y%m%d')
print('timeFormatDir:', timeFormatDir)
print('os.getcwd():', os.getcwd())
os.chdir('..')
print('os.getcwd():', os.getcwd())

# %% Create/manage output dir
if os.path.exists(timeFormatDir):
    shutil.rmtree(timeFormatDir)
    print('Existing dir', timeFormatDir, 'purged')
os.mkdir(timeFormatDir)
os.chdir(timeFormatDir)
print('os.getcwd():', os.getcwd())

# %% Define MIPs and iterate
mips = {}
mips['CMIP6'] = ['C4MIP', 'CMIP', 'DAMIP', 'FAFMIP', 'HighResMIP', 'OMIP',
                 'PMIP', 'ScenarioMIP']
mips['CMIP5'] = ['CMIP']
mips['CMIP3'] = ['CMIP']

# %% Loop through mipEras and actIds
for mipEra in mips.keys():
    print('mipEra:', mipEra)
    for count, actId in enumerate(mips[mipEra]):
        print('activity_id:', actId)
        # Call function - get json output
        js = get_dataset_time_data(project=mipEra, activity_id=actId,
                                   variable_id='tos')
        # Write output
        outFile = '_'.join([timeFormatDir, mipEra, actId,
                            'ESGF-Datasets.json'])
        print('outFile:', outFile)
        print('JSON response numFound:', js['response']['numFound'])
        with open(outFile, 'w', encoding='utf-8') as f:
            json.dump(js, f, ensure_ascii=False, indent=4, sort_keys=True)
