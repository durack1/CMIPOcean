#!/bin/env python

'''
To run conversion:
(cdat)duro@ocean:[src]:[master]:[1168]> jsonToHtml.py ../CMIP6_experiment_id.json experiment_id CMIP6_experiment_id.html
{u'note': u'Correct getGitInfo call', u'author': u'Paul J. Durack <durack1@llnl.gov>', u'creation_date': u'Wed Aug 31 16:36:15 2016 -0700', u'institution_id': u'PCMDI', u'commit': u'43c311fab67ef26acadbe81f22868691c1357f12', u'latest_tag_point': u'None'}
Notes:
http://stackoverflow.com/questions/6551446/can-i-run-html-files-directly-from-github-instead-of-just-viewing-their-source

PJD  6 May 2021     - Copy from https://github.com/WCRP-CMIP/CMIP6_CVs/blob/master/src/json_to_html.py and update input
PJD  6 May 2021     - Download jquery 3.6.0, dataTables 1.10.24
                    - Download file from https://jquery.com/download/ - select "Download the compressed, production jQuery 3.6.0 slim build
                    - Download files from https://datatables.net/download/ [jQuery 3 and dataTables selected, minified];
                      copy css/jquery.dataTables.min.css and js/jquery.dataTables.min.js (updating *dataTables* -> *dataTables-1.10.24*)
                    - Update jquery.dataTables-1.10.24.min.js line 176 update ,aLengthMenu:[10,25,50,100], ->
                    ,aLengthMenu:[5,10,25,50,100,150,200,250,300,350,400], (use jquery.dataTables.js for location lookup [non-minified])
                    https://www.w3.org/International/questions/qa-html-encoding-declarations
                    https://validator.w3.org/check
                   - TODO: Update default page lengths
'''
# This script takes the json file and turns it into a nice jquery/data-tabled html doc
import argparse
import json
import os
import re
import sys

# %% Create generic header
header = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<meta name="author" content="Paul J. Durack" />
<meta name="description" content="CMIP ocean model configuration information" />
<meta name="keywords" content="HTML, CSS, JavaScript" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<link rel="stylesheet" type="text/css" charset="utf-8" href="../src/jquery.dataTables-1.10.24.min.css" />
<script type="text/javascript" charset="utf-8" src="../src/jquery-3.6.0.slim.min.js"></script>
<script type="text/javascript" charset="utf-8" src="../src/jquery.dataTables-1.10.24.min.js"></script>
<script type="text/javascript">
//<![CDATA[
$(document).ready( function () {
    $('#table_id').DataTable();
    } );
//]]>
</script>"""

# 190425 Updates below fail
# <script type="text/javascript">
# //<![CDATA[
# $(document).ready( function () {
#    $('#table_id').DataTable( {
#      "pageLength": 50,
#      "lengthMenu": [ [5,10,25,50,100,150,200,250,300,-1], [5,10,25,50,100,150,200,250,300,"All"] ]
#    } );
# //]]>
# </script>"""

# %% Argparse extract
# Matching version format 0.10.23
verTest = re.compile(r'[0-2][.][0-9]+[.][0-9]+')
parser = argparse.ArgumentParser()
parser.add_argument('ver', metavar='str', type=str,
                    help=' '.join(['For e.g. \'0.10.23\' as a command line',
                                   'argument will ensure version information',
                                   'is written to the html output']))
args = parser.parse_args()
if re.search(verTest, args.ver):
    version = args.ver  # 1 = make files
    print('** HTML Write mode - ', version, ' will be written **')
else:
    print('** Version: ', version, ' invalid, exiting')
    sys.exit()

# %% Set global arguments
destDir = '../docs/'

# %% Read data
inFile = '../CMIP_ESGF.json'
with open(inFile) as jsonFile:
    CMIP = json.load(jsonFile)
CMIP6 = CMIP.get('CMIP6')
CMIP5 = CMIP.get('CMIP5')
CMIP3 = CMIP.get('CMIP3')
versionInfo = CMIP.get('version')

# %% Process html

