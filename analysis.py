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
import statsmodels.stats.api as sms
from datetime import datetime
import seaborn as sns
import scipy, scipy.stats
sns.set(font_scale=1.5)
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

# counts of dummy variables
dcfc['year_2019'].value_counts()
dcfc['year_2018'].value_counts()
dcfc['year_2017'].value_counts()
dcfc['year_2016'].value_counts()
dcfc['year_2015'].value_counts()
dcfc['year_2014'].value_counts()

(dcfc['year_2019'].value_counts()+dcfc['year_2018'].value_counts()+dcfc['year_2017'].value_counts()
+dcfc['year_2016'].value_counts()+dcfc['year_2015'].value_counts()+dcfc['year_2014'].value_counts()
-len(dcfc))
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


##### AMI DATA ################################################################
dt = ami['INTERVAL_TIME']
date = []
for i in range(len(dt)):
    ddd = datetime.strptime(dt[i][:-9], "%Y-%m-%d").date()
    date.append(ddd)

ami['date'] = date
# filter only top on each date
ami['dt_month']=ami['date'].apply(lambda x : x.replace(day=1))
ami = ami.groupby('dt_month').head(10)
#ami = ami.groupby('date').head(1)

kw = ami['demand']
temp = ami['Temp']
slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(kw,temp)
line = [ slope*xi + intercept for xi in kw]

fig6 = plt.figure()
plt.plot(kw,line,'r-',linewidth=5,label='linear regression')
plt.scatter(kw,temp,c=ami['Year'], alpha = .7)
plt.title('AMI Maximum Demand by Temperature', fontsize = 20)
plt.xlabel('Rate of Charge (kW)', fontsize=14)
plt.ylabel('Temperature (F)', fontsize=16)
plt.colorbar(label='Year')
plt.legend()
plt.show()
fig6.savefig('stats/ami_dcfc_peak_demand_by_day', bbox_inches='tight')


g = sns.FacetGrid(ami, col="Year")
g.map(plt.scatter, "demand", "Temp", alpha=.7)
g.add_legend()

##### DCFC Session Data #######################################################
dcfc1 = dcfc[dcfc.Start_SOC < 40]
dcfc1 = dcfc1[dcfc1.charge_time > '00:20:00']


# simple regression
avg_kw_rate = dcfc1['avg_kw']
temp = dcfc1['Temp']
slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(temp,avg_kw_rate)
line = [ slope*xi + intercept for xi in temp]
slope = round(slope,3)
r_value = round(r_value,3)

# DCFC effect of temperature on average charging rate 
fig7 = plt.figure()
plt.plot(temp,line,'r-',linewidth=5,label='Linear Regression \n slope: {} \n r-value{}'.format(slope,r_value))
plt.scatter(temp,avg_kw_rate,c = dcfc1['model_year'], alpha = .7)
plt.title('Effect of Temperature on Fast Charging', fontsize = 20)
plt.xlabel('Temperature (F)', fontsize=14)
plt.ylabel('Rate of Charge (kW)', fontsize=16)
plt.colorbar(label='model year')
plt.legend()
plt.show()
fig7.savefig('stats/dcfc_linear_regression', bbox_inches='tight')

# print linear regression details
print("slope", slope)
print("r_value", r_value)
print("p_value", p_value)
print("std_err", std_err)


# facit 2 - effect of temperature by model year

# filtering
dcfc2 = dcfc[dcfc.Start_SOC < 60]
# create splits to fit as two sets
a = dcfc2[dcfc2.model_year<2016]
b = dcfc2[dcfc2.model_year>2015]


# 2013-2015
fig8 = plt.figure()
g = sns.lmplot(x="avg_kw", y="Temp", col="model_year", data=a,
           aspect=1, ci=None, line_kws={'color':'red'})
g.savefig('stats/model_year_facit_a', bbox_inches='tight')

# 2016-2019
plt.figure()
g = sns.lmplot(x="avg_kw", y="Temp", col="model_year", data=b,
           aspect=1, ci=None, line_kws={'color':'red'})
g.savefig('stats/model_year_facit_b', bbox_inches='tight')

