#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  4 14:27:40 2021

Extract model information from CMIP6 project direct from ESGF API

PJD 31 Mar 2021 - Started
PJD  4 May 2021 - Finalized working version across CMIP6, 5, 3

@author: durack1
"""

import argparse
import datetime
import json
import os
#import pdb
import requests

#%%
timeNow = datetime.datetime.now()
timeFormat = timeNow.strftime('%y%m%d')
timeFormatY = timeNow.strftime('%Y-%m-%d')

#%%
def get_solr_query_url():
    search_url = 'https://esgf-node.llnl.gov/esg-search/search/' \
                 '?limit=0&format=application%2Fsolr%2Bjson'

    req = requests.get(search_url)
    js = json.loads(req.text)
    shards = js['responseHeader']['params']['shards']

    solr_url = 'https://esgf-node.llnl.gov/solr/datasets/select' \
               '?q=*:*&wt=json&facet=true&rows=50000&fq=type:Dataset' \
               '{{query}}&shards={shards}'
    # Limit to unique/latest only - '&fq=replica:false&fq=latest:true&{{query}}&shards={shards}'
    # Set row size to 1M - &rows=1000000; CMIP5 'tos' == 31050, max out at 50k

    return solr_url.format(shards=shards)

#%%
def get_dataset_time_data(project, activity_id, variable_id,
                          experiment_id=None,
                          start_date="2018-07-01",
                          end_date=timeFormatY):
    """
    dfd.
    https://esgf-node.llnl.gov/solr/datasets/select?q=*:*&wt=json&facet=true&rows=2165&fq=type:Dataset&fq=variable_id:tos&fq=activity_id:CMIP&fq=experiment_id:historical

    https://esgf-node.llnl.gov/solr/datasets/select?q=*:*&wt=json&facet=true&rows=2165&fq=type:Dataset&fq=mip_era:CMIP6&fq=activity_id:CMIP&fq=experiment_id:historical&fq=variable_id:tos

    https://esgf-node.llnl.gov/solr/datasets/select?q=*:*&wt=json&facet=true&rows=2165&fq=type:Dataset&fq=project:CMIP5&fq=experiment:historical&fq=variable:tos

    https://esgf-node.llnl.gov/solr/datasets/select?q=*:*&wt=json&facet=true&rows=2165&fq=type:Dataset&fq=project:CMIP3&fq=experiment:historical&fq=variable:tos

    https://esgf-node.llnl.gov/solr/datasets/select?q=*:*&wt=json&facet=true&rows=4000&fq=type:Dataset&fq=mip_era:CMIP6&fq=activity_id:CMIP&fq=experiment_id:historical&fq=variable_id:tos&shards=localhost:8983/solr/datasets,localhost:8985/solr/datasets,localhost:8987/solr/datasets,localhost:8988/solr/datasets,localhost:8990/solr/datasets,localhost:8993/solr/datasets,localhost:8994/solr/datasets,localhost:8995/solr/datasets,localhost:8996/solr/datasets,localhost:8997/solr/datasets


