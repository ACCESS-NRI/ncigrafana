#!/usr/bin/env python

from __future__ import print_function

import datetime
from numpy.testing import assert_array_equal, assert_array_almost_equal
from numpy import arange
import os
import pytest
import time

from ncigrafana.UsageDataset import *
from ncigrafana.DBcommon import datetoyearquarter
from ncigrafana.parse_membership import parse_membership

# Set acceptable time zone strings so we can parse the 
# AEST timezone in the test file
os.environ['TZ'] = 'AEST-10AEDT-11,M10.5.0,M3.5.0'
time.tzset()
dbfileprefix = '.'
verbose = False

@pytest.fixture(scope='session')
def db():
    project = 'xx00'
    dbfile = "sqlite:///:memory:"
    #dbfile = "postgresql://postgres:postgres@localhost:5432/ncigrafana_test"
    return ProjectDataset(project, dbfile)

def test_parse_membership(db):

    parse_membership('test/2024-12-03T11:09:28.au88.membership.dump', verbose=verbose, db=db)

    assert db.db["Users"].count() == 3
    assert db.db["Users"].find_one(user='test581')
    assert db.db["Projects"].find_one(project='au88')

    project_id = db.db["Projects"].find_one(project='au88')['id']
    assert db.db["ProjectMembership"].find_one(project_id=project_id, date=datetime.date(2024,12,3))
    
    membership_record = db.db["ProjectMembership"].find_one(project_id=project_id, date=datetime.date(2024,12,3))
    assert len(membership_record["members"].split(",")) == 3
