#!/bin/env python

'''
To run conversion:
(cdat)duro@ocean:[src]:[master]:[1168]> jsonToHtml.py ../CMIP6_experiment_id.json experiment_id CMIP6_experiment_id.html
{u'note': u'Correct getGitInfo call', u'author': u'Paul J. Durack <durack1@llnl.gov>', u'creation_date': u'Wed Aug 31 16:36:15 2016 -0700',
    u'institution_id': u'PCMDI', u'commit': u'43c311fab67ef26acadbe81f22868691c1357f12', u'latest_tag_point': u'None'}
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
PJD 11 May 2021     - Add humanSort function
PJD 13 May 2021     - Update queries (order and description)
PJD 13 May 2021     - Update instId, srcId etc mappings, remove _, add space
PJD 13 May 2021     - Update html table titles with - to allow word multi-line
PJD 13 May 2021     - queries, add cpocean (specific heat capacity, realign to Griffies et al., 2016 GMD)
PJD 13 May 2021     - More html table titles updated with - to allow word multi-line
PJD 18 May 2021     - Added modId 'ocean model id (+ version)'
PJD  2 Jun 2021     - Updated jquery.dataTables-1.10.24.min.js with 500,1000 entries (line 176)
PJD  3 Jun 2021     - Added exclusion for CMIP5:DCPP/decadalXXXX exps
PJD 21 Jun 2021     - Added geothermal heating (geotHt)
PJD 23 Jun 2021     - Download files from https://datatables.net/download/ [jQuery 3 and dataTables selected, minified];
                      copy css/jquery.dataTables.min.css and datatables.min.js (updating *datatables* -> *dataTables-1.10.25*)
                    - Update dataTables-1.10.25.min.js line 176 update ,aLengthMenu:[10,25,50,100], ->
                    ,aLengthMenu:[5,10,25,50,100,150,200,250,300,350,400], (use jquery.dataTables.js for location lookup [non-minified])
PJD 25 Jun 2021     - Update to read ESGF_Merge.json
PJD  9 Jun 2023     - Download files from https://datatables.net/download/ [jQuery 3 and dataTables selected, minified];
                      copy css/jquery.dataTables.min.css and datatables.min.js (updating *datatables* -> *dataTables-1.14.3*)
                    - Update jquery.dataTables-1.14.3.min.js ,aLengthMenu:[10,25,50,100], ->
                    ,aLengthMenu:[5,10,25,50,100,150,200,250,300,350,400,450,500],
                    - macOS update files to remove
                    extended attributes "$ xattr -c jquery-3.7.0.slim.min.js",
                    "$ xattr -c jquery.dataTables-1.14.3*",
                    "$ xattr -c 230222_DataTables-1p13p3.zip"
                    file permissions "$ chmod 644 jquery.dataTables-1.13*"                    
                    - Update dataTables styling
                    <table id="table_id" class="display"> ->
                    <table id="table_id" class="display compact" style="width:100%">
PJD 14 Jun 2023     - update to use pcmdi.github.io/assets jquery libraries so to single update across repos              
                                        
                   - TODO: Update default page lengths
                   - TODO: Use <td rowspan="2">$50</td> across multiple actIds
                   https://www.w3schools.com/TAgs/tryit.asp?filename=tryhtml_td_rowspan
'''
# This script takes the json file and turns it into a nice
# jquery/data-tabled html doc
import argparse
import copy
import json
import os
#import pdb
import re
import sys

# %% Functions


def humanSort(inList):
    """

    Parameters
    ----------
    inList : list
        input data list

    Returns
    -------
    outList : list
        output data sorted alphanumerically

    """
    outList = copy.copy(inList)

    def convert(text):
        return int(text) if text.isdigit() else text

    def alphanum(key):
        return [convert(c) for c in re.split('([0-9]+)', key)]

    outList.sort(key=alphanum)

    return outList


