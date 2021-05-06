#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  4 14:33:10 2021

PJD 6 May 2021 - Regex testing https://regex101.com/

@author: durack1
"""

# %% Imports
import datetime
import json
import os
#import pdb
import re
import sys
import time

# %% functions


def siftBits(tmpId):
    """

    Parameters
    ----------
    tmpId : TYPE
        DESCRIPTION.

    Returns
    -------
    mipEra : TYPE
        DESCRIPTION.
    actId : TYPE
        DESCRIPTION.
    instId : TYPE
        DESCRIPTION.
    srcId : TYPE
        DESCRIPTION.
    expId : TYPE
        DESCRIPTION.
    ripfId : TYPE
        DESCRIPTION.
    tabId : TYPE
        DESCRIPTION.
    varId : TYPE
        DESCRIPTION.
    gridId : TYPE
        DESCRIPTION.
    verId : TYPE
        DESCRIPTION.
    nodeId : TYPE
        DESCRIPTION.

    """
    # CMIP6.ScenarioMIP.NCAR.CESM2-WACCM.ssp126.r1i1p1f1.Oday.tos.gn.v20190815|esgf-data3.ceda.ac.uk
    # cmip5.output1.NOAA-GFDL.GFDL-ESM2M.historicalMisc.day.ocean.day.r1i1p3.v20110601|aims3.llnl.gov
    # cmip3.GFDL.gfdl_cm2_0.historical.mon.ocean.run3.tos.v1|aims3.llnl.gov
    docId = tmpId.split('|')
    modId = docId[0].split('.')
    mipEra = modId[0].upper()
    # validate mipEra
    mipTest = re.compile('^CMIP\d{1}')
    if not mipTest.match(mipEra):
        print('** mipEra format invalid - mipTest: ', mipEra,
              ', exiting.. **')
        sys.exit()
    # Parse dependent on mipEra indexes
    if 'CMIP6' in mipEra:
        actId = modId[1]
        instId = modId[2]
        srcId = modId[3]
        # validate srcId
        expId = modId[4]
        ripfId = modId[5]
        ripfTest = re.compile('^r\d{1,4}i\d{1,4}p\d{1,3}f\d{1,3}')
        tabId = modId[6]
        varId = modId[7]
        gridId = modId[8]
        verTest = re.compile('^v\d{8}')
    elif 'CMIP5' in mipEra:
        actId = 'CMIP'
        instId = modId[2]
        srcId = modId[3]
        # validate srcId
        expId = modId[4]
        # Kludge actId from expId
        expTest = re.compile('^rcp\d{1,2}')
        if expTest.match(expId):
            actId = 'ScenarioMIP'
        # Kludge - poor indexes, missing tableId
        if ('CCCma' in instId and 'CanCM4' in srcId and
            'v20130331' in modId[-1]
            and expId in ['decadal1960', 'decadal1961', 'decadal1962',
                          'decadal1963', 'decadal1964', 'decadal1965',
                          'decadal1966', 'decadal1967', 'decadal1968',
                          'decadal1969', 'decadal1970', 'decadal1971',
                          'decadal1972', 'decadal1973', 'decadal1974',
                          'decadal1975', 'decadal1976', 'decadal1977',
                          'decadal1978', 'decadal1979', 'decadal1980',
                          'decadal1981', 'decadal1982', 'decadal1983',
                          'decadal1984', 'decadal1985', 'decadal1986',
                          'decadal1987', 'decadal1988', 'decadal1989',
                          'decadal1990', 'decadal1991', 'decadal1992',
                          'decadal1993', 'decadal1994', 'decadal1995',
                          'decadal1996', 'decadal1997', 'decadal1998',
                          'decadal1999', 'decadal2000', 'decadal2001',
                          'decadal2002', 'decadal2003', 'decadal2004',
                          'decadal2005', 'decadal2006', 'decadal2007',
                          'decadal2008', 'decadal2009', 'decadal2010',
                          'decadal2011', 'decadal2012', 'decadal2013',
                          'decadal2014', 'decadal2015',
                          'historical', 'rcp45']) or\
            ('CCCma' in instId and 'CanESM2' in srcId and
             'v20130331' in modId[-1]
             and expId in ['1pctCO2', 'abrupt4xCO2', 'esmControl', 'esmFdbk1',
                           'esmFdbk2', 'esmFixClim1', 'esmFixClim2',
                           'esmHistorical', 'esmrcp85', 'historical',
                           'historicalExt', 'historicalGHG', 'historicalMisc',
                           'historicalNat', 'piControl',
                           'rcp26', 'rcp45', 'rcp85']):
            ripfId = modId[7]
        else:
            ripfId = modId[8]
        ripfTest = re.compile('^r\d{1,2}i\d{1,2}p\d{1,3}')
        tabId = '.'.join([modId[6], modId[5]])
        varId = None  # solr scrape was 'tos'
        gridId = None
        verTest = re.compile('^v\d{1,8}')
    elif 'CMIP3' in mipEra:
        actId = 'CMIP'
        instId = modId[1]
        # Kludge for wrong instId
        if instId in 'CSIRO-QCCCE':
            instId = 'CSIRO'
        srcId = modId[2]
        # validate srcId
        expId = modId[3]
        # Kludge actId from expId
        expTest = re.compile('^sres[a-b]\d')
        if expTest.match(expId):
            actId = 'ScenarioMIP'
        ripfId = modId[6]
        ripfTest = re.compile('^run\d{1}')
        tabId = '.'.join([modId[5], modId[4]])
        varId = modId[7]
        gridId = None
        verTest = re.compile('^v\d{1}')
        pass
    # Get generics and validate
    verId = modId[-1]
    nodeId = docId[1]
    # Remap institutions to CMIP6
    instId = instRemap(instId)
    # Print for testing
    # print('mipEra:', mipEra)
    # print('actId:', actId)
    # print('instId:', instId)
    # print('srcId:', srcId)
    # print('expId:', expId)
    # print('ripfId:', ripfId)
    # print('tabId:', tabId)
    # print('varId:', varId)
    # print('gridId:', gridId)
    # print('verId:', verId)
    # print('nodeId:', nodeId)
    # pdb.set_trace()
    # validate ripfId
    if not ripfTest.match(ripfId):
        print('** ripfId format invalid - ripfTest: ', ripfId,
              ', exiting.. **')
        sys.exit()
    # validate verId
    if not verTest.match(verId):
        print('** verId format invalid - verTest: ', verId,
              ', exiting.. **')
        sys.exit()

    return mipEra, actId, instId, srcId, expId, ripfId, tabId, varId, gridId,\
        verId, nodeId


def instRemap(instId):
    """

    Parameters
    ----------
    instId : TYPE
        DESCRIPTION.

    Returns
    -------
    instId : TYPE
        DESCRIPTION.

    """
    # Create CMIP6 alias for earlier mipEras
    if instId in ['BCC', 'BCCR']:
        instId = 'BCC'
    if instId in ['IAP', 'CAS']:
        instId = 'CAS'
    if instId in ['INGV', 'ICHEC', 'CMCC']:
        instId = 'CMCC'
    if instId in ['CRNM_CERFACS', 'CNRM-CERFACS']:
        instId = 'CNRM-CERFACS'
    if instId in ['CSIRO-BOM', 'CSIRO']:
        instId = 'CSIRO'
    if instId in ['FIO', 'FIO-QLNM']:
        instId = 'FIO-QLNM'
    if instId in ['NCAR', 'NSF-DOE-NCAR']:
        instId = 'NCAR'
    if instId in ['NIMR-KMA', 'NIMS-KMA']:
        instId = 'NIMS-KMA'
    if instId in ['GFDL', 'NOAA-GFDL']:
        instId = 'NOAA-GFDL'

    return instId


'''
https://github.com/WCRP-CMIP/CMIP6_CVs/blob/master/CMIP6_institution_id.json 210506 1231
"AER":"Research and Climate Group, Atmospheric and Environmental Research, 131 Hartwell Avenue, Lexington, MA 02421, USA",
"AS-RCEC":"Research Center for Environmental Changes, Academia Sinica, Nankang, Taipei 11529, Taiwan",
"AWI":"Alfred Wegener Institute, Helmholtz Centre for Polar and Marine Research, Am Handelshafen 12, 27570 Bremerhaven, Germany",
"BCC":"Beijing Climate Center, Beijing 100081, China",
"BNU":"Beijing Normal University, Beijing 100875, China",
"CAMS":"Chinese Academy of Meteorological Sciences, Beijing 100081, China",
"CAS":"Chinese Academy of Sciences, Beijing 100029, China",
"CCCR-IITM":"Centre for Climate Change Research, Indian Institute of Tropical Meteorology Pune, Maharashtra 411 008, India",
"CCCma":"Canadian Centre for Climate Modelling and Analysis, Environment and Climate Change Canada, Victoria, BC V8P 5C2, Canada",
"CMCC":"Fondazione Centro Euro-Mediterraneo sui Cambiamenti Climatici, Lecce 73100, Italy",
"CNRM-CERFACS":"CNRM (Centre National de Recherches Meteorologiques, Toulouse 31057, France), CERFACS (Centre Europeen de Recherche et de Formation Avancee en Calcul Scientifique, Toulouse 31057, France)",
"CSIR-Wits-CSIRO":"CSIR (Council for Scientific and Industrial Research - Natural Resources and the Environment, Pretoria, 0001, South Africa), Wits (University of the Witwatersrand - Global Change Institute, Johannesburg 2050, South Africa), CSIRO (Commonwealth Scientific and Industrial Research Organisation, Aspendale, Victoria 3195, Australia)Mailing address: Wits, Global Change Institute, Johannesburg 2050, South Africa",
"CSIRO":"Commonwealth Scientific and Industrial Research Organisation, Aspendale, Victoria 3195, Australia",
"CSIRO-ARCCSS":"CSIRO (Commonwealth Scientific and Industrial Research Organisation, Aspendale, Victoria 3195, Australia), ARCCSS (Australian Research Council Centre of Excellence for Climate System Science). Mailing address: CSIRO, c/o Simon J. Marsland, 107-121 Station Street, Aspendale, Victoria 3195, Australia",
"CSIRO-COSIMA":"CSIRO (Commonwealth Scientific and Industrial Research Organisation, Australia), COSIMA (Consortium for Ocean-Sea Ice Modelling in Australia). Mailing address: CSIRO, c/o Simon J. Marsland, 107-121 Station Street, Aspendale, Victoria 3195, Australia",
"DKRZ":"Deutsches Klimarechenzentrum, Hamburg 20146, Germany",
"DWD":"Deutscher Wetterdienst, Offenbach am Main 63067, Germany",
"E3SM-Project":"LLNL (Lawrence Livermore National Laboratory, Livermore, CA 94550, USA); ANL (Argonne National Laboratory, Argonne, IL 60439, USA); BNL (Brookhaven National Laboratory, Upton, NY 11973, USA); LANL (Los Alamos National Laboratory, Los Alamos, NM 87545, USA); LBNL (Lawrence Berkeley National Laboratory, Berkeley, CA 94720, USA); ORNL (Oak Ridge National Laboratory, Oak Ridge, TN 37831, USA); PNNL (Pacific Northwest National Laboratory, Richland, WA 99352, USA); SNL (Sandia National Laboratories, Albuquerque, NM 87185, USA). Mailing address: LLNL Climate Program, c/o David C. Bader, Principal Investigator, L-103, 7000 East Avenue, Livermore, CA 94550, USA",
"EC-Earth-Consortium":"AEMET, Spain; BSC, Spain; CNR-ISAC, Italy; DMI, Denmark; ENEA, Italy; FMI, Finland; Geomar, Germany; ICHEC, Ireland; ICTP, Italy; IDL, Portugal; IMAU, The Netherlands; IPMA, Portugal; KIT, Karlsruhe, Germany; KNMI, The Netherlands; Lund University, Sweden; Met Eireann, Ireland; NLeSC, The Netherlands; NTNU, Norway; Oxford University, UK; surfSARA, The Netherlands; SMHI, Sweden; Stockholm University, Sweden; Unite ASTR, Belgium; University College Dublin, Ireland; University of Bergen, Norway; University of Copenhagen, Denmark; University of Helsinki, Finland; University of Santiago de Compostela, Spain; Uppsala University, Sweden; Utrecht University, The Netherlands; Vrije Universiteit Amsterdam, the Netherlands; Wageningen University, The Netherlands. Mailing address: EC-Earth consortium, Rossby Center, Swedish Meteorological and Hydrological Institute/SMHI, SE-601 76 Norrkoping, Sweden",
"ECMWF":"European Centre for Medium-Range Weather Forecasts, Reading RG2 9AX, UK",
"FIO-QLNM":"FIO (First Institute of Oceanography, Ministry of Natural Resources, Qingdao 266061, China), QNLM (Qingdao National Laboratory for Marine Science and Technology, Qingdao 266237, China)",
"HAMMOZ-Consortium":"ETH Zurich, Switzerland; Max Planck Institut fur Meteorologie, Germany; Forschungszentrum Julich, Germany; University of Oxford, UK; Finnish Meteorological Institute, Finland; Leibniz Institute for Tropospheric Research, Germany; Center for Climate Systems Modeling (C2SM) at ETH Zurich, Switzerland",
"INM":"Institute for Numerical Mathematics, Russian Academy of Science, Moscow 119991, Russia",
"INPE":"National Institute for Space Research, Cachoeira Paulista, SP 12630-000, Brazil",
"IPSL":"Institut Pierre Simon Laplace, Paris 75252, France",
"KIOST":"Korea Institute of Ocean Science and Technology, Busan 49111, Republic of Korea",
"LLNL":"Lawrence Livermore National Laboratory, Livermore, CA 94550, USA. Mailing address: LLNL Climate Program, c/o Stephen A. Klein, Principal Investigator, L-103, 7000 East Avenue, Livermore, CA 94550, USA",
"MESSy-Consortium":"The Modular Earth Submodel System (MESSy) Consortium, represented by the Institute for Physics of the Atmosphere, Deutsches Zentrum fur Luft- und Raumfahrt (DLR), Wessling, Bavaria 82234, Germany",
"MIROC":"JAMSTEC (Japan Agency for Marine-Earth Science and Technology, Kanagawa 236-0001, Japan), AORI (Atmosphere and Ocean Research Institute, The University of Tokyo, Chiba 277-8564, Japan), NIES (National Institute for Environmental Studies, Ibaraki 305-8506, Japan), and R-CCS (RIKEN Center for Computational Science, Hyogo 650-0047, Japan)",
"MOHC":"Met Office Hadley Centre, Fitzroy Road, Exeter, Devon, EX1 3PB, UK",
"MPI-M":"Max Planck Institute for Meteorology, Hamburg 20146, Germany",
"MRI":"Meteorological Research Institute, Tsukuba, Ibaraki 305-0052, Japan",
"NASA-GISS":"Goddard Institute for Space Studies, New York, NY 10025, USA",
"NASA-GSFC":"NASA Goddard Space Flight Center, Greenbelt, MD 20771, USA",
"NCAR":"National Center for Atmospheric Research, Climate and Global Dynamics Laboratory, 1850 Table Mesa Drive, Boulder, CO 80305, USA",
"NCC":"NorESM Climate modeling Consortium consisting of CICERO (Center for International Climate and Environmental Research, Oslo 0349), MET-Norway (Norwegian Meteorological Institute, Oslo 0313), NERSC (Nansen Environmental and Remote Sensing Center, Bergen 5006), NILU (Norwegian Institute for Air Research, Kjeller 2027), UiB (University of Bergen, Bergen 5007), UiO (University of Oslo, Oslo 0313) and UNI (Uni Research, Bergen 5008), Norway. Mailing address: NCC, c/o MET-Norway, Henrik Mohns plass 1, Oslo 0313, Norway",
"NERC":"Natural Environment Research Council, STFC-RAL, Harwell, Oxford, OX11 0QX, UK",
"NIMS-KMA":"National Institute of Meteorological Sciences/Korea Meteorological Administration, Climate Research Division, Seoho-bukro 33, Seogwipo-si, Jejudo 63568, Republic of Korea",
"NIWA":"National Institute of Water and Atmospheric Research, Hataitai, Wellington 6021, New Zealand",
"NOAA-GFDL":"National Oceanic and Atmospheric Administration, Geophysical Fluid Dynamics Laboratory, Princeton, NJ 08540, USA",
"NTU":"National Taiwan University, Taipei 10650, Taiwan",
"NUIST":"Nanjing University of Information Science and Technology, Nanjing, 210044, China",
"PCMDI":"Program for Climate Model Diagnosis and Intercomparison, Lawrence Livermore National Laboratory, Livermore, CA 94550, USA",
"PNNL-WACCEM":"PNNL (Pacific Northwest National Laboratory), Richland, WA 99352, USA",
"RTE-RRTMGP-Consortium":"AER (Atmospheric and Environmental Research, Lexington, MA 02421, USA); UColorado (University of Colorado, Boulder, CO 80309, USA). Mailing address: AER c/o Eli Mlawer, 131 Hartwell Avenue, Lexington, MA 02421, USA",
"RUBISCO":"ORNL (Oak Ridge National Laboratory, Oak Ridge, TN 37831, USA); ANL (Argonne National Laboratory, Argonne, IL 60439, USA); BNL (Brookhaven National Laboratory, Upton, NY 11973, USA); LANL (Los Alamos National Laboratory, Los Alamos, NM 87545); LBNL (Lawrence Berkeley National Laboratory, Berkeley, CA 94720, USA); NAU (Northern Arizona University, Flagstaff, AZ 86011, USA); NCAR (National Center for Atmospheric Research, Boulder, CO 80305, USA); UCI (University of California Irvine, Irvine, CA 92697, USA); UM (University of Michigan, Ann Arbor, MI 48109, USA). Mailing address: ORNL Climate Change Science Institute, c/o Forrest M. Hoffman, Laboratory Research Manager, Building 4500N Room F106, 1 Bethel Valley Road, Oak Ridge, TN 37831-6301, USA",
"SNU":"Seoul National University, Seoul 08826, Republic of Korea",
"THU":"Department of Earth System Science, Tsinghua University, Beijing 100084, China",
"UA":"Department of Geosciences, University of Arizona, Tucson, AZ 85721, USA",
"UCI":"Department of Earth System Science, University of California Irvine, Irvine, CA 92697, USA",
"UHH":"Universitat Hamburg, Hamburg 20148, Germany",
"UTAS":"Institute for Marine and Antarctic Studies, University of Tasmania, Hobart, Tasmania 7001, Australia",
"UofT":"Department of Physics, University of Toronto, 60 St George Street, Toronto, ON M5S1A7, Canada"
'''

# %% Build list of models per MIP
# Get time
timeFormatDir = datetime.datetime.now().strftime('%y%m%d')
# List input files
fileList = os.listdir(timeFormatDir)
fileList.sort()

# %% Build dictionary keying off source_id
mips = {}
mips['CMIP6'] = {}
mips['CMIP5'] = {}
mips['CMIP3'] = {}

for count1, filePath in enumerate(fileList):
    if 'ESGF.json' in filePath:
        continue
    print('count1', count1, 'filePath:', filePath)
    fullPath = os.path.join(timeFormatDir, filePath)
    print('fullPath:', fullPath)
    with open(fullPath) as jsonFile:
        a = json.load(jsonFile)
        print('a.keys():', a.keys())
        print('a[''response''].keys():', a['response'].keys())
        # Use source_id indexes to build out tree
        for count2, tmp in enumerate(a['response']['docs']):
            print('count2:', count2, 'id:', tmp['id'])
            [mipEra, actId, instId, srcId, expId, ripfId, tabId, varId,
             gridId, verId, nodeId] = siftBits(tmp['id'])
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
            # Build json
            if instId not in mips[mipEra].keys():
                mips[mipEra][instId] = {}
            if srcId not in mips[mipEra][instId].keys():
                mips[mipEra][instId][srcId] = {}
            if actId not in mips[mipEra][instId][srcId].keys():
                mips[mipEra][instId][srcId][actId] = {}
            if expId not in mips[mipEra][instId][srcId][actId].keys():
                mips[mipEra][instId][srcId][actId][expId] = {}
            if ripfId not in mips[mipEra][instId][srcId][actId][expId].keys():
                mips[mipEra][instId][srcId][actId][expId][ripfId] = {}
                # Populate all fields with queries
                queries = ['angular rotation of planet (radians s-1)',
                           'anthropogenic aerosol forcing',
                           'equation of state (and constants)',
                           'freezing equation',
                           'gravitational acceleration (m s-2)',
                           'horizontal resolution',
                           'initialization observed climatology',
                           'mixed-layer scheme',
                           'reference density (boussinesq)',
                           'sea water volume',
                           'spinup length (years)',
                           'vertical diffusivity scheme',
                           'vertical resolution',
                           'volcanic forcing']
                for count3, query in enumerate(queries):
                    mips[mipEra][instId][srcId][actId][expId][ripfId][query]\
                        = None
        print(fullPath)
        print('----------')
        print('----------')
        time.sleep(3)

# Process mipEra result
outFile = os.path.join(timeFormatDir, '_'.join([timeFormatDir,
                                                'CMIP_ESGF.json']))
print('outFile:', outFile)
with open(outFile, 'w', encoding='utf-8') as outJson:
    json.dump(mips, outJson, ensure_ascii=False, indent=4, sort_keys=True)

# %% Build webpages per mipEra