for mipEra in ['CMIP6', 'CMIP5', 'CMIP3']:
    print(mipEra)
    CMIP = eval(mipEra)

    fout = os.path.join('..', 'docs', '.'.join([mipEra, 'html']))
    print("processing", fout)
    # fout = fout.split('/')[-1] ; # Write to local directory
    fo = open(fout, 'w')

    #print(header)
    #print(mipEra)
    #print(version)
    html = ''.join([header, '<title>', mipEra,
                    ' ocean model configurations</title>\n</head>\n<body>',
                    '<p>CMIPOcean version: ', version, '</p>',
                    '<table id="table_id" class="display">\n'])
    #print(html)
    fo.write(html)

    # dictOrder = [
    #     'label_extended', 'atmospheric_chemistry', 'atmosphere',
    #     'ocean_biogeochemistry', 'release_year', 'cohort', 'sea_ice', 'label',
    #     'institution_id', 'land_surface', 'aerosol', 'source_id', 'ocean',
    #     'land_ice', 'activity_participation',
    #     'native_nominal_resolution_atmos', 'native_nominal_resolution_landIce',
    #     'native_nominal_resolution_ocean']
    # dictOrderKold = [
    #     'institution_id', 'release_year', 'activity_participation',
    #     'atmosphere', 'nominal_resolution_atmos', 'ocean',
    #     'nominal_resolution_ocean', 'aerosol', 'atmospheric_chemistry',
    #     'cohort', 'label', 'label_extended', 'land_ice',
    #     'nominal_resolution_landIce', 'land_surface', 'ocean_biogeochemistry',
    #     'sea_ice']
    # dictOrderK = [
    #     'institution_id', 'release_year', 'activity_participation', 'cohort',
    #     'label', 'label_extended', 'atmos', 'natNomRes_atmos', 'ocean',
    #     'natNomRes_ocean', 'landIce', 'natNomRes_landIce', 'aerosol',
    #     'atmosChem', 'land', 'ocnBgchem', 'seaIce']
    # dictRealmKeys = [
    #     'atmos', 'ocean', 'aerosol', 'landIce', 'atmosChem', 'land',
    #     'ocnBgchem', 'seaIce']
    # dictNomResKeys = ['natNomRes_atmos',
    #                   'natNomRes_ocean', 'natNomRes_landIce']

    modKeys = ['source_id', 'activity_id', 'experiment_id', 'ripf',
               'angular rotation of planet (radians s-1)',
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

    first_row = False
    # Create table columns
    if not first_row:
        for hf in ["thead", "tfoot"]:
            fo.write("<%s>\n<tr>\n<th>institutionId</th>\n" % hf)
            for i in modKeys:
                i = i.replace('_id', 'Id')  # Remove '_' from table titles
                fo.write("<th>%s</th>\n" % i)
            fo.write("</tr>\n</%s>\n" % hf)
    first_row = True
    # Get data and populate rows
    for instId in CMIP.keys():
        fo.write("<tr>\n<td>%s</td>\n" % instId)
        # Deal with more than single model
        srcId = CMIP[instId]
        print('srcId:', srcId)
        fo.write("<td>%s</td>\n" % srcId)
        actId = CMIP[instId][srcId]
        print('actId:', actId)
        fo.write("<td>%s</td>\n" % actId)
        expId = CMIP[instId][srcId][actId]
        fo.write("<td>%s</td>\n" % expId)
        ripf = CMIP[instId][srcId][actId][expId]
        fo.write("<td>%s</td>\n" % ripf)
        # Fill rows with values
        for k in modKeys:
            val = CMIP[instId][srcId][actId][expId][k]
            fo.write("<td>%s</td>\n" % val)
        fo.write("</tr>\n")
    fo.write("</table>")
    fo.write("""\n</body>\n</html>\n""")
    fo.close()

    # first_row = False
    # print(CMIP.keys())
    # print(CMIP['AS-RCEC'].keys())
    # for exp in CMIP.keys():
    #     exp_dict = CMIP[exp]
    #     # Create table columns
    #     if not first_row:
    #         for hf in ["thead", "tfoot"]:
    #             fo.write("<%s>\n<tr>\n<th>institutionId</th>\n" % hf)
    #             for i in modKeys:
    #                 i = i.replace('_id', 'Id')  # Remove '_' from table titles
    #                 fo.write("<th>%s</th>\n" % i)
    #             fo.write("</tr>\n</%s>\n" % hf)
    #     first_row = True
    #     fo.write("<tr>\n<td>%s</td>\n" % exp)
    #     # Fill rows with values
    #     for k in modKeys:
    #         # Deal with embeds
    #         if k in dictRealmKeys:
    #             st = exp_dict['model_component'][k]['description']
    #         elif k in dictNomResKeys:
    #             keyVal = k.replace('natNomRes_', '')
    #             st = exp_dict['model_component'][keyVal]
    #             ['native_nominal_resolution']
    #         else:
    #             st = exp_dict[k]
    #         if isinstance(st, (list, tuple)):
    #             st = " ".join(st)
    #         fo.write("<td>%s</td>\n" % st)
    #     fo.write("</tr>\n")
    # fo.write("</table>")
    # fo.write("""\n</body>\n</html>\n""")
    # fo.close()
