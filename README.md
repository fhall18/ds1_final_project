# ds1_final_project

## The Effects of Temperature on Electric Vehicle Charging Across Time and Vehicle Model


## * Included:
#### -README.md
#### -clean_data.py
#### -analysis.py
#### -data
##
### * clean_data.py
#### 1. This file should be run first.
#### 2. This file takes in all data files, cleans them, and calculates necessary variables and equations for analysis.
##### -btv_total_charging_sessions.csv
##### -dcfc_ami.csv
##### -weather_temp_2013-2019.csv
#####  -ev_type.csv
#### 3. Outputs:
#####  -dcfc_tidy.csv
#####  -dcfc_ami_tidy.csv
 ##
### * analysis.py
#### 1. This file includes all calculations necessary for the EDA and analysis of our datasets. 
#### 2. Outputs:
#####  -summary statistics from dcfc tidy data file
#####  -simple regression on dcfc tidy data file
#####  -multiple linear regression on dcfc tidy data file
#####   +Average kW vs. Temperature
#####   +Average kW vs. Initial State of Charge
#####   +Average kW vs. Battery Size
#####  -Check Collinearity between Temperature, Initial State of Charge, and Batter Size
#####  -Histogram of change in initial and end state of charge
#####  -How Battery Size Accounts for Temperature's effects on average kW
#####  -How Model Year Might Change How Temperature Affects Average kW
#####  -Rate of charge vs. Temperature based on 15 minute interval data (AMI Data)
#####  -Linear Regression on Effect of Temperature on Average Charging Rate
#####  -Effect of Temperature by Model Year (2013-2015, 2016-2019)
 ##
### * Data:
#### 1. btv_total_charging_sessions.csv
##### -Features: 
###### Start Date
######   Start Time Zone
######  End Date
######   End Time Zone
######   total_time
######   charge_time
######   energy
######   Port_Type
######   Port Number
######   Plug Type
######   EVSE ID
######   Address 1
 ######  Latitude
 ######  Longitude
 ######  Fee
 ######  Ended_By
 ######  Plug In Event Id
 ######  Driver Postal Code
 ######  User_ID
######   Start_SOC
######   End_SOC
######   County
 ######  System S/N
 ######  Model Number
 ######  Start Date Truncated
 ######  End Date Truncated
 ######  Year
 ######  Temp
 ######  avg_kw
 ######  battery_size
 ######  model_year
 ######  Change_SOC
 ######  year_2019
######   year_2018
######   year_2017
######   year_2016
######   year_2015
######   year_2014
#### 2. dcfc_ami.csv
###### -features:
######   INTERVAL_TIME
######   LOCID
######   LP_VALUE
#### 3. weather_temp_2013-2019.csv
###### features:
 ######  Year
######   Month
######   Day
######   HR01
######   HR02
######   HR03
######   HR04
######   HR05
######   HR06
######   HR07
######   HR08
######   HR09
######   HR10
######   HR11
######   HR12
######   HR13
######   HR14
 ######  HR15
 ######  HR16
######   HR17
######   HR18
######   HR19
######   HR20
######   HR21
######   HR22
######   HR23
######   HR24
#### 4. ev_type.csv
######   -features:
######   Make_Model
######   EV_type
######   Year
######   \# in VT
######   Max Lvl 2 Charge (kW)
######   Battery (kWh)
######   DC compatable
 
