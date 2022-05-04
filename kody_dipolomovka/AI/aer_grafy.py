#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 07:31:49 2022

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

dataset=netCDF4.Dataset('/data/oko/dusan/sentinel5P/AER/2019/post_data/aer_354_38.nc')
pocet_snimkov= len(dataset.variables['aer_354_38'][:,0,0])
lon= dataset.variables['lon'][:,:]
lat= dataset.variables['lat'][:,:]
aer= dataset.variables['aer_354_38'][:,:,:]

aer_polia=[]
for k in range (pocet_snimkov):
     aer_polia.append(aer[k,:,:])

datumy=[]
for s in (dataset.variables['times'][:]):
    dates = datetime(2019, 1, 1,11,15,55,387549)+ timedelta(seconds=s)
    datumy.append(dates)
   
udaje = {'name':['Bratislava, Mamateyova','Bratislava, Trnavské Mýto','Stará Lesná, AÚ SAV, EMEP','Topoľníky, Aszód, EMEP','Ružomberok, Riadok','Žilina, Obežná','Jelšava, Jesenského','Humenné, Nám. slobody','Martin, Jesenského','Trnava, Kollárova','Trenčín, Hasičská','Bratislava, Jeséniova','Prievidza, Malonecpalská','Nitra, Janíkovce','Banská Bystrica,Štefánik. náb.','Banská Bystrica, Zelená','Malacky, Mierové námestie','Prešov, arm. gen. L. Svobodu','Košice, Štefánikova','Nitra, Štúrova','Kojšovská hoľa','Gánovce, Meteo. st.','Starina, Vodná nádrž, EMEP','Chopok, EMEP'], 'no2': [21,37,5,8,18,21,9,9,24,34,27,10,16,10,29,9,22,39,28,31,3,8,3,2], 'lat_x': [48.124692,48.158359,49.151384,47.959423,49.079025,49.211470,48.631194,48.930897,49.059630,48.371385,48.896419,48.167952,48.782641,48.283059,48.735110,48.733222,48.436843,48.992475,48.726310,48.309436,48.782875,49.034601,49.042734,48.943620],'lon_x': [17.125400,17.128891,20.289529,17.860238,19.302536,18.771289,20.240498,21.913688,18.921378,17.584926,18.041240,17.106209,18.628071,18.140716,19.154985,19.115278,17.019052,21.266767,21.258902,18.076870,20.987112,20.322844,22.260012,19.589236]}
tabulka = pd.DataFrame(udaje)

for i, row in tabulka.iterrows():   
    hodnoty=[]
    for pole in (aer_polia):
        ix, iy=getclosest_ij(lat,lon,row['lat_x'],row['lon_x'])
        hodnoty.append(pole[ix, iy]) 
    
    data = {'Dátum': datumy,'Hodnoty': hodnoty}
    df = pd.DataFrame(data)

    df.plot(kind = 'scatter',
            x = 'Dátum',
            y = 'Hodnoty',
            color = 'red')
    plt.title(str(row['name'])+' počas roka 2019')
    plt.xlabel('Dátum')
    plt.ylabel("AI počas roka 2019")
    plt.xticks(rotation='horizontal')
    plt.savefig(str(row['name'])+' počas roka 2019.png',bbox_inches='tight',dpi=600)
    plt.clf()
    #plt.show()

   