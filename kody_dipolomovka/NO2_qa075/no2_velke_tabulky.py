#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 16:58:14 2021

@author: OMKO459
"""

import netCDF4
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from datetime import datetime
from datetime import timedelta

plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = 20,8





def getclosest_ij(nlats,nlons,latpt,lonpt):
    # find squared distance of every point on grid
    dist_sq = (nlats-latpt)**2 + (nlons-lonpt)**2  
    # 1D index of minimum dist_sq element
    minindex_flattened = dist_sq.argmin()    
    # Get 2D index for latvals and lonvals arrays from 1D index
    return np.unravel_index(minindex_flattened, nlats.shape)

dataset_2019=netCDF4.Dataset('/data/oko/dusan/sentinel5P/no2/2019/post_data/no2_trop_grid.nc')
dataset_2020=netCDF4.Dataset('/data/oko/dusan/sentinel5P/no2/2020/post_data/no2_trop_grid.nc')
pocet_snimkov_2019= len(dataset_2019.variables['tropospheric_no2'][:,0,0])
pocet_snimkov_2020= len(dataset_2020.variables['tropospheric_no2'][:,0,0])
lon_2019= dataset_2019.variables['lon'][:,:]
lat_2019= dataset_2019.variables['lat'][:,:]
lon_2020= dataset_2020.variables['lon'][:,:]
lat_2020= dataset_2020.variables['lat'][:,:]
tropospheric_no2_2019= dataset_2019.variables['tropospheric_no2'][:,:,:]
tropospheric_no2_2020= dataset_2020.variables['tropospheric_no2'][:,:,:]

tropospheric_no2_polia_2019=[]
for k in range (pocet_snimkov_2019):
     tropospheric_no2_polia_2019.append(tropospheric_no2_2019[k,:,:])

tropospheric_no2_polia_2020=[]
for k in range (pocet_snimkov_2020):
     tropospheric_no2_polia_2020.append(tropospheric_no2_2020[k,:,:])

datumy_2019=[]
for s in (dataset_2019.variables['times'][:]):
    dates = datetime(2019, 1, 1,11,15,46,949999)+ timedelta(seconds=s)
    datumy_2019.append(dates)

datumy_2020=[]
for s in (dataset_2020.variables['times'][:]):
    dates = datetime(2020, 1, 1,10,32,12,742616)+ timedelta(seconds=s)
    datumy_2020.append(dates)


 
tabulka=pd.read_csv('/data/karol/diplomovka/stanice_no2_2019_prizemne_koncentracie.csv')  
datalist_2019=[]
datalist_2020=[]
for i, row in tabulka.iterrows():   
    hodnoty_2019=[]
    for pole in (tropospheric_no2_polia_2019):
        ix, iy=getclosest_ij(lat_2019,lon_2019,row['lat_x'],row['lon_x'])
        hodnoty_2019.append(pole[ix, iy]) 
    hodnoty_2020=[]
    for pole in (tropospheric_no2_polia_2020):
        ix, iy=getclosest_ij(lat_2020,lon_2020,row['lat_x'],row['lon_x'])
        hodnoty_2020.append(pole[ix, iy]) 
     
    data_2019 = {'Hodnoty '+str(row['name']): hodnoty_2019}
    df_2019 = pd.DataFrame(data_2019) 
    datalist_2019.append(df_2019)
    data_2020 = {'Hodnoty '+str(row['name']): hodnoty_2020}
    df_2020 = pd.DataFrame(data_2020) 
    datalist_2020.append(df_2020)

dates_2019={'Datumy': datumy_2019}
df_dates_2019=pd.DataFrame(dates_2019)
dataframe_stanice_2019=pd.concat(datalist_2019,axis=1)
result_2019 = pd.concat([df_dates_2019,dataframe_stanice_2019], axis=1)


dates_2020={'Datumy': datumy_2020}
df_dates_2020=pd.DataFrame(dates_2020)
dataframe_stanice_2020=pd.concat(datalist_2020,axis=1)
result_2020 = pd.concat([df_dates_2020,dataframe_stanice_2020], axis=1)

# result_2019.to_csv('no2_velka_tabulka_2019.csv')
# result_2020.to_csv('no2_velka_tabulka_2020.csv')





































