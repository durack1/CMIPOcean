#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 18 12:00:39 2021

This file runs code/index updates and applies changes to registered info. The
approach is to build and ESGF-sourced registry (which is frequently updated),
and a CMIP-modeler-sourced registry which is merged to form the html tables

PJD 18 May 2021     - Started
PJD  2 Jun 2021     - Updated to reflect ESGF/modeler-sourced info
PJD 21 Jun 2021     - Added geothermal heating (geotHt)
PJD 22 Jun 2021     - Update to meld resources before writing pages
PJD 23 Jun 2021     - Update index to copy CMIP_ESGF "all"
PJD 10 Jun 2023     - Updated to fix "".join syntax

@author: durack1
"""
# %% imports
import collections
import json
import os
#import pdb

# %% run ESGF index scrape

# %% run modeller data read
CMIP_modeller = {}
CMIP_modeller["CMIP6"] = {}
CMIP_modeller["CMIP5"] = {}
CMIP_modeller["CMIP3"] = {}

# %% queries and default entries
queries = {"modId": "ocean model id (+ version)",
           "eos": "equation of state (+ constants)",
           "cp": "specific heat capacity (cpocean, J kg-1 K-1)",
           "refRho": "reference density (boussinesq; rhozero, kg m-3)",
           "frzEqn": "freezing point (equation)",
           "angRot": "planet angular rotation (radians s-1)",
           "graAcc": "gravitational acceleration (m s-2)",
           "horRes": "native horizontal resolution",
           "verRes": "native vertical resolution",
           "vertK": "vertical diffusivity scheme",
           "mldSch": "boundary-layer (mixed-) scheme",
           "vol": "sea water volume",
           "initCl": "initialization observed climatology",
           "spinYr": "spinup length (years)",
           "antAer": "anthropogenic aerosol forcing",
           "volcFo": "volcanic forcing",
           "aerInd": "sulphate aerosol indirect effects",
           "geotHt": "geothermal heating"}

# template
instKey = "NOAA-GFDL"
modKey = "gfdl_cm_2_0"
modId = "GFDL-MOM4; OM3.0; Delworth et al., 2006, doi: 10.1175/JCLI3629.1"
horRes = "XX x YY longitude/latitude"
verRes = "XX; 50 levels"

# %% apply registered info changes
instKey = "NOAA-GFDL"

# CMIP3 through 6
angRot = 7.2921E-05
graAcc = 9.8
refRho = 1035.0

# CMIP3 through 5
frzEqn = "T_Fr = dTFr_dS * S; dTFr_dS = -0.054"

# %% CMIP3
mipEra = "CMIP3"
CMIP_modeller[mipEra][instKey] = {}

# all CMIP3 models
eos = "".join(["[Jackett et al., 2006](https://doi.org/10.1175/JTECH1946.1)",
               " (EOS-80; thetao, so/Sp)"])
cp = 3992.1
vol = 1.325363E+18
horRes = "tripolar, nominal 1 deg; 360 x 200 longitude/latitude"
verRes = "50 z-vertical layers; top grid cell 0-10 m"
vertK = "".join(["shear mixing ([Large et al., 1994](https://doi.org/10.1029/",
                 "94RG01872)) + tide mixing ([Simmons et al., 2004]",
                 "(https://doi.org/10.1016/j.dsr2.2004.09.015)) + constant ",
                 "background diffusivity 3e-5 m-2 s-1 >30N/S, tapering to ",
                 "1.5e-5 m-2 s-1 at equator with vertical [Bryan and Lewis,",
                 " 1979](https://doi.org/10.1029/JC084iC05p02503) profile"])
mldSch = "".join(["KPP diffusivity ([Large et al., 1994](https://doi.org/",
                  "10.1029/94RG01872))"])
spinYr = 300
initCl = "WOA1998; step-wise initialization"
antAer = "prescribed aerosol concentration"
volcFo = "".join(["prescribed aerosol optical properties ([Sato et al., 1993",
                  " updated](https://doi.org/10.1029/93JD02553) and ",
                  "[Stenchikov et al., 1998](https://doi.org/10.1029/",
                  "98JD00693))"])
aerInd = "prescribed"
geotHt = "None"

# specific CMIP3 models
modId0 = "".join(["GFDL-MOM4; OM3.0; [Delworth et al., 2006]",
                  "(https://doi.org/10.1175/JCLI3629.1)"])
modId1 = "".join(["GFDL-MOM4p1; OM3.1; [Delworth et al., 2006]",
                  "(https://doi.org/10.1175/JCLI3629.1)"])

# overwrite model specific info
for count1, mod in enumerate(["gfdl_cm2_0", "gfdl_cm2_1"]):
    CMIP_modeller[mipEra][instKey][mod] = {}
    CMIP_modeller[mipEra][instKey][mod]["all"] = {}
    CMIP_modeller[mipEra][instKey][mod]["all"]["all"] = {}
    CMIP_modeller[mipEra][instKey][mod]["all"]["all"]["all"] = {}
    for count2, queryKey in enumerate(queries.keys()):
        CMIP_modeller[mipEra][instKey][mod]["all"]["all"]["all"][queryKey] \
            = eval(queryKey)
    # Overwrite default queries
    if mod == "gfdl_cm2_0":
        modId = modId0
    elif mod == "gfdl_cm2_1":
        modId = modId1
    CMIP_modeller[mipEra][instKey][mod]["all"]["all"]["all"]["modId"] = modId

print("----------")
keys = CMIP_modeller["CMIP3"][instKey].keys()
for count, key in enumerate(keys):
    print(key)
    print(CMIP_modeller["CMIP3"][instKey][key])

# %% CMIP5
mipEra = "CMIP5"
CMIP_modeller[mipEra][instKey] = {}

# all CMIP5 models
eos = "".join(["[Jackett et al., 2006](https://doi.org/10.1175/JTECH1946.1)",
               " (EOS-80; thetao, so/Sp)"])
cp = 3992.1
vol = 1.325363E+18
horRes = "tripolar, nominal 1 deg; 360 x 200 longitude/latitude"
verRes = "50 z-vertical layers; top grid cell 0-10 m"
vertK = "".join(["shear mixing ([Large et al., 1994](https://doi.org/10.1029/",
                 "94RG01872)) + tide mixing ([Simmons et al., 2004]",
                 "(https://doi.org/10.1016/j.dsr2.2004.09.015)) + constant ",
                 "background diffusivity 3e-5 m-2 s-1 >30N/S, tapering to ",
                 "1.5e-5 m-2 s-1 at equator with vertical [Bryan and Lewis,",
                 " 1979](https://doi.org/10.1029/JC084iC05p02503) profile"])
mldSch = "".join(["KPP diffusivity ([Large et al., 1994](https://doi.org/",
                  "10.1029/94RG01872))"])
spinYr = 1000
initCl = "WOA1998; step-wise initialization"
volcFo = "".join(["prescribed aerosol optical properties ([Sato et al., 1993",
                  " updated](https://doi.org/10.1029/93JD02553) and ",
                  "[Stenchikov et al., 1998](https://doi.org/10.1029/",
                  "98JD00693))"])

# specific CMIP5 models
antAerCM = "".join(["emission-driven based on [Lamarque et al., 2010]",
                    "(https://doi.org/10.5194/acp-10-7017-2010) ",
                    "(full chemistry)"])
aerIndCM = "yes, based on bulk mass concentration"
modIdCM = "".join(["GFDL-MOM4; OM3.0; [Delworth et al., 2006]",
                   "(https://doi.org/10.1175/JCLI3629.1)"])

initClESM = "WOA2005"
antAerESM = "prescribed aerosol concentration"
aerIndESM = "prescribed"
geotHtESM = "".join(["50 mW m-2; [Adcroft et al., 2001](https://doi.org/",
                     "10.1029/2000GL012182)"])

eos2G = "".join(["[Wright, 1997](https://doi.org/10.1175/1520-0426(1997)014%",
                 "3C0735AEOSFU%3E2.0.CO;2) (EOS-80; thetao, so/Sp)"])
cp2G = 3925.0
vol2G = 1.33291E+18
horRes2G = "tripolar, nominal 1 deg; 360 x 210 longitude/latitude"
verRes2G = "".join(["59 rho2000 layers + 4 z-like layers in upper boundary ",
                    "(rho2000 = potential density referenced to 2000dbar); ",
                    "top grid cell 0-10 m"])
vertK2G = "".join(["shear mixing ([Jackson et al., 2008](https://doi.org/",
                   "10.1175/2007JPO3779.1)) + tide mixing ([Simmons et al., ",
                   "2004](https://doi.org/10.1016/j.dsr2.2004.09.015)) + ",
                   "bottom boundary layer [Legg and Huijts, 2006](https://doi",
                   ".org/10.1016/j.dsr2.2005.09.014) + constant background ",
                   "diffusivity 2e-5 m-2 s-1 >30N/S, tapering to 2e-6 m-2 ",
                   "s-1 at equator"])
mldSch2G = "".join(["bulk mixed layer ([Hallberg, 2003](http://www.soest.",
                    "hawaii.edu/PubServices/2003pdfs/Hallberg.pdf))"])
modId2G = "GFDL-GOLD; Hallberg, 1995"

vertK2M = "".join(["shear mixing ([Large et al., 1994](https://doi.org/",
                   "10.1029/94RG01872)) + tide mixing ([Simmons et al., 2004]",
                   "(https://doi.org/10.1016/j.dsr2.2004.09.015)) + constant ",
                   "background diffusivity 1.5e-5 m-2 s-1 >30N/S, tapering ",
                   "to 1e-5 m-2 s-1 at equator"])
modId2M = "".join(["GFDL-MOM4p1; OM3.1; [Delworth et al., 2006]",
                   "(https://doi.org/10.1175/JCLI3629.1)"])

# overwrite model specific info
for count1, mod in enumerate(["GFDL-CM2p1", "GFDL-CM3", "GFDL-ESM2G",
                              "GFDL-ESM2M"]):
    CMIP_modeller[mipEra][instKey][mod] = {}
    CMIP_modeller[mipEra][instKey][mod]["all"] = {}
    CMIP_modeller[mipEra][instKey][mod]["all"]["all"] = {}
    CMIP_modeller[mipEra][instKey][mod]["all"]["all"]["all"] = {}
    # Overwrite default queries
    if mod == "GFDL-CM3":
        modId = modIdCM
        antAer = antAerCM
        aerInd = aerIndCM
    elif mod == "GFDL-ESM2G":
        modId = modId2G
        eos = eos2G
        cp = cp2G
        horRes = horRes2G
        verRes = verRes2G
        vertK = vertK2G
        mldSch = mldSch2G
        initCl = initClESM
        antAer = antAerESM
        aerInd = aerIndESM
        geotHt = geotHtESM
    elif mod == "GFDL-ESM2M":
        modId = modId2M
        initCl = initClESM
        antAer = antAerESM
        aerInd = aerIndESM
        geotHt = geotHtESM
    for count2, queryKey in enumerate(queries.keys()):
        CMIP_modeller[mipEra][instKey][mod]["all"]["all"]["all"][queryKey] \
            = eval(queryKey)

print("----------")
keys = CMIP_modeller["CMIP5"][instKey].keys()
for count, key in enumerate(keys):
    print(key)
    print(CMIP_modeller["CMIP5"][instKey][key])

# %% CMIP6
mipEra = "CMIP6"
CMIP_modeller[mipEra][instKey] = {}

# all CMIP6 models
modId = "".join(["GFDL-MOM6; OM4.25; [Adcroft et al., 2019](https://doi.org/",
                 "10.1029/2019MS001726)"])
eos = "".join(["[Wright, 1997](https://doi.org/10.1175/1520-0426(1997)014",
               "<0735:AEOSFU>2.0.CO;2) (EOS-80; thetao, so/Sp)"])
cp = 3992.0
refRho = 1035.0
frzEqn = " ".join(["T_Fr = dTFr_dS * S + dTFr_dp * pres; dTFr_dS = -0.054,",
                   "dTFr_dp = -7.75e-8, pres = gauge pressure (Pa)"])
# angRot
# graAcc
horRes = "tripolar, nominal 0.25 deg; 1440 x 1080 longitude/latitude"
verRes = "75 hybrid layers (z* and rho2000); top grid cell 0-2 m"
vertK = "".join(["shear mixing ([Jackson et al., 2008](https://doi.org/",
                 "10.1175/2007JPO3779.1)), + tide mixing ([Melet et al., 2013",
                 "](https://doi.org/10.1175/JPO-D-12-055.1)), + constant",
                 " background diffusivity 1.5e-5 m-2 s-1 >30n/S, tapering to",
                 "2e-6 m-2 s-1 at equator"])
mldSch = "".join(["energy based boundary layer ([Reichl and Hallberg, 2018]",
                  "(https://doi.org/10.1016/j.ocemod.2018.10.004))"])
vol = 1.33511E+18
initCl = "WOA2013"
spinYr = 600
antAer = "emission-driven based on input4MIPs; CM4 has simplified chemistry"
volcFo = "".join(["prescribed aerosol optical properties based on input4MIPs",
                  " [ETH Zürich (ETHZ), 2017](https://doi.org/10.22033/ESGF/",
                  "input4MIPs.1681)"])
aerInd = "yes; based on bulk mass concentration"
geotHt = "".join(["95.9 mW m-2; [Davies, 2013](https://doi.org/",
                  "10.1002/ggge.20271)"])

# specific CMIP6 models
key = "GFDL-ESM2M"
modIdE2M = "".join(["GFDL-MOM4p1; OM3.1; [Dunne et al., 2012](https://doi.org/",
                    "10.1175/JCLI-D-11-00560.1)"])
eosE2M = "".join(["[Jackett et al., 2006](https://doi.org/10.1175/JTECH1946.1",
                  ") (EOS-80; thetao, so/Sp)"])
cpE2M = 3992.1
frzEqnE2M = "T_Fr = dTFr_dS * S; dTFr_dS = -0.054"
horResE2M = "tripolar, nominal 1 deg; 360 x 200 longitude/latitude"
verResE2M = "50 z-vertical layers; top grid cell 0-10 m"
vertKE2M = "".join(["shear mixing ([Large et al., 1994](https://doi.org/",
                    "10.1029/94RG01872)) + tide mixing ([Simmons et al., 2004",
                    "](https://doi.org/10.1016/j.dsr2.2004.09.015)) + ",
                    "constant background diffusivity 1.5e-5 m-2 s-1 >30N/S, ",
                    "tapering to 1e-5 m-2 s-1 at equator"])
mldSchE2M = "".join(["KPP diffusivity ([Large et al., 1994](https://doi.org/",
                     "10.1029/94RG01872))"])
volE2M = 1.325363E+18
initClE2M = "WOA2005"
spinYrE2M = 1000
antAerE2M = "prescribed aerosol concentration"
volcFoE2M = "".join(["prescribed aerosol optical properties [Sato et al., ",
                     "1993 updated](https://doi.org/10.1029/93JD02553) and ",
                     "[Stenchikov et al., 1998](https://doi.org/10.1029/",
                     "98JD00693)"])
aerIndE2M = "prescribed"
geotHtE2M = "".join(["50 mW m-2; [Adcroft et al., 2001](https://doi.org/",
                     "10.1029/2000GL012182)"])

key = "GFDL-ESM4" or "GFDL-OM4p5B"
modIdE4 = "".join(["GFDL-MOM6; OM4.5; [Adcroft et al., 2019](https://doi.org/",
                   "10.1029/2019MS001726)"])
horResE4 = "tripolar, nominal 0.5 deg; 720 x 576 longitude/latitude"
volE4 = 1.33480E+18
spinYrE4 = 1000
geotHtE4 = "".join(["95.9 mW m-2; [Davies, 2013](https://doi.org/",
                    "10.1002/ggge.20271)"])

# overwrite model specific info
for count1, mod in enumerate(["GFDL-CM4", "GFDL-ESM2M", "GFDL-ESM4",
                              "GFDL-OM4p5B"]):
    CMIP_modeller[mipEra][instKey][mod] = {}
    CMIP_modeller[mipEra][instKey][mod]["all"] = {}
    CMIP_modeller[mipEra][instKey][mod]["all"]["all"] = {}
    CMIP_modeller[mipEra][instKey][mod]["all"]["all"]["all"] = {}
    # Overwrite default queries
    if mod == "GFDL-ESM2M":
        modId = modIdE2M
        eos = eosE2M
        cp = cpE2M
        frzEqn = frzEqnE2M
        horRes = horResE2M
        verRes = verResE2M
        vertK = vertKE2M
        mldSch = mldSchE2M
        vol = volE2M
        initCl = initClE2M
        spinYr = spinYrE2M
        antAer = antAerE2M
        volcFo = volcFoE2M
        aerInd = aerIndE2M
        geotHt = geotHtE2M
    elif mod in ["GFDL-ESM4", "GFDL-OM4p5B"]:
        modId = modIdE4
        horRes = horResE4
        vol = volE4
        spinYr = spinYrE4
        geotHt = geotHtE4  # Reinstate
    for count2, queryKey in enumerate(queries.keys()):
        CMIP_modeller[mipEra][instKey][mod]["all"]["all"]["all"][queryKey] \
            = eval(queryKey)

print("----------")
keys = CMIP_modeller["CMIP6"][instKey].keys()
for count, key in enumerate(keys):
    print(key)
    print(CMIP_modeller["CMIP6"][instKey][key])

# %% finally sort
CMIP_modeller = collections.OrderedDict(CMIP_modeller)

# Process data to file
outFile = os.path.join("..", "CMIP_Modeller.json")
print("outFile:", outFile)
with open(outFile, "w", encoding="utf-8") as outJson:
    json.dump(CMIP_modeller, outJson, ensure_ascii=False, indent=4,
              sort_keys=True)

# %% Now meld resources (ESGF index, modeller sourced info) and write html
# CMIP_ESGF.     CMIP6.NOAA-GFDL.GFDL-CM4.CMIP.1pctCO2.r1i1p1f1.query
# CMIP6_Modeller.CMIP6.NOAA-GFDL.GFDL-CM4.                      query

# Load CMIP_ESGF
inFile = "../CMIP_ESGF.json"
with open(inFile) as jsonFile:
    CMIP_merge = json.load(jsonFile)

    # Overwrite CMIP_ESGF with CMIP_Modeller values
    for countm, mipEra in enumerate(CMIP_modeller.keys()):
        print("countm:", countm, mipEra)
        for counti, instId in enumerate(CMIP_modeller[mipEra].keys()):
            print("counti", counti, instId)
            for countM, modIdM in enumerate(CMIP_modeller[mipEra]
                                            [instId].keys()):
                print("countM:", countM, modIdM)
                for counta, actId in enumerate(CMIP_modeller[mipEra]
                                               [instId][modIdM].keys()):
                    print("counta:", counta, actId)
                    for counte, expId in enumerate(CMIP_modeller[mipEra]
                                                   [instId][modIdM]
                                                   [actId].keys()):
                        print("counte:", counte, expId)
                        for countr, ripId in enumerate(CMIP_modeller[mipEra]
                                                       [instId][modIdM]
                                                       [actId].keys()):
                            print("countr:", countr, ripId)
                            # Test for all cases
                            if "all" in {actId, expId, ripId}:
                                print("all across all")
                                # Impose changes across all published instances
                                for countaM, actIdM in enumerate(CMIP_merge
                                                                 [mipEra]
                                                                 [instId]
                                                                 [modIdM]
                                                                 .keys()):
                                    for counteM, expIdM in enumerate(CMIP_merge
                                                                     [mipEra]
                                                                     [instId]
                                                                     [modIdM]
                                                                     [actIdM]
                                                                     .keys()):
                                        for countrM, ripIdM in enumerate(
                                                CMIP_merge[mipEra][instId]
                                                [modIdM][actIdM][expIdM]
                                                .keys()):
                                            print(mipEra, instId, modIdM,
                                                  actIdM, expIdM, ripIdM)
                                            for query in queries.keys():
                                                print("-----")
                                                #print("query:", query)
                                                #print("modId", modIdM)
                                                # print("keys:", CMIP_modeller
                                                #      [mipEra][instId].keys())
                                                # print("keys:", CMIP_modeller
                                                #      [mipEra][instId][modIdM]
                                                #      [actId][expId][ripId]
                                                #      .keys())
                                                # print("query:", CMIP_modeller
                                                #      [mipEra][instId][modIdM]
                                                #      [actId][expId][ripId]
                                                #      [query])
                                                # Reassign value over ESGF
                                                print("Merge:", CMIP_merge
                                                      [mipEra][instId][modIdM]
                                                      [actIdM][expIdM][ripIdM]
                                                      [queries[query]])
                                                print("modeller:",
                                                      CMIP_modeller[mipEra]
                                                      [instId][modIdM][actId]
                                                      [expId][ripId][query])
                                                print("modeller type:",
                                                      type(CMIP_modeller
                                                           [mipEra][instId]
                                                           [modIdM][actId]
                                                           [expId][ripId]
                                                           [query]))
                                                print("queries:",
                                                      queries[query])
                                                # Overwrite values
                                                CMIP_merge[mipEra][instId][modIdM][actIdM][expIdM][ripIdM][queries[query]] =\
                                                    CMIP_modeller[mipEra][instId][modIdM][actId][expId][ripId][query]
                                                print("after")
                                                print(CMIP_merge[mipEra]
                                                      [instId][modIdM][actIdM]
                                                      [expIdM][ripIdM]
                                                      [queries[query]])
                            else:
                                print("all not in all")

# Send revised CMIP_ESGF to jsonToHtml as argument (no file read/open)
# Process data to file
outFile = os.path.join("..", "CMIP_Merge.json")
print("outFile:", outFile)
with open(outFile, "w", encoding="utf-8") as outJson:
    json.dump(CMIP_merge, outJson, ensure_ascii=False, indent=4,
              sort_keys=True)
