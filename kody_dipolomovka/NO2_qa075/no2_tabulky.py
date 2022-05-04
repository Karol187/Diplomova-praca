#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 09:25:33 2021

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

mapb=Basemap(projection='lcc',lat_1=46.24470138549805,lat_2=46.24470138549805,lat_0=48.66,lon_0=19.7,width=432780,height=216351,resolution='h')



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
    
    
    
udaje = {'name':['Bratislava, Mamateyova','Bratislava, Trnavské Mýto','Stará Lesná, AÚ SAV, EMEP','Topoľníky, Aszód, EMEP','Ružomberok, Riadok','Žilina, Obežná','Jelšava, Jesenského','Humenné, Nám. slobody','Martin, Jesenského','Trnava, Kollárova','Trenčín, Hasičská','Bratislava, Jeséniova','Prievidza, Malonecpalská','Nitra, Janíkovce','Banská Bystrica,Štefánik. náb.','Banská Bystrica, Zelená','Malacky, Mierové námestie','Prešov, arm. gen. L. Svobodu','Košice, Štefánikova','Nitra, Štúrova','Kojšovská hoľa','Gánovce, Meteo. st.','Starina, Vodná nádrž, EMEP','Chopok, EMEP'], 'no2': [21,37,5,8,18,21,9,9,24,34,27,10,16,10,29,9,22,39,28,31,3,8,3,2], 'lat_x': [48.124692,48.158359,49.151384,47.959423,49.079025,49.211470,48.631194,48.930897,49.059630,48.371385,48.896419,48.167952,48.782641,48.283059,48.735110,48.733222,48.436843,48.992475,48.726310,48.309436,48.782875,49.034601,49.042734,48.943620],'lon_x': [17.125400,17.128891,20.289529,17.860238,19.302536,18.771289,20.240498,21.913688,18.921378,17.584926,18.041240,17.106209,18.628071,18.140716,19.154985,19.115278,17.019052,21.266767,21.258902,18.076870,20.987112,20.322844,22.260012,19.589236]}
tabulka = pd.DataFrame(udaje)
tabulka_zoznam_2019=[]
tabulka_zoznam_2020=[]
for i, row in tabulka.iterrows():   
    hodnoty_2019=[]
    for pole in (tropospheric_no2_polia_2019):
        ix, iy=getclosest_ij(lat_2019,lon_2019,row['lat_x'],row['lon_x'])
        hodnoty_2019.append(pole[ix, iy]) 
    hodnoty_2020=[]
    for pole in (tropospheric_no2_polia_2020):
        ix, iy=getclosest_ij(lat_2020,lon_2020,row['lat_x'],row['lon_x'])
        hodnoty_2020.append(pole[ix, iy]) 
     
    data_2019 = {'Dátum': datumy_2019,'Hodnoty '+str(row['name']): hodnoty_2019}
    df_2019 = pd.DataFrame(data_2019)
    tabulka_zoznam_2019.append(df_2019)
                               
    data_2020 = {'Dátum': datumy_2020,'Hodnoty '+str(row['name']): hodnoty_2020}
    df_2020 = pd.DataFrame(data_2020)
    tabulka_zoznam_2020.append(df_2020)
'''
Tabulky s nazvom stanice a hodnotou z druzice za roky 2019 a 2020
'''
# for i, row in tabulka.iterrows():
#     tabulka_zoznam_2019[i].to_csv(str(row['name'])+' no2_druzica_rok_2019.csv')
#     tabulka_zoznam_2020[i].to_csv(str(row['name'])+' no2_druzica_rok_2020.csv')
