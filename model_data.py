#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 22:10:38 2019

@author: fhall, spell, jhardy
"""

#import csv
import collections
from datetime import datetime
from dateutil import tz

import pandas as pd
from pytz import all_timezones


###############################################################################
#### FORMATE DATA ####

### Weather Data
# data = pd.read_csv('ev_type.csv')
# print(data)

data = pd.read_csv('btv_total_charging_sessions.csv')
for i in data:
    print(i)
