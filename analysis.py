#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
from datetime import datetime
import seaborn as sns
import scipy, scipy.stats

#### FUNCTIONS ################################################################



#### LOAD DATA ################################################################

dcfc = pd.read_csv('data/dcfc_tidy.csv')
ami = pd.read_csv('data/dcfc_ami_tidy.csv')


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
fig1.savefig('stats/TempAvgkW_Scatter', bbox_inches='tight')

fig2 = plt.figure()
plt.scatter(dcfc['avg_kw'], dcfc['Start_SOC'])
plt.xlabel('Average kW')
plt.ylabel('Start State of Charge (SOC)')
plt.show()
fig2.savefig('stats/SOCAvgkW_Scatter', bbox_inches='tight')

fig3 = plt.figure()
plt.scatter(dcfc['avg_kw'], dcfc['battery_size'])
plt.xlabel('Average kW')
plt.ylabel('Battery Size')
plt.show()
fig3.savefig('stats/BatteryAvgkW_Scatter', bbox_inches='tight')

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

#### histogram of change in soc before, change in soc after
fig4 = plt.figure()
plt.hist(dcfc['Start_SOC'], bins='auto', density=True,
color='#424FA4')
plt.hist(dcfc['End_SOC'], bins='auto', density=True,
color='#4FA442', alpha=0.5)
plt.xlabel('State of Charge (SOC)')
plt.ylabel('P(x)')
plt.legend(['Start SOC', 'End SOC'], fontsize=14)
plt.show()
fig4.savefig('stats/ComparingSOCs', bbox_inches='tight')

# change in SOC
dcfc['SOC_change'] = dcfc['End_SOC'] - dcfc['Start_SOC']
fig5 = plt.figure()
plt.hist(dcfc['SOC_change'], bins=25)
plt.ylabel('Frequency')
plt.xlabel('Change in SOC (percentage point)')
plt.show()
fig5.savefig('stats/DistChangeSOC', bbox_inches='tight')


### How battery size changes how temperature affects avg_kw
model = smf.ols('avg_kw ~ battery_size + Temp + battery_size*Temp', data=dcfc).fit()
print(model.summary())


### How model year changes how temperature affects avg_kw
model = smf.ols('avg_kw ~ year_2019 + year_2018 + year_2017 + year_2016 + year_2015 + year_2014 + Temp + year_2019*Temp + year_2018*Temp + year_2017*Temp + year_2016*Temp + year_2015*Temp + year_2014*Temp', data=dcfc).fit()
print(model.summary())


####### FREDDDIE  HERE
# AMI
dt = ami['INTERVAL_TIME']
date = []
for i in range(len(dt)):
    ddd = datetime.strptime(dt[i][:-9], "%Y-%m-%d").date()
    date.append(ddd)

ami['date'] = date
# filter only top on each date
ami = ami.groupby('date').head(1)

kw = ami['demand']
temp = ami['Temp']
slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(kw,temp)
line = [ slope*xi + intercept for xi in kw]

#fig6 = plt.figure()
#plt.scatter(dcfc['energy'],dcfc['Temp'])
#plt.plot(kw,line,'r-',linewidth=5,label='linear regression')
#plt.scatter(ami['demand'],ami['Temp'],c=ami['Year'], alpha = .7)
#plt.title('Charging Rate by Temperature', fontsize = 20)
#plt.xlabel('Rate of Charge (kW)', fontsize=14)
#plt.ylabel('Temperature (F)', fontsize=16)
#plt.colorbar()
#plt.legend()
#plt.show()
#fig6.savefig('stats/ami_dcfc_peak_demand_by_day', bbox_inches='tight')

#g = sns.FacetGrid(ami, col="Year")
#g.map(plt.scatter, "demand", "Temp", alpha=.7)
#g.add_legend()

##### DCFC Session Data #####
dcfc = dcfc[dcfc.Start_SOC < 40]
#dcfc = dcfc[dcfc.energy > 5]
dcfc = dcfc[dcfc.charge_time > '00:20:00']

# simple regression
avg_kw_rate = dcfc['avg_kw']
temp = dcfc['Temp']
slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(avg_kw_rate,temp)
line = [ slope*xi + intercept for xi in avg_kw_rate]

#plt.scatter(dcfc['energy'],dcfc['Temp'])
fig7 = plt.figure()
plt.plot(avg_kw_rate,line,'r-',linewidth=5,label='linear regression')
plt.scatter(dcfc['avg_kw'],dcfc['Temp'],c = dcfc['model_year'], alpha = .7)
plt.title('Charging Rate by Temperature', fontsize = 20)
plt.xlabel('Rate of Charge (kW)', fontsize=14)
plt.ylabel('Temperature (F)', fontsize=16)
plt.colorbar()
plt.legend()
plt.show()
fig7.savefig('stats/dcfc_linear_regression', bbox_inches='tight')

# facit - split into two sets
a = dcfc[dcfc.model_year<2016]
b = dcfc[dcfc.model_year>2015]

fig8 = plt.figure()
g = sns.FacetGrid(a, col="model_year")
g.map(plt.scatter, "avg_kw", "Temp", alpha=.7)
g.add_legend()
fig8.savefig('stats/model_year_facit_a', bbox_inches='tight')

fig9 = plt.figure()
g = sns.FacetGrid(b, col="model_year")
g.map(plt.scatter, "avg_kw", "Temp", alpha=.7)
g.add_legend()
fig9.savefig('stats/model_year_facit_b', bbox_inches='tight')

