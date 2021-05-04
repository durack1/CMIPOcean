#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  4 14:33:10 2021

@author: durack1
"""

#%% Imports
import datetime
import json
import os
import pdb

#%% Build list of models per MIP
# Get time
timeFormatDir = datetime.datetime.now().strftime('%y%m%d')
# List input files
fileList = os.listdir(timeFormatDir)

#%% Build entries keying off source_id
mipEra = {}
mipEra['CMIP6'] = {}

for count, filePath in enumerate(fileList):
    if 'CMIP6' in filePath:
        print('filePath:', filePath)
        fullPath = os.path.join(timeFormatDir, filePath)
        print('fullPath:', fullPath)
        with open(fullPath) as jsonFile:
            a = json.load(jsonFile)
            print('a.keys():', a.keys())
            print('a[''response''].keys():', a['response'].keys())
            pdb.set_trace()
            # Use source_id indexes to build out tree
            for count, tmp in enumerate(a['response']['docs']):
                print('id:', tmp['id'])
                docId = tmp['id'].split('|')
                print('docId:', docId)
                modId = docId[0].split('.')
                mipEra = modId[0]
                actId = modId[1]
                instId = modId[2]
                srcId = modId[3]
                expId = modId[4]
                ripfId = modId[5]
                tabId = modId[6]
                varId = modId[7]
                gridId = modId[8]
                verId = modId[9]
                nodeId = docId[1]
                print('mipEra:', mipEra)
                print('actId:', actId)
                print('instId:', instId)
                print('srcId:', srcId)
                print('expId:', expId)
                print('ripfId:', ripfId)
                print('tabId:', tabId)
                print('varId:', varId)
                print('gridId:', gridId)
                print('verId:', verId)
                print('nodeId:', nodeId)
                pdb.set_trace()
