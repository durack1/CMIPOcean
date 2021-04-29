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


#%%

3982
https://esgf-node.llnl.gov/solr/datasets/select?q=*:*&wt=json&facet=true&rows=4000&fq=type:Dataset&fq=mip_era:CMIP6&fq=activity_id:CMIP&fq=experiment_id:historical&fq=variable_id:tos&shards=localhost:8983/solr/datasets,localhost:8985/solr/datasets,localhost:8987/solr/datasets,localhost:8988/solr/datasets,localhost:8990/solr/datasets,localhost:8993/solr/datasets,localhost:8994/solr/datasets,localhost:8995/solr/datasets,localhost:8996/solr/datasets,localhost:8997/solr/datasets
2204
https://esgf-node.llnl.gov/solr/datasets/select?q=*:*&wt=json&facet=true&rows=2161&fq=type:Dataset&fq=mip_era:CMIP6&fq=activity_id:CMIP&fq=experiment_id:historical&fq=variable_id:tos
Shards
https://esgf-node.llnl.gov/esg-search/search/?limit=0&format=application%2Fsolr%2Bjson