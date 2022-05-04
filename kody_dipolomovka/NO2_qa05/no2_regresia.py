#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 08:48:44 2021

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
pole_priemerne_2019=np.load('/data/karol/diplomovka_no2_qavalue_05/priemer_no2_2019.npy')
pole_priemerne_2020=np.load('/data/karol/diplomovka_no2_qavalue_05/priemer_no2_2020.npy')
dataset_2019=netCDF4.Dataset('/data/oko/dusan/sentinel5P/no2/2019qa05/post_data/tropospheric_no2.nc')
dataset_2020=netCDF4.Dataset('/data/oko/dusan/sentinel5P/no2/2020qa05/post_data/no2_trop_grid.nc')
lon_2019= dataset_2019.variables['lon'][:,:]
lat_2019= dataset_2019.variables['lat'][:,:]
lon_2020= dataset_2020.variables['lon'][:,:]
lat_2020= dataset_2020.variables['lat'][:,:]


#udaje_2019 = {'name':['Bratislava, Mamateyova','Bratislava, Trnavské Mýto','Stará Lesná, AÚ SAV, EMEP','Topoľníky, Aszód, EMEP','Ružomberok, Riadok','Žilina, Obežná','Jelšava, Jesenského','Humenné, Nám. slobody','Martin, Jesenského','Trnava, Kollárova','Trenčín, Hasičská','Bratislava, Jeséniova','Prievidza, Malonecpalská','Nitra, Janíkovce','Banská Bystrica,Štefánik. náb.','Banská Bystrica, Zelená','Malacky, Mierové námestie','Prešov, arm. gen. L. Svobodu','Košice, Štefánikova','Nitra, Štúrova','Kojšovská hoľa','Gánovce, Meteo. st.','Starina, Vodná nádrž, EMEP','Chopok, EMEP'], 'no2': [21,37,5,8,18,21,9,9,24,34,27,10,16,10,29,9,22,39,28,31,3,8,3,2], 'lat_x': [48.124692,48.158359,49.151384,47.959423,49.079025,49.211470,48.631194,48.930897,49.059630,48.371385,48.896419,48.167952,48.782641,48.283059,48.735110,48.733222,48.436843,48.992475,48.726310,48.309436,48.782875,49.034601,49.042734,48.943620],'lon_x': [17.125400,17.128891,20.289529,17.860238,19.302536,18.771289,20.240498,21.913688,18.921378,17.584926,18.041240,17.106209,18.628071,18.140716,19.154985,19.115278,17.019052,21.266767,21.258902,18.076870,20.987112,20.322844,22.260012,19.589236]}
#tabulka_2019 = pd.DataFrame(udaje_2019)

#udaje_2020 = {'name':['Bratislava, Mamateyova','Bratislava, Trnavské Mýto','Stará Lesná, AÚ SAV, EMEP','Topoľníky, Aszód, EMEP','Ružomberok, Riadok','Žilina, Obežná','Jelšava, Jesenského','Humenné, Nám. slobody','Martin, Jesenského','Trnava, Kollárova','Trenčín, Hasičská','Bratislava, Jeséniova','Prievidza, Malonecpalská','Nitra, Janíkovce','Banská Bystrica,Štefánik. náb.','Banská Bystrica, Zelená','Malacky, Mierové námestie','Prešov, arm. gen. L. Svobodu','Košice, Štefánikova','Nitra, Štúrova','Kojšovská hoľa','Gánovce, Meteo. st.','Starina, Vodná nádrž, EMEP','Chopok, EMEP'],'no2': [16,33,5,8,17,16,8,8,19,27,23,9,14,8,24,8,18,31,23,26,3,8,3,2], 'lat_x': [48.124692,48.158359,49.151384,47.959423,49.079025,49.211470,48.631194,48.930897,49.059630,48.371385,48.896419,48.167952,48.782641,48.283059,48.735110,48.733222,48.436843,48.992475,48.726310,48.309436,48.782875,49.034601,49.042734,48.943620],'lon_x': [17.125400,17.128891,20.289529,17.860238,19.302536,18.771289,20.240498,21.913688,18.921378,17.584926,18.041240,17.106209,18.628071,18.140716,19.154985,19.115278,17.019052,21.266767,21.258902,18.076870,20.987112,20.322844,22.260012,19.589236]}
#tabulka_2020 = pd.DataFrame(udaje_2020)
tabulka_2019=pd.read_csv('/data/karol/diplomovka/stanice_no2_2019_prizemne_koncentracie.csv')
tabulka_2020=pd.read_csv('/data/karol/diplomovka/stanice_no2_2020_prizemne_koncentracie.csv')
def linearna_regresia (rok,pole_prediktor, tabulka, pole_lat, pole_lon):
    hodnoty=[] #hodnoty v gridovom bode 
    for i,row in tabulka.iterrows():
        lat_x=row['lat_x']
        lon_x=row['lon_x']
        ix, iy = getclosest_ij(pole_lat,pole_lon,row['lat_x'],row['lon_x'])
        hodnoty.append(pole_prediktor[ix,iy])    
        
    pollutant=np.array(tabulka['no2'])
    
    X=np.asarray(hodnoty)
    XH=X.reshape(-1,1)
    #XH is special shape of X which is necessary for multivariable Linear regression
    y=pollutant
    # model is linear reggresion fit
    model = LinearRegression().fit(XH, y)
    # a, c are coeficcients of linear reggresion model
    a=model.coef_
    c=model.intercept_
    # PREDICT is a predicted values in points of measurments, shape is the same as pollutant
    PREDICT=(a*pole_prediktor)+c
    Predikovane_hodnoty=[]
    for i,row in tabulka.iterrows():
        lat_x=row['lat_x']
        lon_x=row['lon_x']
        ix, iy = getclosest_ij(pole_lat,pole_lon,row['lat_x'],row['lon_x'])
        Predikovane_hodnoty.append(PREDICT[ix,iy])    
    Predikovane_hodnoty=np.asarray(Predikovane_hodnoty)
    rmse=np.sqrt(metrics.mean_squared_error(pollutant,Predikovane_hodnoty))
    r2=metrics.r2_score(pollutant,Predikovane_hodnoty)
    #np.save('regresne_pole_2020.npy',PREDICT)
    b=mapb.pcolormesh(pole_lon,pole_lat,PREDICT,cmap=plt.cm.jet,latlon=True)
    mapb.drawcountries(linewidth=3)
    mapb.drawrivers()
    cb=plt.colorbar(label='$\mu$g.$m^{-3}$')
    font = matplotlib.font_manager.FontProperties( style='italic', size=16)
    cb.ax.yaxis.label.set_font_properties(font)
    plt.title('Prízemné koncentrácie za rok '+str(rok)+' (lineárna regresia)')
    plt.clim(0,45)
    plt.savefig('Prízemné koncentrácie za rok '+str(rok)+' (lineárna regresia).png',bbox_inches='tight',dpi=600)
    plt.clf()
    #plt.show()
    return c,a,Predikovane_hodnoty,PREDICT,rmse,r2