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

#### FUNCTIONS ################################################################



#### LOAD DATA ################################################################

dcfc = pd.read_csv('data/dcfc_tidy.csv')



#### ANALYSIS #################################################################


# simple regression
avg_kw_rate = dcfc['avg_kw']
temp = dcfc['Temp']
slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(avg_kw_rate,temp)
line = [ slope*xi + intercept for xi in avg_kw_rate]

plt.scatter(dcfc['Energy (kWh)'],dcfc['Temp'])
plt.plot(avg_kw_rate,line,'r-',linewidth=5,label='linear regression')
plt.scatter(dcfc['avg_kw'],dcfc['Temp'],c = dcfc['Start SOC'], alpha = .7)
plt.title('Charging Rate by Temperature', fontsize = 20)
plt.xlabel('Rate of Charge (kW)', fontsize=14)
plt.ylabel('Temperature (F)', fontsize=16)
plt.colorbar()
plt.legend()
plt.show()
