#!/usr/bin/env python

"""
Copyright 2020 ARC Centre of Excellence for Climate Systems Science

author: Aidan Heerdegen <aidan.heerdegen@anu.edu.au>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import print_function

import argparse
import datetime
import sys
from .UsageDataset import *
from .DBcommon import extract_num_unit, parse_size, mkdir, archive
from .DBcommon import datetoyearquarter, date_range_from_quarter

dbfileprefix = '.'
nfields = 7

def parse_membership(filename, verbose, db=None, dburl=None):

    project = None
    date = None
    system = 'gadi'

    with open(filename) as f:

        print("Parsing {file}".format(file=filename))

        # read 3 lines in membership dump file
        header = f.readline()
        if verbose: print("> ", header)
        
        date_line = f.readline()
        if verbose: print("> ", header)

        data_line = f.readline()

        # parse date from file
        date = datetime.datetime.strptime(date_line.strip(), '%a %b %d %H:%M:%S %Z %Y')

        # parse project_id and members from file
        data_line_parts = data_line.strip().split(":")
        project = data_line_parts[0]
        members_csv = data_line_parts[3]
        members_list = members_csv.split(",")

        # remove service users
        members_list = [ m for m in members_list if not m.endswith("_thredds") ]
        members_list = [ m for m in members_list if not m.endswith("_ci") ]

        members_count = len(members_list)

        # write the results to database
        if verbose: print('Add project membership', project, system, date, members_count)
        db.addprojectmembership(project, system, date, members_list, members_count)

"""
%%%%%%%%%%%%%%%%
Tue Dec 03 11:09:29 AEDT 2024
au88:*:8950:user502,user581,user561
"""

def main(args):

    verbose = args.verbose

    db = None
    if args.dburl:
        db = ProjectDataset(dburl=args.dburl)

    for f in args.inputs:
        try:
            parse_membership(f, verbose, db=db)
        except:
            raise
        else:
            if not args.noarchive:
                archive(f)

def parse_args(args):
    """
    Parse arguments given as list (args)
    """
    parser = argparse.ArgumentParser(description="Parse project membership report dumps")
    parser.add_argument("-v","--verbose", help="Verbose output", action='store_true')
    parser.add_argument("-db","--dburl", help="Database file url", default=None)
    parser.add_argument("-n","--noarchive", help="Database file url", action='store_true')
    parser.add_argument("inputs", help="dumpfiles", nargs='+')

    return parser.parse_args()

def main_parse_args(args):
    """
    Call main with list of arguments. Callable from tests
    """
    # Must return so that check command return value is passed back to calling routine
    # otherwise py.test will fail
    return main(parse_args(args))

def main_argv():
    """
    Call main and pass command line arguments. This is required for setup.py entry_points
    """
    main_parse_args(sys.argv[1:])

if __name__ == "__main__":

    main_argv()

