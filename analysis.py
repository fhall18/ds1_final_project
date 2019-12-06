#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 09:43:50 2019

@author: johnhardy
"""

"""
Created on Tue Dec  3 19:18:26 2019
UNCANNYHORSE DS1 FINAL
@author: fhall, spell, jhardy
"""

#### IMPORTS ##################################################################
from matplotlib import pyplot as plt
import pandas as pd
import scipy, scipy.stats
import numpy as np
import statsmodels as sm
import statsmodels.formula.api as smf

#### FUNCTIONS ################################################################



#### LOAD DATA ################################################################

dcfc = pd.read_csv('dcfc_tidy.csv')

# making


#### ANALYSIS #################################################################

#### EDA

dcfc.info()

# making dummy variables factors (rather than numeric)
dcfc['Port Number'] = dcfc['Port Number'].astype('category', copy=False)
dcfc['year_2019'] = dcfc['year_2019'].astype('category', copy=False)
dcfc['year_2018'] = dcfc['year_2018'].astype('category', copy=False)
dcfc['year_2017'] = dcfc['year_2017'].astype('category', copy=False)
dcfc['year_2016'] = dcfc['year_2016'].astype('category', copy=False)
dcfc['year_2015'] = dcfc['year_2015'].astype('category', copy=False)
dcfc['year_2014'] = dcfc['year_2014'].astype('category', copy=False)

# summary statistics on all variables
sum_data = dcfc.describe(include='all')
print(sum_data)

# sum of null values
dcfc.isnull().sum()


#### simple regression
avg_kw_rate = dcfc['avg_kw']
temp = dcfc['Temp']
slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(avg_kw_rate,temp)
line = [ slope*xi + intercept for xi in avg_kw_rate]

#### multiple linear regression
# checking linearity between response and predictors
fig1 = plt.figure()
plt.scatter(dcfc['avg_kw'], dcfc['Temp'])
plt.xlabel('Average kW')
plt.ylabel('Temperature (in Fahrenheit)')
plt.show()
fig1.savefig('TempAvgkW_Scatter', bbox_inches='tight')

fig2 = plt.figure()
plt.scatter(dcfc['avg_kw'], dcfc['Start_SOC'])
plt.xlabel('Average kW')
plt.ylabel('Start State of Charge (SOC)')
plt.show()
fig2.savefig('SOCAvgkW_Scatter', bbox_inches='tight')

fig3 = plt.figure()
plt.scatter(dcfc['avg_kw'], dcfc['battery_size'])
plt.xlabel('Average kW')
plt.ylabel('Battery Size')
plt.show()
fig3.savefig('BatteryAvgkW_Scatter', bbox_inches='tight')

# checking for collinearity
corr_data = dcfc[['Temp', 'Start_SOC', 'battery_size']]
corr = corr_data.corr()

# regression with dummy variables
model = smf.ols('avg_kw ~ Temp + Start_SOC + battery_size + year_2019 + year_2018 + year_2017 + year_2016 + year_2015 + year_2014', data=dcfc).fit()
print(model.summary())

# regression without dummy variables
model = smf.ols('avg_kw ~ Temp + Start_SOC + battery_size', data=dcfc).fit()
print(model.summary())

####################################

plt.scatter(dcfc['energy'],dcfc['Temp'])
plt.plot(avg_kw_rate,line,'r-',linewidth=5,label='linear regression')
plt.scatter(dcfc['avg_kw'],dcfc['Temp'],c = dcfc['Start_SOC'], alpha = .7)
plt.title('Charging Rate by Temperature', fontsize = 20)
plt.xlabel('Rate of Charge (kW)', fontsize=14)
plt.ylabel('Temperature (F)', fontsize=16)
plt.colorbar()
plt.legend()
plt.show()




#### histogram of change in soc before, change in soc after
plt.figure()
plt.hist(dcfc['Start_SOC'], bins='auto', density=True,
color='#424FA4')
plt.hist(dcfc['End_SOC'], bins='auto', density=True,
color='#4FA442', alpha=0.5)
plt.xlabel('Change in State of Charge (SOC)')
plt.ylabel('P(x)')
plt.legend(['Change in SOC Before', 'Change in SOC After'], fontsize=14)
plt.show()

# change in SOC
dcfc['SOC_change'] = dcfc['End_SOC'] - dcfc['Start_SOC']
plt.figure()
plt.hist(dcfc['SOC_change'])
plt.ylabel('Frequency')
plt.xlabel('Change in SOC (percentage point)')
plt.show()



#### change in soc by time duration (temperature colored)
cm = plt.cm.get_cmap('viridis')
plt.figure()
sc = plt.scatter(dcfc['total_time'], dcfc['SOC_change'], 
c=dcfc['Temp'], vmin=-20, vmax=100, cmap=cm)
plt.colorbar(sc)
plt.show()

### How battery size changes how temperature affects avg_kw
plt.figure()
ax = plt.subplots()
cm = plt.cm.get_cmap('viridis')
sc1 = plt.scatter(dcfc['Temp'], dcfc['avg_kw'],
c=dcfc['battery_size'], vmin=0, vmax=50, cmap=cm)
cbar = plt.colorbar(sc1)
cbar.ax.get_yaxis().labelpad = 15
cbar.ax.set_ylabel('Battery Size kWh',rotation=270)
plt.xlabel('Temperature (in Fahrenheit)')
plt.ylabel('Average KW')
plt.show()

model = smf.ols('avg_kw ~ battery_size + Temp + battery_size*Temp', data=dcfc).fit()
print(model.summary())


### How model year changes how temperature affects avg_kw
plt.figure()
ax = plt.subplots()
cm = plt.cm.get_cmap('viridis')
sc2 = plt.scatter(dcfc['Temp'], dcfc['avg_kw'],
c=dcfc['year_2019'], vmin=0, vmax=1, cmap=cm)
cbar = plt.colorbar(sc2)
cbar.ax.get_yaxis().labelpad = 15
cbar.ax.set_ylabel('2019 (1 = yes and 0 = no)', rotation=270)
plt.xlabel('Temperature (in Fahrenheit)')
plt.ylabel('Average KW')
plt.show()

model = smf.ols('avg_kw ~ year_2019 + year_2018 + year_2017 + year_2016 + year_2015 + year_2014 + Temp + year_2019*Temp + year_2018*Temp + year_2017*Temp + year_2016*Temp + year_2015*Temp + year_2014*Temp', data=dcfc).fit()
print(model.summary())










































































