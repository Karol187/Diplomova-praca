#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 20:28:20 2022

@author: OMKO459
"""

#imported libraries
import numpy as np 
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import netCDF4
import pandas as pd
import matplotlib
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = 20,8

mapb=Basemap(projection='lcc',lat_1=46.24470138549805,lat_2=46.24470138549805,lat_0=48.66,lon_0=19.7,width=432780,height=216351,resolution='h')
#########################
#funkction which fidns ix and iy indexes of grid
def getclosest_ij(nlats,nlons,latpt,lonpt):
    # find squared distance of every point on grid
    dist_sq = (nlats-latpt)**2 + (nlons-lonpt)**2  
    # 1D index of minimum dist_sq element
    minindex_flattened = dist_sq.argmin()    
    # Get 2D index for latvals and lonvals arrays from 1D index
    return np.unravel_index(minindex_flattened, nlats.shape)
#########################
pole_priemerne_2019=np.load('/data/karol/diplomovka/priemer_no2_2019.npy')
pole_priemerne_2020=np.load('/data/karol/diplomovka/priemer_no2_2020.npy')
dataset_2019=netCDF4.Dataset('/data/oko/dusan/sentinel5P/no2/2019/post_data/no2_trop_grid.nc')
dataset_2020=netCDF4.Dataset('/data/oko/dusan/sentinel5P/no2/2020/post_data/no2_trop_grid.nc')
lon_2019= dataset_2019.variables['lon'][:,:]
lat_2019= dataset_2019.variables['lat'][:,:]
lon_2020= dataset_2020.variables['lon'][:,:]
lat_2020= dataset_2020.variables['lat'][:,:]



tabulka_2019=pd.read_csv('/data/karol/diplomovka/stanice_no2_2019_prizemne_koncentracie.csv')
tabulka_2020=pd.read_csv('/data/karol/diplomovka/stanice_no2_2020_prizemne_koncentracie.csv')

################################################################################


import numpy as np
x=[] #hodnoty v gridovom bode 
for i,row in tabulka_2019.iterrows():
    lat_x=row['lat_x']
    lon_x=row['lon_x']
    ix, iy = getclosest_ij(lat_2019,lon_2019,row['lat_x'],row['lon_x'])
    x.append(pole_priemerne_2019[ix,iy])
tabulka_2019['Druzica']=x
tabulka_2019.to_csv('tabulka_stanice_druzica_2019.csv')

import numpy as np
x=[] #hodnoty v gridovom bode 
for i,row in tabulka_2020.iterrows():
    lat_x=row['lat_x']
    lon_x=row['lon_x']
    ix, iy = getclosest_ij(lat_2019,lon_2019,row['lat_x'],row['lon_x'])
    x.append(pole_priemerne_2020[ix,iy])
tabulka_2020['Druzica']=x
tabulka_2020.to_csv('tabulka_stanice_druzica_2020.csv')

