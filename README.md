# ds1_final_project

## The Effects of Temperature on Electric Vehicle Charging Across Time and Vehicle Model


## * Included:
#### -README.md
#### -clean_data.py
#### -analysis.py
#### -data (directory)
#### -stats (directory)
#### -minutes (directory)
#### -ideas.pdf
#### -FP-peer-evaluation-01_USERNAME.docx
#### -FP-peer-evaluation-01_USERNAME.docx
#### -FP-self-evaluation_USERNAME.docx
#### -FP-team-process-evaluation_USERNAME.docx
#### -reflection_UNCANNYHORSE.pdf
#### -report_UNCANNYHORSE.PDF
#### -slides_UNCANNYHORSE.pptx
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
##### This dataset was our main store of information. This dataset provided most of the information we needed, attributes like time, charge time, total charge time, battery state of charge, etc. 
###### -Features: 
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
##### AMI stands for Advanced Metering Infrastructure. This dataset gave us fifteen minute interval energy data which recorded the energy use (kW-15) of the DCFC located on 75 S. Winooski Ave.
###### -features:
######   INTERVAL_TIME
######   LOCID
######   LP_VALUE
#### 3. weather_temp_2013-2019.csv
##### This dataset was used to gather our temperature data. We merged this dataset with btv_total_charging_sessions.csv and dcfc_ami.csv based on time. 
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
##### -This dataset was used as reference for us when looking at electric vehicle models.
######   -features:
######   Make_Model
######   EV_type
######   Year
######   \# in VT
######   Max Lvl 2 Charge (kW)
######   Battery (kWh)
######   DC compatable
  ##
### * stats
#### Stats is a directory containing figures from our statistical analyses.
  ##
### * ideas.pdf
#### File describing our research questions, possible statistical analyses, and datasets. 
### * Minutes
#### A directory that holds all of the documents that describe our various meetings.
### * report_UNCANNYHORSE
#### Our Technical report discussing our research processes. 
### * Slides_UncannyHorse.pptx
#### Our powerpoint to summarize and present our results from our project.
### * Reflection_UncannyHorse.pdf
#### Our group reflection our our group dynamics, gantt chart, and research processes. 
### * FP-peer-evaluation-01_USERNAME.docx
#### peer evaluation form 1
### * FP-peer-evaluation-02_USERNAME.docx
#### peer evaluation form 2
### * FP-self-evaluation_USERNAME.docx
#### self evaluation form
### * FP-team-process-evaluation_USERNAME.docx
#### team process evaluation form