def markupSwitch(s):
    """
    take string and switch markdown for fully expanded html <a href= ... </a>
    Parameters
    ----------
    is : input data string

    Returns
    -------
    outS : output data string reformatted as html -> <a href="url">link text</a>

    Ref:
        https://stackoverflow.com/questions/23394608/python-regex-fails-to-identify-markdown-links
        https://pynative.com/python-find-position-of-regex-match-using-span-start-end/

    Test strings:
        testStr1 = '[Wright, 1997](https://doi.org/10.1175/1520-0426(1997)014<0735:AEOSFU>2.0.CO;2) (EOS-80; thetao, so/Sp)'
        testStr2 = 'blah blah [Wright, 1997](https://doi.org/10.1175/1520-0426(1997)014<0735:AEOSFU>2.0.CO;2) (EOS-80; thetao, so/Sp)'
        testStr3 = '[Wright, 1997](https://doi.org/10.1175/1520-0426(1997)014<0735:AEOSFU>2.0.CO;2)'
        testStr4 = 'blah blah [Wright, 1997](https://doi.org/10.1175/1520-0426(1997)014<0735:AEOSFU>2.0.CO;2)'
        testStr5 = ' [ ['
        testStr6 = ' '.join(['vertK shear mixing ([Jackson et al., 2008](https://doi.org/10.1175/2007JPO3779.1))',
                             '+ tide mixing ([Melet et al., 2013](https://doi.org/10.1175/JPO-D-12-055.1))',
                             '+ constant background diffusivity 1.5e-5 m-2 s-1 >30n/S, tapering to 2e-6 m-2 s-1 at equator'])
        testStr7 = 'mldSch energy based boundary layer ([Reichl and Hallberg, 2018](https://doi.org/10.1016/j.ocemod.2018.10.004))'
        testStr8 = ''.join(['prescribed aerosol optical properties based on input4MIPs',
                          ' [ETH Zürich (ETHZ), 2017](https://doi.org/10.22033/ESGF/',
                          'input4MIPs.1681)'])
        testStr9 = 'GFDL-MOM6; OM4.25; [Adcroft et al., 2019](https://doi.org/10.1029/2019MS001726)'
        testStr10 = 'KPP diffusivity ([Large et al., 1994](https://doi.org/10.1029/94RG01872))'

    """
    outStrTmp = copy.copy(s)
    #print("outStrTmp in:", outStrTmp)

    # determine number of links
    urlCount = outStrTmp.count("](http")

    # find around span
    markdownMatch = re.compile('\]\(http')

    cnt = 0
    # loop over "(http" entries in string
    while cnt < urlCount:
        cnt += 1
        tmp = markdownMatch.search(outStrTmp)
        #print("tmp:", tmp)
        # find all "[" - start of markdown pattern
        indSquOpen = findChar(outStrTmp, "[")
        #print("indSquOpen:", indSquOpen)
        # find all ")" - end of markdown pattern
        indParOpen = findChar(outStrTmp, ")")
        #print("indParOpen:", indParOpen)
        #print("tmp:", tmp)
        startInd = min(indSquOpen, key=lambda x: abs(x-tmp.start()))
        # pdb.set_trace()
        # check to ensure all parens are greater than startInd
        indParOpen = [x for x in indParOpen if x > startInd]
        # check to ensure all parens are greater than tmp.start()
        indParOpen = [x for x in indParOpen if x > tmp.start()]
        # check to ensure doi url > 39
        if "[Wright, 1997]" in outStrTmp:
            indParOpen = [x for x in indParOpen if (x - tmp.end()) > 39]
        endInd = min(indParOpen, key=lambda x: abs(x-tmp.end()))
        url = outStrTmp[tmp.start()+2:endInd]
        #print("outStrTmp:", outStrTmp)
        #print("url:", url)
        link = outStrTmp[startInd+1:tmp.start()]
        #print("link:", link)
        oldText = outStrTmp[startInd:endInd+1]
        #print("oldText:", oldText)
        newText = flipMarkdown(url, link)
        #print("newText:", newText)
        outStrTmp = outStrTmp.replace(oldText, newText)
        #print("outStrTmp:", outStrTmp)

    return outStrTmp


def findChar(s, ch):
    """
    find all indexes of a single character in a string

    Parameters
    ----------
    s : string
    ch : character to find in string

    Returns
    -------
    list of indexes
    """
    # first check for single character lookup
    if len(ch) != 1:
        print("len(ch) > 1, only single character lookup available, exiting")
        return
    else:
        return [i for i, ltr in enumerate(s) if ltr == ch]


def flipMarkdown(url, link):
    """
    code to flip markdown syntax to html

    Parameters
    ----------
    url : full url using https
    link : descriptive link

    Returns
    -------
    html : fully expanded html link expansion

    """

    # Composite href
    html = ''.join(['<a href="', url, '" target="_blank">',
                    link, '</a>'])

    return html


# %% Create generic header
header = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<meta name="author" content="Paul J. Durack" />
<meta name="description" content="CMIP ocean model configuration information" />
<meta name="keywords" content="HTML, CSS, JavaScript" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<link rel="stylesheet" type="text/css" charset="utf-8" href="https://github.com/PCMDI/assets/blob/main/jquery/jquery.dataTables.min.css" />
<script type="text/javascript" charset="utf-8" src="https://github.com/PCMDI/assets/blob/main/jquery/jquery.slim.min.js"></script>
<script type="text/javascript" charset="utf-8" src="https://github.com/PCMDI/assets/blob/main/jquery/jquery.dataTables.min.js"></script>
<!-- Global site tag (gtag.js) - Google Analytics -->
<script type="text/javascript" src="https://github.com/PCMDI/assets/blob/main/google/googleAnalyticsTag.js" ></script>
<script type="text/javascript">
//<![CDATA[
$(document).ready( function () {
    $('#table_id').DataTable();
    } );
