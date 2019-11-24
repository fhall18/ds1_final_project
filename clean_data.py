#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 22:10:38 2019

@author: fhall
"""

#import csv
from datetime import datetime
from dateutil import tz
import pandas as pd



###############################################################################
#### FORMATE DATA ####

# weather data
messy_weather = pd.read_csv('weather_temp_2013-2019.csv')
# delete unused columns
del messy_weather['TOTAL']; del messy_weather['HR25']
weather = pd.melt(messy_weather,
                  id_vars = ['Year','Month','Day'],
                  var_name = 'Hour',
                  value_name = 'Temp'
                  )
# create date... need to add hour...
weather['Hour'] = weather.Hour.str.slice(2,4).astype(int)-1
weather['datetime'] = pd.to_datetime(weather[['Year', 'Month', 'Day', 'Hour']])


# charging sessions data
messy_charging = pd.read_csv('btv_total_charging_sessions.csv')
# delete unused columns
del messy_charging['Org Name']
del messy_charging['MAC Address']
del messy_charging['GHG Savings (kg)']
del messy_charging['Gasoline Savings (gallons)']
del messy_charging['Address 2']
del messy_charging['City']
del messy_charging['State/Province']
del messy_charging['Postal Code']
del messy_charging['Country']
del messy_charging['Currency']
# convert datetimes based on tz
#from_zone = tx.gettx('UTC')
to_zone = tz.gettz('America/New_York')

#messy_charging['Start Date'] = datetime.strptime(messy_charging['Start Date'], '%Y-%m-%d %H:%M:%S')
#messy_charging['Start Date Adjusted'] = messy_charging['Start Time Zone'].apply(lambda x: messy_charging['Start Date'].astimezone(to_zone) if 'UTC' else messy_weather['Start Date'])


print(messy_charging.head())
