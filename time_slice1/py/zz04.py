# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 00:15:25 2020

@author: hunt"""

import pandas as pd
import datetime
import os

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm1
import xarray as xr
from datetime import timedelta

# Add the directory used to run the time clustering algorithm.
# path = 'C:/Users/julia/Documents/Julian/IIASA/Behnam/Time slices paper/time clustering/'

path = "C:/Users/zhangzixuan/OneDrive/Research/Message/zzx22yssp/time_slice1/py/"

os.chdir(path)

now = datetime.datetime.now()

# Algorithm time selection
# Select the op value according to the scenario you want to analyze from 1 to 3

# select the number os hourly time slices = 24, 12, 6, 4, 3, 2, 1
hourly_time_slices_in_a_day = 4

# default = 1. If 2, the algorithm will look for a representative week with 4 seasons, 2 days and 6 hours, i.e. 48 time slices.
daily_time_slices_in_a_week = 2

# True = time slices will be divided into months. False = time slices will be divided into seasons
monthly = False

# if monthly = True, select the number of monthly time slices = 12, 6, 4, 3, 2, 1
# 12 = JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SET, OCT, NOV, DEC
# 6  = JAN-FEB, MAR-APR, MAY-JUN, JUL-AUG, SET-OCT, NOV-DEC
# 4  = JAN-MAR, APR-JUN, JUL-SET, OCT-DEC
# 3  = JAN-APR, MAY-AUG, SET-DEC
# 2  = JAN-JUN, JUL-DEC
# 1  = JAN-DEC
monthly_time_slices_in_a_year = 12

# if monthly = False, select the number of seasons time slices = 4, 2, 1
# 4 = Winter, Spring, Summer, Autumn = 21/DEC-19/MAR, 20/MAR-19/JUN, 20/JUN-21/SEP, 22/SEP-20/DEC
# 2 = Winter-Spring, Summer, Autumn = 21/DEC-19/JUN, 20/JUN-20/DEC
# 1 = Winter-Autumn = 21/DEC-20/DEC
seasonal_time_slices_in_a_year = 4

# Weights selection
# Define the weights for each kind of energy source (sum must be equal to 1):
# If a country of region has small wind or hydropower potential, the weight of wind and hydropower should be reduced so that the time slice improves the representation of solar and demand, for example.
solar_weight = 0.35
wind_weight = 0.35
hydro_weight = 0.15
demand_weight = 0.15

# Start time selection
# If you want the timeslices to start at 00:00 GTM for al reagions gtm = True. For aleatory start time gtm = False
# Starting at 00:00 GTM is interesting if the model will consider the transmission between regions. Thus solar power during the day in Europa can supply the night electricity demand in China.
# Not starting at 00:00 GTM results in better overall results for each individual country or region.
gtm = False
if gtm == True:
    mid_night = 6 # 6 is the number of time slices in the day. By jumping 6 time slices, the algorithm only consider days starting from midnight GTM time.
else:
    mid_night = 1 # This alternative will look for the best day for each reagion starting from 00:00, 04:00, 08:00, 12:00, 16:00, 18:00, 20:00. However, each reagion might have a different day start time.

# Data selections:
# There are two sets of data ready to run the time clustering algorithms: 1) 11 regions (11_regions =True) 2) Individual Countries (11_regions =False).
r_or_c = False # True = 11 regions / False = individual countries
if r_or_c == True:
    input_data = pd.read_excel('11 regions.xlsx')

    # Select the number of the regions that needs to be analysed with the numbers below:
    # region => NAM = 0, LAC = 1, WEU = 2, EEU = 3, FSU = 4, AFR = 5, MEA = 6, SAS = 7, CPA = 8, PAS = 9, PAO = 10
    regions_or_countries = ['NAM','CPA']
    selected_regions_or_countries = [0,8]

else:
    input_data = pd.read_excel('../data/CHN_west.xlsx')
    #input_data = pd.read_excel('test_ordos.xlsx')
    # Select the number of the country that needs to be analysed with the numbers below:
    # country => AFG = 0; AGO = 1; ALB = 2; ARE = 3; ARG = 4; ARM = 5; AUS = 6; AUT = 7; AZE = 8; BDI = 9; BEL = 10; BEN = 11; BFA = 12; BGD = 13; BGR = 14; BHR = 15; BIH = 16; BLR = 17; BLZ = 18; BOL = 19; BRA = 20;
    #BRN = 21; BTN = 22; BWA = 23; CAF = 24; CAN = 25; CHE = 26; CHL = 27; CHN = 28; CIV = 29; CMR = 30; COD = 31; COG = 32; COL = 33; CPV = 34; CRI = 35; CUB = 36; CYP = 37; CZE = 38; DEU = 39; DJI = 40;
    #DNK = 41; DOM = 42; DZA = 43; ECU = 44; EGY = 45; ERI = 46; ESH = 47; ESP = 48; EST = 49; ETH = 50; FIN = 51; FJI = 52; FRA = 53; GAB = 54; GBR = 55; GEO = 56; GHA = 57; GIN = 58; GMB = 59; GNB = 60;
    #GNQ = 61; GRC = 62; GTM = 63; GUF = 64; GUY = 65; HND = 66; HRV = 67; HTI = 68; HUN = 69; IDN = 70; IND = 71; IRL = 72; IRN = 73; IRQ = 74; ISL = 75; ISR = 76; ITA = 77; JAM = 78; JOR = 79; JPN = 80;
    #KAZ = 81; KEN = 82; KGZ = 83; KHM = 84; KOR = 85; KOS = 86; KWT = 87; LAO = 88; LBN = 89; LBR = 90; LBY = 91; LKA = 92; LSO = 93; LTU = 94; LUX = 95; LVA = 96; MAR = 97; MDA = 98; MDG = 99; MEX = 100;
    #MKD = 101; MLI = 102; MLT = 103; MMR = 104; MNE = 105; MNG = 106; MOZ = 107; MRT = 108; MUS = 109; MWI = 110; MYS = 111; NAM = 112; NER = 113; NGA = 114; NIC = 115; NLD = 116; NOR = 117; NPL = 118; NZL = 119; OMN = 120;
    #PAK = 121; PAN = 122; PER = 123; PHL = 124; PNG = 125; POL = 126; PRK = 127; PRT = 128; PRY = 129; QAT = 130; ROU = 131; RUS = 132; RWA = 133; SAU = 134; SDN = 135; SEN = 136; SGP = 137; SLE = 138; SLV = 139; SOM = 140;
    #SRB = 141; SUR = 142; SVK = 143; SVN = 144; SWE = 145; SWZ = 146; SYR = 147; TCD = 148; TGO = 149; THA = 150; TJK = 151; TKM = 152; TLS = 153; TTO = 154; TUN = 155; TUR = 156; TWN = 157; TZA = 158; UGA = 159; UKR = 160;
    #URY = 161; USA = 162; UZB = 163; VEN = 164; VNM = 165; YEM = 166; ZAF = 167; ZMB = 168; ZWE = 169;
    regions_or_countries = ['CHN_west']
    selected_regions_or_countries = [0]

if daily_time_slices_in_a_week == 2:
    from zz05 import algorithm as t48
    # algorithm(data,name,value,solarweight,windweight,hydroweight,demandweight,mid_night,path)
    t48(input_data,regions_or_countries,selected_regions_or_countries,solar_weight,wind_weight,hydro_weight,demand_weight,mid_night,path)
    x = 0

else:
    print("check")