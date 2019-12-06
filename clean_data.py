#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 22:10:38 2019

@author: fhall, spell, jhardy
"""
#### IMPORTS ##################################################################
from datetime import datetime
import pandas as pd

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
messy_charging['Start Date'] = pd.to_datetime(messy_charging['Start Date'],format='%Y-%m-%d %H:%M:%S')
messy_charging['End Date']=pd.to_datetime(messy_charging['End Date'],format='%Y-%m-%d %H:%M:%S')

# index datetimes
start_date = messy_charging['Start Date']
start_date = pd.Index(start_date)

# localize
start_date = start_date.tz_localize(None)
messy_charging['Start Date'] = start_date

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
port_type = data['Port_Type']

for i in range(list_len):
    t = datetime.strptime(time[i], "%H:%M:%S").time()
    t = t.hour + t.minute/60
    if(t != 0):
        avg_kw.append(energy[i]/t)
    else:
        avg_kw.append(None)

kw = pd.DataFrame()
kw['energy'] = energy
kw['time'] = time
kw['kw'] = avg_kw
kw['port_type'] = port_type

#### MERGE 2 ##################################################################
data['avg_kw'] = avg_kw
data = data.merge(driver_stats, on='User_ID')


#### DCFC DATA ################################################################

# filters
data = data[data.Port_Type == 'DC Fast']
data = data[data.avg_kw < 30] # strange datapoint higher than 30 kW...
data = data[data.Start_SOC.notnull()]
data = data[data.charge_time > '00:05:00']


# change SOC to numbers
soc_a = data['Start_SOC']
soc_b = data['End_SOC']
battery_series = data['battery_size']
energy_series = data['energy']

# convert Start SOC to int
start_soc = []
for i in soc_a:
    num = i[:-1]
    num = int(num)
    start_soc.append(num)

# convert End SOC to int
end_soc = series_to_list_of_percents(soc_b)
end_soc = []
for i in soc_b:
    num = i[:-1]
    num = int(num)
    end_soc.append(num)

# battery and energy as lists
battery = series_to_list_of_nums(battery_series)
energy = series_to_list_of_nums(energy_series)  


# fix End_SOC
for i in range(len(start_soc)):
    if end_soc[i] < start_soc[i]:
        soc_e = energy[i]/battery[i]*100
        if (soc_e + start_soc[i]) <= 100:
            end_soc[i] = (soc_e + start_soc[i])
        else:
            end_soc[i] = soc_e
    if end_soc[i] < start_soc[i]:
        end_soc[i] = 100

# change in SOC
change_soc = []
for i in range(len(start_soc)):
    change_soc.append(end_soc[i] - start_soc[i])


# append SOC variables
data['Start_SOC'] = start_soc
data['End_SOC'] = end_soc
data['Change_SOC'] = change_soc

# filter soc again
data = data[data.Start_SOC > 0]
data = data[data.End_SOC > 0]

# creating dummy variables for model year
data['year_2019'] = (data['model_year']==2019).astype(int)
data['year_2018'] = (data['model_year']==2018).astype(int)
data['year_2017'] = (data['model_year']==2017).astype(int)
data['year_2016'] = (data['model_year']==2016).astype(int)
data['year_2015'] = (data['model_year']==2015).astype(int)
data['year_2014'] = (data['model_year']==2014).astype(int)

print(data.shape)

#### MAPPING DATA #############################################################
mapping = charging[['Start Date Truncated','total_time','charge_time','EVSE ID',
                    'Latitude','Longitude',]]

#### Save Tidy Data ###########################################################
data.to_csv('data/dcfc_tidy.csv', sep=',', encoding='utf-8')
dcfc_ami.to_csv('data/dcfc_ami_tidy.csv', sep=',', encoding='utf-8')
mapping.to_csv('data/mapping_tidy.csv', sep=',', encoding='utf-8')
