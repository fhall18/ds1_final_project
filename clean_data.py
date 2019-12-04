#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 22:10:38 2019
@author: fhall, spell, jhardy
"""

# import csv
import collections
import math
from datetime import datetime
from dateutil import tz

import pandas as pd
from pytz import all_timezones

###############################################################################
#### FORMAT DATA ####

### Weather Data
messy_weather = pd.read_csv('weather_temp_2013-2019.csv')
# delete unused columns
del messy_weather['TOTAL'];
del messy_weather['HR25']
weather = pd.melt(messy_weather,
                  id_vars=['Year', 'Month', 'Day'],
                  var_name='Hour',
                  value_name='Temp'
                  )

# create date... need to add hour...
weather['Hour'] = weather.Hour.str.slice(2, 4).astype(int) - 1
weather['datetime'] = pd.to_datetime(weather[['Year', 'Month', 'Day', 'Hour']])

# clean up unused fields
del weather['Year']
del weather['Month']
del weather['Day']
del weather['Hour']

### Charging sessions data
messy_charging = pd.read_csv('btv_total_charging_sessions.csv')

# delete unused columns
del messy_charging['Org Name']
del messy_charging['MAC Address']
del messy_charging['Transaction Date (Pacific Time)']
del messy_charging['GHG Savings (kg)']
del messy_charging['Gasoline Savings (gallons)']
del messy_charging['Address 2']
del messy_charging['City']
del messy_charging['State/Province']
del messy_charging['Postal Code']
del messy_charging['Country']
del messy_charging['Currency']

# convert to datetime
# messy_charging['Start Date'] = pd.to_datetime(messy_charging['Start Date'],infer_datetime_format=True)
messy_charging['Start Date'] = pd.to_datetime(messy_charging['Start Date'], format='%Y-%m-%d %H:%M:%S')
# messy_charging['End Date'] = pd.to_datetime(messy_charging['Start Date'],infer_datetime_format=True)
messy_charging['End Date'] = pd.to_datetime(messy_charging['End Date'], format='%Y-%m-%d %H:%M:%S')

### Timezones
# from_zone = tx.gettx('UTC')
# to_zone = tz.gettz('America/New_York')

# index datetimes
start_date = messy_charging['Start Date']
start_date = pd.Index(start_date)
# localize
start_date = start_date.tz_localize(None)
messy_charging['Start Date'] = start_date

# convert based on TZ
# messy_charging['Start Date'] = messy_charging['Start Time Zone'].apply(lambda x: messy_charging['Start Date'].tz_localize('utc') if 'UTC'
#              else messy_weather['Start Date'].tz_localize('utc'))

# messy_charging['Start Date'] = messy_charging['Start Date'].tz_localize(None)

# start_time = messy_charging['Start Date']
# start_time_idx = pd.Index(start_time)

# start_time_idx = start_time_idx.tz_localize('utc')
# start_time_idx = start_time_idx.tz_convert(tz = 'America/New_York')
# messy_charging['Start Date Index'] = start_time_idx


# messy_charging['Start Date Adjusted'] = messy_charging['Start Time Zone'].apply(lambda x: messy_charging['Start Date Index'].astimezone(to_zone) if 'UTC' else messy_weather['Start Date Index'])
# messy_charging['Start Date Adjusted'] = messy_charging['Start Time Zone'].apply(lambda x: messy_charging['Start Date'].tz_convert('America/New_York') if 'UTC' else messy_weather['Start Date'])

# print("start time:", start_time.dtypes)
# print("start time idx:", start_time_idx.dtypes)


# rounding dates to the nearest hour
messy_charging['Start Date Truncated'] = messy_charging['Start Date'].dt.round('60T')
messy_charging['End Date Truncated'] = messy_charging['End Date'].dt.round('60T')

# create clean version
charging = pd.DataFrame.copy(messy_charging)
charging.rename(columns={'User ID': 'User_ID'}, inplace=True)

### Electric Vehicle Make-Model-Year Data
# ev_specs = pd.read_csv('data/')

# need to fill this out with EV/PHEV data
# Fields:
# make, model, year, AEV or PHEV, battery kWh, lvl 2 kW charging, DCFC capable


# Merge
weather = weather.rename(columns={'datetime': 'Start Date Truncated'})
data = charging.merge(weather, on='Start Date Truncated')

# print(data.dtypes)
# print(data.head())

# driver ID filter out NAN values
data[data.User_ID.notnull()]
driver_id = data["User_ID"]
counts = collections.Counter(driver_id)

charge_end = data["Ended By"]
charge_end_counts = collections.Counter(charge_end)

# variables we care about:

### DATETIME ###
# Start Date
# End Date
# Charging Time (hh:mm:ss)
# Charge End (formula: "Start Date" + "Charge Duration")

### CHARGING ###
# Energy (kWh)
# Average kW (formula: Energy (kWh) / Charging Time (hh:mm:ss))
avg_kw = []
energy = data["Energy (kWh)"]
time = data["Charging Time (hh:mm:ss)"]
list_len = len(energy)

for i in range(list_len):
    t = datetime.strptime(time[i], "%H:%M:%S").time()
    t = t.hour + t.minute / 60
    if (t != 0):
        avg_kw.append(energy[i] / t)
    else:
        avg_kw.append(None)
# print(avg_kw)

####BATTERY SIZE####
# Start SOC
# End SOC
start_soc = data["Start SOC"]
end_soc = data["End SOC"]
# battery_sizes = []
# ct = 0
# ct2 = 0
# for i in range(list_len):
#     # if start_soc[i] != "nan" and end_soc[i] != "nan":
#     print(energy[i], end_soc[i], start_soc[i])
#     if math.isnan(start_soc[i]):
#         ct += 1
#     if end_soc[i] == "nan":
#         ct2 += 1
# print('hi')
# print(list_len, ct, ct2)

        # battery_sizes.append(energy[i] / (end_soc - start_soc))

# print(battery_sizes)

# Temp
# Ended By (variable of how the session was terminated)
# Full Charge (binary variable - Formula:
# if Ended By == "Driver Unplugged" & total duration > charge duration

### EVSE ###
# Address 1
# Port Type
# Ended By

### Driver ###
# User_ID
# Driver Postal Code ??

### Variables We Want ###
# EV Make
# EV Model
# EV Year

### Variables We Can Create ###
# vehicle battery size FORMULA:
# max(Energy)
# Energy / (SOC End - SOC Start)
# Energy / (100 - SOC Start) if Ended By == Charger Stopped & Charge Duration < Total Duration
