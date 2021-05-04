#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  4 14:27:40 2021

Extract model information from CMIP6 project direct from ESGF API

PJD 31 Mar 2021 - Started
PJD  4 May 2021 - Finalized working version across CMIP6, 5, 3
                TODO: Cleanup type checking (datetime)

@author: durack1
"""

import argparse
import datetime
import json
import os
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