//]]>
</script>\n"""

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
inFile = '../CMIP_Merge.json'
with open(inFile) as jsonFile:
    CMIP = json.load(jsonFile)
CMIP6 = CMIP.get('CMIP6')
CMIP5 = CMIP.get('CMIP5')
CMIP3 = CMIP.get('CMIP3')
versionInfo = CMIP.get('version')

# %% Process html

# Names and varId
queries = {'modId': 'ocean model id (+ version)',
           'eos': 'equation of state (+ constants)',
           'cp': 'specific heat capacity (cpocean, J kg-1 K-1)',
           'refRho': 'reference density (boussinesq; rhozero, kg m-3)',
           'frzEqn': 'freezing point (equation)',
           'angRot': 'planet angular rotation (radians s-1)',
           'graAcc': 'gravitational acceleration (m s-2)',
           'horRes': 'native horizontal resolution',
           'verRes': 'native vertical resolution',
           'vertK': 'vertical diffusivity scheme',
           'mldSch': 'boundary-layer (mixed-) scheme',
           'vol': 'sea water volume',
           'initCl': 'initialization observed climatology',
           'spinYr': 'spinup length (years)',
           'antAer': 'anthropogenic aerosol forcing',
           'volcFo': 'volcanic forcing',
           'aerInd': 'sulphate aerosol indirect effects',
           'geotHt': 'geothermal heating'}

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
                        # Get first ripf values
                        if count5 == 0:
                            for count6, query in enumerate(queries.keys()):
                                vars()[query] = CMIP[instId][srcId][actId][
                                    expId][ripId][queries[query]]
                    dump = [instId, srcId, actId, expId, ripfList]
                    print(dump)
                    CMIPList.append(dump)
    print(CMIPList)
    print('len:', len(CMIPList))
    for count1, val in enumerate(CMIPList):
        print(count1, val)

    # sys.exit()

    fout = os.path.join('..', 'docs', '.'.join([mipEra, 'html']))
    print("processing", fout)
    fo = open(fout, 'w')
    html = ''.join([header, '<title>', mipEra,
                    ' ocean model configurations</title>\n</head>\n<body>\n',
                    '<p>CMIPOcean version: ', version, ' - ', mipEra, '</p>\n',
                    '<table id="table_id" class="display compact" style="width:100%">\n'])
    fo.write(html)

    modKeys = ['source_id', 'activity_id', 'experiment_id', 'ripf',
               'ocean model id (+ version)',
               'EOS (+ constants)',
               'specific heat capacity (cpocean)',
               'ref. density (bouss-inesq, rhozero)',
               'freezing eqn.',
               'planet ang. rotation (radians s-1)',
               'gravit-ational accel. (m s-2)',
               'native horiz. resol-ution',
               'native vert. resol-ution',
               'vertical diffus-ivity scheme',
               'boundary-layer (mld) scheme',
               'sea water volume',
               'initial-ization obs. clim.',
               'spinup length (years)',
               'anthrop. aerosol forcing',
               'volcanic forcing',
               'sulphate aerosol indirect effects',
               'geo-thermal heating']

    first_row = False
    # Create table columns
    if not first_row:
        for hf in ["thead", "tfoot"]:
            fo.write("<%s>\n<tr>\n<th>institution id</th>\n" % hf)
            for i in modKeys:
                i = i.replace('_id', ' id')  # Remove '_' from table titles
                fo.write("<th>%s</th>\n" % i)
            fo.write("</tr>\n</%s>\n" % hf)
    first_row = True
    # Get data and populate rows
    for count, instEntry in enumerate(CMIPList):
        print('instEntry:', instEntry)
        instId, srcId, actId, expId, ripfId = instEntry
        # Check case CMIP5:DCPP
        if mipEra == 'CMIP5' and actId == 'DCPP':
            continue  # Skip decadalXXXX experiments
        print('instId:', instId)
        print('srcId: ', srcId)
        print('actId: ', actId)
        print('expId: ', expId)
        print('ripfId:', ripfId)
        ripfId = humanSort(ripfId)
        print('ripfId (humanSort):', ripfId)
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
        # Write entries for ripf #1
        for count2, key in enumerate(queries):
            # Get query value
            val = CMIP[instId][srcId][actId][expId][ripfId[0]][queries[key]]
            print('key/val:', key, val)
            # if "[(http" in val:
            #    fo.write("<td>%s</td>\n" % markupSwitch(val))
            if isinstance(val, str):
                fo.write("<td>%s</td>\n" % markupSwitch(val))
            else:
                fo.write("<td>%s</td>\n" % val)
            # print(key.ljust(6), ':', val)
        fo.write("</tr>\n")
    fo.write("</table>")
    fo.write("""\n</body>\n</html>\n""")
    fo.close()
