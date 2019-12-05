#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 22:10:38 2019

@author: fhall, spell, jhardy
"""
#### IMPORTS ##################################################################
import collections
from datetime import datetime
from dateutil import tz
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from pytz import all_timezones

#### FUNCTIONS ################################################################

def series_to_list_of_nums(some_series):
    some_list = []
    for i in some_series:
        num = int(i)
        some_list.append(num)
    
    return some_list

def series_to_list_of_percents(some_series):
    some_list = []
    for i in some_series:
        num = i[:-1]
        num = int(num)/100
        some_list.append(num)
    
    return some_list


#### FORMAT DATA ##############################################################

####################
#### AMI DATA ######

dcfc_ami = pd.read_csv('data/dcfc_ami.csv')

energy = dcfc_ami['LP_VALUE']
demand = []
# compute demand (kW)
for i in range(len(energy)):
    demand.append(i*4)

dcfc_ami['demand'] = demand

# restructure datetime
dcfc_time = dcfc_ami['INTERVAL_TIME']
dcfc_time_list = []

for i in range(len(dcfc_time)):
    dt = dcfc_time[i]
    dt = datetime.strptime(dt, '%m/%d/%Y %H:%M:%S')
    dcfc_time_list.append(dt)

dcfc_ami['INTERVAL_TIME'] = dcfc_time_list
dcfc_ami['Start Date Truncated'] = dcfc_ami['INTERVAL_TIME'].dt.round('60T')   


####################
### Weather Data ###
messy_weather = pd.read_csv('data/weather_temp_2013-2019.csv')
del messy_weather['TOTAL']; del messy_weather['HR25']
weather = pd.melt(messy_weather,
                  id_vars = ['Year','Month','Day'],
                  var_name = 'Hour',
                  value_name = 'Temp'
                  )
# create datetime
weather['Hour'] = weather.Hour.str.slice(2,4).astype(int)-1
weather['datetime'] = pd.to_datetime(weather[['Year', 'Month', 'Day', 'Hour']])

# remove unused fields
del weather['Month']
del weather['Day']
del weather['Hour']

##############################
### Charging Sessions Data ###
messy_charging = pd.read_csv('data/btv_total_charging_sessions.csv')

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
del messy_charging['Station Name']


# convert to datetime
#messy_charging['Start Date'] = pd.to_datetime(messy_charging['Start Date'],infer_datetime_format=True)
messy_charging['Start Date'] = pd.to_datetime(messy_charging['Start Date'],format='%Y-%m-%d %H:%M:%S')
#messy_charging['End Date'] = pd.to_datetime(messy_charging['Start Date'],infer_datetime_format=True)
messy_charging['End Date']=pd.to_datetime(messy_charging['End Date'],format='%Y-%m-%d %H:%M:%S')


### Timezones
#from_zone = tx.gettx('UTC')
#to_zone = tz.gettz('America/New_York')

# index datetimes
start_date = messy_charging['Start Date']
start_date = pd.Index(start_date)
# localize
start_date = start_date.tz_localize(None)
messy_charging['Start Date'] = start_date

# convert based on TZ
#messy_charging['Start Date'] = messy_charging['Start Time Zone'].apply(lambda x: messy_charging['Start Date'].tz_localize('utc') if 'UTC' 
#              else messy_weather['Start Date'].tz_localize('utc'))

#messy_charging['Start Date'] = messy_charging['Start Date'].tz_localize(None)

#start_time = messy_charging['Start Date']
#start_time_idx = pd.Index(start_time)

#start_time_idx = start_time_idx.tz_localize('utc')
#start_time_idx = start_time_idx.tz_convert(tz = 'America/New_York')
#messy_charging['Start Date Index'] = start_time_idx


#messy_charging['Start Date Adjusted'] = messy_charging['Start Time Zone'].apply(lambda x: messy_charging['Start Date Index'].astimezone(to_zone) if 'UTC' else messy_weather['Start Date Index'])
#messy_charging['Start Date Adjusted'] = messy_charging['Start Time Zone'].apply(lambda x: messy_charging['Start Date'].tz_convert('America/New_York') if 'UTC' else messy_weather['Start Date'])

#print("start time:", start_time.dtypes)
#print("start time idx:", start_time_idx.dtypes)


# rounding dates to the nearest hour
messy_charging['Start Date Truncated'] = messy_charging['Start Date'].dt.round('60T')
messy_charging['End Date Truncated'] = messy_charging['End Date'].dt.round('60T')

#### Filter ###################################################################

#rename variables
messy_charging.rename(columns={'User ID':'User_ID', 'Ended By':'Ended_By', 
                               'Port Type':'Port_Type', 'Start SOC':'Start_SOC',
                               'End SOC':'End_SOC', 'Total Duration (hh:mm:ss)':'total_time',
                               'Charging Time (hh:mm:ss)':'charge_time',
                               'Energy (kWh)':'energy'}, inplace=True)

messy_charging = messy_charging[messy_charging.User_ID.notnull()] # driver ID filter out NAN values
messy_charging = messy_charging[messy_charging['energy'] > 0] # energy greater than zero

# filter Ended By: Customer, Plug Out at Vehicle, or Plug Out at Station
end_charging = ["Customer", "Plug Out at Vehicle", "Plug Out at Station"]
messy_charging = messy_charging[messy_charging.Ended_By.isin(end_charging)]


# create clean version
charging = pd.DataFrame.copy(messy_charging)


### Electric Vehicle Make-Model-Year Data
#ev_specs = pd.read_csv('data/')

# need to fill this out with EV/PHEV data
# Fields: 
# make, model, year, AEV or PHEV, battery kWh, lvl 2 kW charging, DCFC capable


#### MERGE 1 ##################################################################
weather = weather.rename(columns={'datetime' : 'Start Date Truncated'})
data = charging.merge(weather, on='Start Date Truncated')

# merge ami with weather
dcfc_ami = dcfc_ami.merge(weather, on='Start Date Truncated')

#### Build Variables ##########################################################

# estimate for battery size
max_energy = data.groupby(['User_ID'], sort=False)['energy'].max()
max_energy = max_energy.to_frame()

# estimate for model year
min_year = data.groupby(['User_ID'], sort=False)['Year'].min()
min_year = min_year.to_frame()

# merge and rename
driver_stats = max_energy.merge(min_year, on='User_ID')
driver_stats.rename(columns={'Year':'model_year', 
                               'energy':'battery_size'}, inplace=True)

# create average kw
avg_kw = []
energy = data["energy"]
time = data["charge_time"]
list_len = len(energy)

for i in range(list_len):
    t = datetime.strptime(time[i], "%H:%M:%S").time()
    t = t.hour + t.minute/60
    if(t != 0):
        avg_kw.append(energy[i]/t)
    else:
        avg_kw.append(None)



#### MERGE 2 ##################################################################
data = data.merge(driver_stats, on='User_ID')
data['avg_kw'] = avg_kw


#### DCFC DATA ################################################################

# filters
data = data[data.Port_Type == 'DC Fast']
data = data[data.avg_kw < 40] # strange datapoint higher than 40 kW...
data = data[data.Start_SOC.notnull()]

print(data.shape)


# change SOC to numbers
soc_a = data['Start_SOC']
soc_b = data['End_SOC']
battery_series = data['battery_size']
energy_series = data['energy']
#plug_time = data['total_time']
#charge_time = data['charge_time']


start_soc = series_to_list_of_percents(soc_a)
end_soc = series_to_list_of_percents(soc_b)
battery = series_to_list_of_nums(battery_series)
energy = series_to_list_of_nums(energy_series)  


for i in range(len(start_soc)):
    if end_soc[i] < start_soc[i]:
        soc_e = energy[i]/battery[i]
        if (soc_e + start_soc[i]) <= 1:
            end_soc[i] = (soc_e + start_soc[i])
        else:
            end_soc[i] = soc_e
    if end_soc[i] < start_soc[i]:
        end_soc[i] = 1

# change in SOC
change_soc = []
for i in range(len(start_soc)):
    change_soc.append(end_soc[i] - start_soc[i])

data['Start_SOC'] = start_soc
data['End_SOC'] = end_soc
data['Change_SOC'] = change_soc


#### Save Tidy Data ###########################################################
data.to_csv('data/dcfc_tidy.csv', sep=',', encoding='utf-8')

dcfc_ami.to_csv('data/dcfc_ami_tidy.csv', sep=',', encoding='utf-8')

# VARIABLES NEEDED

# END SOC CLEANER
# CHANGE IN SOC

#battery_sizes = []
#zero_division_ct = 0
#for i in range(list_len):
#    if isinstance(start_soc[i], str) and isinstance(end_soc[i], str):
#        e = float(energy[i])
#        start = float(start_soc[i][:-1])
#        end = float(end_soc[i][:-1])
#
#        # print(e ,start, end)
#        try:
#            # battery_sizes.append(math.fabs(e / (end - start)))
#            battery_sizes.append(e / (end - start))
#        except ZeroDivisionError:
#            zero_division_ct = zero_division_ct + 1
#






# facit by starting SOC



# variables we care about: 

### DATETIME ###
# Start Date
# End Date
# Charging Time (hh:mm:ss)
# Charge End (formula: "Start Date" + "Charge Duration")

### CHARGING ###
# Energy (kWh)
# Average kW (formula: Energy (kWh) / Charging Time (hh:mm:ss))
# Start SOC
# End SOC
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
# EV Make                           Not yet, kinda hard...
# EV Model                          Not yet, kinda hard...
# EV Year                           Done

### Variables We Can Create ### 
# vehicle battery size FORMULA: 
    # max(Energy)
    # Energy / (SOC End - SOC Start)
    # Energy / (100 - SOC Start) if Ended By == Charger Stopped & Charge Duration < Total Duration
