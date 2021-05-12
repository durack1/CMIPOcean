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
PJD 11 May 2021     - Updated to working version
PJD 11 May 2021     - Correct *.dataTables-* capitalization
                   - TODO: Update default page lengths
'''
# This script takes the json file and turns it into a nice
# jquery/data-tabled html doc
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
<link rel="stylesheet" type="text/css" charset="utf-8" href="https://wcrp-cmip.github.io/CMIP6_CVs/src/jquery.dataTables-1.10.20.min.css" />
<script type="text/javascript" charset="utf-8" src="https://wcrp-cmip.github.io/CMIP6_CVs/src/jquery-3.5.0.slim.min.js"></script>
<script type="text/javascript" charset="utf-8" src="https://wcrp-cmip.github.io/CMIP6_CVs/src/jquery.dataTables-1.10.20.min.js"></script>
<script type="text/javascript">
//<![CDATA[
$(document).ready( function () {
    $('#table_id').DataTable();
    } );
//]]>
</script>\n"""

# <script type="text/javascript" charset="utf-8" src="../src/jquery-3.6.0.slim.min.js"></script>

# <link rel="stylesheet" type="text/css" charset="utf-8" href="../src/jquery.dataTables-1.10.24.min.css" />
# <script type="text/javascript" charset="utf-8" src="../src/jquery-3.3.1.min.js"></script>
# <script type="text/javascript" charset="utf-8" src="../src/jquery.dataTables-1.10.24.min.js"></script>

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
    # Preformat inputs to be a single line for each source_id
    CMIPList = []  # [[] for _ in range(1)]
    for count1, instId in enumerate(CMIP.keys()):
        print(count1, instId)
        for count2, srcId in enumerate(CMIP[instId].keys()):
            print(count2, instId, srcId)
            for count3, actId in enumerate(CMIP[instId][srcId].keys()):
                print(count3, instId, srcId, actId)
                for count4, expId in enumerate(CMIP[instId][srcId][actId]):
                    print(count4, instId, srcId, actId, expId)
                    ripfList = []
                    for count5, ripId in\
                            enumerate(CMIP[instId][srcId][actId][expId]):
                        print(count5, instId, srcId, actId, expId, ripId)
                        ripfList.append(ripId)
                    dump = [instId, srcId, actId, expId, ripfList]
                    print(dump)
                    CMIPList.append(dump)
    print(CMIPList)
    print('len:', len(CMIPList))
    for count1, val in enumerate(CMIPList):
        print(count1, val)

    fout = os.path.join('..', 'docs', '.'.join([mipEra, 'html']))
    print("processing", fout)
    fo = open(fout, 'w')
    html = ''.join([header, '<title>', mipEra,
                    ' ocean model configurations</title>\n</head>\n<body>\n',
                    '<p>CMIPOcean version: ', version, ' - ', mipEra, '</p>\n',
                    '<table id="table_id" class="display">\n'])
    fo.write(html)

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
    for count, instEntry in enumerate(CMIPList):
        print('instEntry:', instEntry)
        instId, srcId, actId, expId, ripfId = instEntry
        print('instId:', instId)
        print('srcId: ', srcId)
        print('actId: ', actId)
        print('expId: ', expId)
        print('ripfId:', ripfId)
        fo.write("<tr>\n<td>%s</td>\n" % instId)
        # Deal with more than single model
        fo.write("<td>%s</td>\n" % srcId)
        fo.write("<td>%s</td>\n" % actId)
        fo.write("<td>%s</td>\n" % expId)
        ripfStr = ''
        ripfStr = ', '.join([str(rip) for rip in ripfId])
        print('ripfStr:', ripfStr)
        fo.write("<td>%s</td>\n" % ripfStr)
        del(ripfStr)
        fo.write("</tr>\n")
    fo.write("</table>")
    fo.write("""\n</body>\n</html>\n""")
    fo.close()
