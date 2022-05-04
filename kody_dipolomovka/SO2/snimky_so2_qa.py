#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 18:15:41 2021

@author: OMKO459
"""

import netCDF4
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from datetime import datetime
from datetime import timedelta
import matplotlib

plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = 28,10
mapb=Basemap(projection='lcc',lat_1=46.24470138549805,lat_2=46.24470138549805,lat_0=48.66,lon_0=19.7,width=432780,height=216351,resolution='h')
maska=np.load('/data/oko/dusan/maska.npy')

def getclosest_ij(nlats,nlons,latpt,lonpt):
    # find squared distance of every point on grid
    dist_sq = (nlats-latpt)**2 + (nlons-lonpt)**2  
    # 1D index of minimum dist_sq element
    minindex_flattened = dist_sq.argmin()    
    # Get 2D index for latvals and lonvals arrays from 1D index
    return np.unravel_index(minindex_flattened, nlats.shape)

dataset=netCDF4.Dataset('/data/oko/dusan/sentinel5P/so2/2021qa/post_dataqa/tropospheric_so2.nc')
lon= dataset.variables['lon'][:,:]
lat= dataset.variables['lat'][:,:]
so2= dataset.variables['tropospheric_so2'][0,:,:]

datumy=[]
for s in (dataset.variables['times'][:]):
    dates = datetime(2021, 9, 1,10,12,53,172413)+ timedelta(seconds=s)
    datumy.append(dates)
''' 
#for i in range(len(datumy)):
for i in range(93):    
    b=mapb.pcolormesh(lon,lat,dataset.variables['tropospheric_so2'][i,:,:],cmap=plt.cm.jet,latlon=True)
    mapb.drawcountries(linewidth=3)
    mapb.drawrivers()
    cb=plt.colorbar(label='mol/m$^2$')
    font = matplotlib.font_manager.FontProperties( style='italic', size=16)
    cb.ax.yaxis.label.set_font_properties(font)
    plt.title('SO2 v case: ' + str(datumy[i]))
    #plt.clim(0, 0.02)
    #plt.savefig('Priemerná hodnota troposférického stĺpca NO$_2$ za rok 2019.png',bbox_inches='tight',dpi=600)
    plt.show()
    #plt.clf()
'''
priemery=[] 
pocty_bodov=[]  
#for z in range(len(datumy)):
for z in range(94):   
    priemer= dataset.variables['tropospheric_so2'][z,:,:].mean()
    pocet= dataset.variables['tropospheric_so2'][z,:,:].count()
    priemery.append(priemer)
    pocty_bodov.append(pocet)
    
data = {'Dátum': datumy[0:94],'Priemer': priemery,'Počet': pocty_bodov}
df = pd.DataFrame(data)
df['Dátum']=pd.to_datetime(df['Dátum']).dt.date


df.plot(x ='Dátum', y='Priemer', kind = 'bar')
plt.title('Priemerné hodnoty celkového stĺpca SO$_2$ vypočítané zo všetkých pixlov na každej snímke pri úrovni filtra B v období od 1.9.2021 do 24.10.2021')
#plt.title('Priemerné hodnoty troposférického stĺpca SO$_2$ na doméne za obdobie od 1.9.2021 do 24.10.2021')
plt.xlabel('Dátum')
plt.ylabel("SO$_2$ [mol/m$^2$]")
plt.annotate('Prechod oblaku plynov 20.10.2021', xy=(86.2, 0.00135), xytext=(55,0.0027),color='red',
            arrowprops=dict(facecolor='red', shrink=0.03))
plt.savefig('Priemerné hodnoty celkového stĺpca SO2qa na doméne za obdobie od 1.9.2021 do 24.10.2021.png',bbox_inches='tight',dpi=600)

##########
df_filtered = df[df['Počet'] > 68039/2]
##########
df_filtered.plot(x ='Dátum', y='Priemer', kind = 'bar')
plt.title('Priemerné hodnoty celkového stĺpca SO$_2$ vypočítané zo všetkých pixlov na každej dostatočne reprezentatívnej snímke pri úrovni filtra B v období od 1.9.2021 do 24.10.2021')
#plt.title('Priemerné hodnoty troposférického stĺpca SO$_2$ na doméne za obdobie od 1.9.2021 do 24.10.2021')
plt.xlabel('Dátum')
plt.ylabel("SO$_2$ [mol/m$^2$]")
plt.annotate('Prechod oblaku plynov 20.10.2021', xy=(42, 0.00132), xytext=(21,0.0015),color='red',
            arrowprops=dict(facecolor='red', shrink=0.03))
plt.savefig('Priemerné hodnoty celkového stĺpca SO2qa filtered na doméne za obdobie od 1.9.2021 do 24.10.2021.png',bbox_inches='tight',dpi=600)