[ml-9585568:sync/git/McDougalletal21GMD] durack1% python
Python 3.8.5 (default, Sep  4 2020, 02:22:02)
[Clang 10.0.0 ] :: Anaconda, Inc. on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import json
>>> a = json.load(open('data.json'))
>>> a.keys()
dict_keys(['responseHeader', 'response', 'facet_counts'])
>>> a['response'].keys()
dict_keys(['numFound', 'start', 'maxScore', 'docs'])
>>> a['response']['docs']
[{'id': 'CMIP6.CMIP.BCC.BCC-CSM2-MR.esm-hist.r1i1p1f1.3hr.tos.gn.v20181128|cmip.bcc.cma.cn', 'version': '20181128', 'access': ['HTTPServer', 'GridFTP', 'OPENDAP', 'Globus', 'LAS'], 'activity_drs': ['CMIP'], 'activity_id': ['CMIP'], 'branch_method': ['Standard'], 'cf_standard_name': ['sea_surface_temperature'], 'citation_url': ['http://cera-www.dkrz.de/WDCC/meta/CMIP6/CMIP6.CMIP.BCC.BCC-CSM2-MR.esm-hist.r1i1p1f1.3hr.tos.gn.v20181128.json'], 'data_node': 'cmip.bcc.cma.cn', 'data_specs_version': ['01.00.27'], 'dataset_id_template_': ['%(mip_era)s.%(activity_drs)s.%(institution_id)s.%(source_id)s.%(experiment_id)s.%(member_id)s.%(table_id)s.%(variable_id)s.%(grid_label)s'], 'datetime_start': '1950-01-01T00:00:00Z', 'datetime_stop': '2014-12-31T21:00:00Z', 'directory_format_template_': ['%(root)s/%(mip_era)s/%(activity_drs)s/%(institution_id)s/%(source_id)s/%(experiment_id)s/%(member_id)s/%(table_id)s/%(variable_id)s/%(grid_label)s/%(version)s'], 'east_degrees': 358.875, 'experiment_id': ['esm-hist'], 'experiment_title': ['all-forcing simulation of the recent past with atmospheric CO2 concentration calculated'], 'frequency': ['3hrPt'], 'further_info_url': ['https://furtherinfo.es-doc.org/CMIP6.BCC.BCC-CSM2-MR.esm-hist.none.r1i1p1f1'], 'geo': ['ENVELOPE(-180.0, -1.125, 89.14152, -89.14152)', 'ENVELOPE(0.0, 180.0, 89.14152, -89.14152)'], 'geo_units': ['degrees_east'], 'grid': ['T106'], 'grid_label': ['gn'], 'index_node': 'esgf-node.llnl.gov', 'instance_id': 'CMIP6.CMIP.BCC.BCC-CSM2-MR.esm-hist.r1i1p1f1.3hr.tos.gn.v20181128', 'institution_id': ['BCC'], 'latest': True, 'master_id': 'CMIP6.CMIP.BCC.BCC-CSM2-MR.esm-hist.r1i1p1f1.3hr.tos.gn', 'member_id': ['r1i1p1f1'], 'mip_era': ['CMIP6'], 'model_cohort': ['Registered'], 'nominal_resolution': ['100 km'], 'north_degrees': 89.14152, 'number_of_aggregations': 2, 'number_of_files': 22, 'pid': ['hdl:21.14100/94b8d8d6-9bb9-398d-8de7-0d0c02a1ce5a'], 'product': ['model-output'], 'project': ['CMIP6'], 'realm': ['ocean'], 'replica': False, 'size': 38876161920, 'source_id': ['BCC-CSM2-MR'], 'source_type': ['AOGCM', 'BGC'], 'south_degrees': -89.14152, 'sub_experiment_id': ['none'], 'table_id': ['3hr'], 'title': 'CMIP6.CMIP.BCC.BCC-CSM2-MR.esm-hist.r1i1p1f1.3hr.tos.gn', 'type': 'Dataset', 'url': ['http://cmip.bcc.cma.cn/thredds/catalog/esgcet/2/CMIP6.CMIP.BCC.BCC-CSM2-MR.esm-hist.r1i1p1f1.3hr.tos.gn.v20181128.xml#CMIP6.CMIP.BCC.BCC-CSM2-MR.esm-hist.r1i1p1f1.3hr.tos.gn.v20181128|application/xml+thredds|THREDDS', 'http://cmip.bcc.cma.cn/las/getUI.do?catid=EB786448FBF51A03B90A8DE0356CDAF5_ns_CMIP6.CMIP.BCC.BCC-CSM2-MR.esm-hist.r1i1p1f1.3hr.tos.gn.v20181128|application/las|LAS'], 'variable': ['tos'], 'variable_id': ['tos'], 'variable_long_name': ['Sea Surface Temperature'], 'variable_units': ['degC'], 'variant_label': ['r1i1p1f1'], 'west_degrees': 0.0, 'xlink': ['http://cera-www.dkrz.de/WDCC/meta/CMIP6/CMIP6.CMIP.BCC.BCC-CSM2-MR.esm-hist.r1i1p1f1.3hr.tos.gn.v20181128.json|Citation|citation', 'http://hdl.handle.net/hdl:21.14100/94b8d8d6-9bb9-398d-8de7-0d0c02a1ce5a|PID|pid'], '_version_': 1647705611744313344, 'retracted': False, '_timestamp': '2019-10-18T04:55:22.919Z', 'score': 1.0}, {'id': 'CMIP6.CMIP.BCC.BCC-CSM2-MR.esm-hist.r1i1p1f1.Omon.tos.gn.v20181211|cmip.bcc.cma.cn', 'version': '20181211', 'access': ['HTTPServer', 'GridFTP', 'OPENDAP', 'Globus', 'LAS'], 'activity_drs': ['CMIP'], 'activity_id': ['CMIP'], 'branch_method': ['Standard'], 'cf_standard_name': ['sea_surface_temperature'], 'citation_url': ['http://cera-www.dkrz.de/WDCC/meta/CMIP6/CMIP6.CMIP.BCC.BCC-CSM2-MR.esm-hist.r1i1p1f1.Omon.tos.gn.v20181211.json'], 'data_node': 'cmip.bcc.cma.cn', 'data_specs_version': ['01.00.27'], 'dataset_id_template_': ['%(mip_era)s.%(activity_drs)s.%(institution_id)s.%(source_id)s.%(experiment_id)s.%(member_id)s.%(table_id)s.%(variable_id)s.%(grid_label)s'], 'datetime_start': '1850-01-16T12:00:00Z', 'datetime_stop': '2014-12-16T12:00:00Z', 'directory_format_template_': ['%(root)s/%(mip_era)s/%(activity_drs)s/%(institution_id)s/%(source_id)s/%(experiment_id)s/%(member_id)s/%(table_id)s/%(variable_id)s/%(grid_label)s/%(version)s'], 'east_degrees': 359.5, 'experiment_id': ['esm-hist'], 'experiment_title': ['all-forcing simulation of the recent past with atmospheric CO2 concentration calculated'], 'frequency': ['mon'], 'further_info_url': ['https://furtherinfo.es-doc.org/CMIP6.BCC.BCC-CSM2-MR.esm-hist.none.r1i1p1f1'], 'geo': ['ENVELOPE(-180.0, -0.5, 89.5, -81.5)', 'ENVELOPE(0.5, 180.0, 89.5, -81.5)'], 'geo_units': ['degrees_east'], 'grid': ['native ocean tri-polar grid'], 'grid_label': ['gn'], 'index_node': 'esgf-node.llnl.gov', 'instance_id': 'CMIP6.CMIP.BCC.BCC-CSM2-MR.esm-hist.r1i1p1f1.Omon.tos.gn.v20181211', 'institution_id': ['BCC'], 'latest': True, 'master_id': 'CMIP6.CMIP.BCC.BCC-CSM2-MR.esm-hist.r1i1p1f1.Omon.tos.gn', 'member_id': ['r1i1p1f1'], 'mip_era': ['CMIP6'], 'model_cohort': ['Registered'], 'nominal_resolution': ['100 km'], 'north_degrees': 89.5, 'number_of_aggregations': 2, 'number_of_files': 1, 'pid': ['hdl:21.14100/f1b9d0de-bca4-35d0-8e22-e28f64187dfd'], 'product': ['model-output'], 'project': ['CMIP6'], 'realm': ['ocean'], 'replica': False, 'size': 662222868, 'source_id': ['BCC-CSM2-MR'], 'source_type': ['AOGCM', 'BGC'], 'south_degrees': -81.5, 'sub_experiment_id': ['none'], 'table_id': ['Omon'], 'title': 'CMIP6.CMIP.BCC.BCC-CSM2-MR.esm-hist.r1i1p1f1.Omon.tos.gn', 'type': 'Dataset', 'url': ['http://cmip.bcc.cma.cn/thredds/catalog/esgcet/2/CMIP6.CMIP.BCC.BCC-CSM2-MR.esm-hist.r1i1p1f1.Omon.tos.gn.v20181211.xml#CMIP6.CMIP.BCC.BCC-CSM2-MR.esm-hist.r1i1p1f1.Omon.tos.gn.v20181211|application/xml+thredds|THREDDS', 'http://cmip.bcc.cma.cn/las/getUI.do?catid=EB786448FBF51A03B90A8DE0356CDAF5_ns_CMIP6.CMIP.BCC.BCC-CSM2-MR.esm-hist.r1i1p1f1.Omon.tos.gn.v20181211|application/las|LAS'], 'variable': ['tos'], 'variable_id': ['tos'], 'variable_long_name': ['Sea Surface Temperature'], 'variable_units': ['degC'], 'variant_label': ['r1i1p1f1'], 'west_degrees': 0.5, 'xlink': ['http://cera-www.dkrz.de/WDCC/meta/CMIP6/CMIP6.CMIP.BCC.BCC-CSM2-MR.esm-hist.r1i1p1f1.Omon.tos.gn.v20181211.json|Citation|citation', 'http://hdl.handle.net/hdl:21.14100/f1b9d0de-bca4-35d0-8e22-e28f64187dfd|PID|pid'], '_version_': 1647713021116547072, 'retracted': False, '_timestamp': '2019-10-18T06:53:09.047Z', 'score': 1.0}

>>> a['response']['docs'][0]
{'id': 'CMIP6.CMIP.BCC.BCC-CSM2-MR.esm-hist.r1i1p1f1.3hr.tos.gn.v20181128|cmip.bcc.cma.cn', 'version': '20181128', 'access': ['HTTPServer', 'GridFTP', 'OPENDAP', 'Globus', 'LAS'], 'activity_drs': ['CMIP'], 'activity_id': ['CMIP'], 'branch_method': ['Standard'], 'cf_standard_name': ['sea_surface_temperature'], 'citation_url': ['http://cera-www.dkrz.de/WDCC/meta/CMIP6/CMIP6.CMIP.BCC.BCC-CSM2-MR.esm-hist.r1i1p1f1.3hr.tos.gn.v20181128.json'], 'data_node': 'cmip.bcc.cma.cn', 'data_specs_version': ['01.00.27'], 'dataset_id_template_': ['%(mip_era)s.%(activity_drs)s.%(institution_id)s.%(source_id)s.%(experiment_id)s.%(member_id)s.%(table_id)s.%(variable_id)s.%(grid_label)s'], 'datetime_start': '1950-01-01T00:00:00Z', 'datetime_stop': '2014-12-31T21:00:00Z', 'directory_format_template_': ['%(root)s/%(mip_era)s/%(activity_drs)s/%(institution_id)s/%(source_id)s/%(experiment_id)s/%(member_id)s/%(table_id)s/%(variable_id)s/%(grid_label)s/%(version)s'], 'east_degrees': 358.875, 'experiment_id': ['esm-hist'], 'experiment_title': ['all-forcing simulation of the recent past with atmospheric CO2 concentration calculated'], 'frequency': ['3hrPt'], 'further_info_url': ['https://furtherinfo.es-doc.org/CMIP6.BCC.BCC-CSM2-MR.esm-hist.none.r1i1p1f1'], 'geo': ['ENVELOPE(-180.0, -1.125, 89.14152, -89.14152)', 'ENVELOPE(0.0, 180.0, 89.14152, -89.14152)'], 'geo_units': ['degrees_east'], 'grid': ['T106'], 'grid_label': ['gn'], 'index_node': 'esgf-node.llnl.gov', 'instance_id': 'CMIP6.CMIP.BCC.BCC-CSM2-MR.esm-hist.r1i1p1f1.3hr.tos.gn.v20181128', 'institution_id': ['BCC'], 'latest': True, 'master_id': 'CMIP6.CMIP.BCC.BCC-CSM2-MR.esm-hist.r1i1p1f1.3hr.tos.gn', 'member_id': ['r1i1p1f1'], 'mip_era': ['CMIP6'], 'model_cohort': ['Registered'], 'nominal_resolution': ['100 km'], 'north_degrees': 89.14152, 'number_of_aggregations': 2, 'number_of_files': 22, 'pid': ['hdl:21.14100/94b8d8d6-9bb9-398d-8de7-0d0c02a1ce5a'], 'product': ['model-output'], 'project': ['CMIP6'], 'realm': ['ocean'], 'replica': False, 'size': 38876161920, 'source_id': ['BCC-CSM2-MR'], 'source_type': ['AOGCM', 'BGC'], 'south_degrees': -89.14152, 'sub_experiment_id': ['none'], 'table_id': ['3hr'], 'title': 'CMIP6.CMIP.BCC.BCC-CSM2-MR.esm-hist.r1i1p1f1.3hr.tos.gn', 'type': 'Dataset', 'url': ['http://cmip.bcc.cma.cn/thredds/catalog/esgcet/2/CMIP6.CMIP.BCC.BCC-CSM2-MR.esm-hist.r1i1p1f1.3hr.tos.gn.v20181128.xml#CMIP6.CMIP.BCC.BCC-CSM2-MR.esm-hist.r1i1p1f1.3hr.tos.gn.v20181128|application/xml+thredds|THREDDS', 'http://cmip.bcc.cma.cn/las/getUI.do?catid=EB786448FBF51A03B90A8DE0356CDAF5_ns_CMIP6.CMIP.BCC.BCC-CSM2-MR.esm-hist.r1i1p1f1.3hr.tos.gn.v20181128|application/las|LAS'], 'variable': ['tos'], 'variable_id': ['tos'], 'variable_long_name': ['Sea Surface Temperature'], 'variable_units': ['degC'], 'variant_label': ['r1i1p1f1'], 'west_degrees': 0.0, 'xlink': ['http://cera-www.dkrz.de/WDCC/meta/CMIP6/CMIP6.CMIP.BCC.BCC-CSM2-MR.esm-hist.r1i1p1f1.3hr.tos.gn.v20181128.json|Citation|citation', 'http://hdl.handle.net/hdl:21.14100/94b8d8d6-9bb9-398d-8de7-0d0c02a1ce5a|PID|pid'], '_version_': 1647705611744313344, 'retracted': False, '_timestamp': '2019-10-18T04:55:22.919Z', 'score': 1.0}
>>> a['response']['docs'][0].keys()
dict_keys(['id', 'version', 'access', 'activity_drs', 'activity_id', 'branch_method', 'cf_standard_name', 'citation_url', 'data_node', 'data_specs_version', 'dataset_id_template_', 'datetime_start', 'datetime_stop', 'directory_format_template_', 'east_degrees', 'experiment_id', 'experiment_title', 'frequency', 'further_info_url', 'geo', 'geo_units', 'grid', 'grid_label', 'index_node', 'instance_id', 'institution_id', 'latest', 'master_id', 'member_id', 'mip_era', 'model_cohort', 'nominal_resolution', 'north_degrees', 'number_of_aggregations', 'number_of_files', 'pid', 'product', 'project', 'realm', 'replica', 'size', 'source_id', 'source_type', 'south_degrees', 'sub_experiment_id', 'table_id', 'title', 'type', 'url', 'variable', 'variable_id', 'variable_long_name', 'variable_units', 'variant_label', 'west_degrees', 'xlink', '_version_', 'retracted', '_timestamp', 'score'])
>>> len(a['response']['docs'])
2019

    Parameters
    ----------
    project : TYPE
        DESCRIPTION.
    activity_id : TYPE
        DESCRIPTION.
    experiment_id : TYPE
        DESCRIPTION. The default is None.
    variable_id : TYPE
        DESCRIPTION.
    start_date : TYPE, optional
        DESCRIPTION. The default is None.
    end_date : TYPE, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    js : TYPE
        DESCRIPTION.

    """
    date_format = '%Y-%m-%dT%H:%M:%SZ'
    start_str = start_date #start_date.strftime(date_format)
    end_str = end_date #end_date.strftime(date_format)

    solr_url = get_solr_query_url()

    # Set query URL by ESGF project
    query = '&fq=project:{project}'
    if project == 'CMIP6':
        if activity_id:
            query += '&fq=activity_id:{activity_id}'
        if variable_id:
            query += '&fq=variable_id:{variable_id}'
    else:
        if variable_id:
            query += '&fq=variable:{variable_id}'

    query_url = solr_url.format(query=query.format(project=project,
                                                   start_date=start_str,
                                                   end_date=end_str,
                                                   activity_id=activity_id,
                                                   experiment_id=experiment_id,
                                                   variable_id=variable_id))

    print('query_url:\n', query_url)

    req = requests.get(query_url)
    js = json.loads(req.text)

    return js


#%%
def main():

    parser = argparse.ArgumentParser(description="Gather dataset counts per day from ESGF")
    parser.add_argument("--project", "-p", dest="project", type=str, default="CMIP6", help="MIP project name (default is CMIP6)")
    parser.add_argument("--activity_id", "-ai", dest="activity_id", type=str, default=None, help="MIP activity id (default is None)")
    parser.add_argument("--experiment_id", "-ei", dest="experiment_id", type=str, default=None, help="MIP experiment id (default is None)")
    parser.add_argument("--variable_id", "-vi", dest="variable_id", type=str, default="tos", help="MIP variable id (default is 'tos')")
    parser.add_argument("--start_date", "-sd", dest="start_date", type=str, default="2018-07-01", help="Start date in YYYY-MM-DD format (default is 2018-07-01)")
    parser.add_argument("--end_date", "-ed", dest="end_date", type=str, default=datetime.datetime.now().strftime('%Y-%m-%d'), help="End date in YYYY-MM-DD format (default is current date)")
    parser.add_argument("--output", "-o", dest="output", type=str, default=os.path.curdir, help="Output directory (default is current directory)")
    args = parser.parse_args()

    if args.start_date is None:
        print("You must enter a start date.")
        return
    else:
        try:
            start_date = datetime.datetime.strptime(args.start_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect start date format, should be YYYY-MM-DD")
            return

    if args.end_date is None:
        print("You must enter an end date.")
        return
    else:
        try:
            end_date = datetime.datetime.strptime(args.end_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect end date format, should be YYYY-MM-DD")
            return

    if not os.path.isdir(args.output):
        print("{} is not a directory. Exiting.".format(args.output))
        return

    print('call get_dataset_time_data')
    js = get_dataset_time_data(project=args.project,
                               start_date=start_date,
                               end_date=end_date,
                               activity_id=args.activity_id,
                               experiment_id=args.experiment_id,
                               variable_id=args.variable_id)

    return js


if __name__ == '__main__':
    main()