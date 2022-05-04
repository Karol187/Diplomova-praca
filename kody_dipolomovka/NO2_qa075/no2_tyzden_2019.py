#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 09:25:25 2021

@author: OMKO459
"""

import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.basemap import Basemap
from datetime import datetime
from datetime import timedelta
import pandas as pd
from datetime import date
import calendar
plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = 20,8

mapb=Basemap(projection='lcc',lat_1=46.24470138549805,lat_2=46.24470138549805,lat_0=48.66,lon_0=19.7,width=432780,height=216351,resolution='h')
maska=np.load('/data/oko/dusan/maska.npy')

rok=2019
dataset=netCDF4.Dataset('/data/oko/dusan/sentinel5P/no2/2019/post_data/no2_trop_grid.nc')

pocet_snimkov= len(dataset.variables['tropospheric_no2'][:,0,0])
lon= dataset.variables['lon'][:,:]
lat= dataset.variables['lat'][:,:]
tropospheric_no2= dataset.variables['tropospheric_no2'][:,:,:]

tropospheric_no2_polia=[]
for k in range (pocet_snimkov):
     tropospheric_no2_polia.append(tropospheric_no2[k,:,:])
priemer=np.nanmean(tropospheric_no2_polia,axis=0)

datumy=[]
for s in (dataset.variables['times'][:]):
    dates = datetime(rok, 1, 1,11,15,46,949999)+ timedelta(seconds=s)
    datumy.append(dates)
    
dni=[]
for i in (datumy):
    dni.append(calendar.day_name[i.weekday()])
    
weekdays_priemer_polia=[]    
weekdays_pocet_polia=[]   
nazvy_dni=[]
for day in ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'):
    indices = [index for index, element in enumerate(dni) if element == day]
    #[tropospheric_no2_polia[i] for i in indices]
    priemer_weekday=np.nanmean([tropospheric_no2_polia[i] for i in indices],axis=0)
    weekdays_priemer_polia.append(priemer_weekday)
    pocet_dat_weekday=np.count_nonzero(~np.isnan([tropospheric_no2_polia[i] for i in indices]),axis=0)
    weekdays_pocet_polia.append(pocet_dat_weekday)
    nazvy_dni.append(day)
    
pocet_dictionary = dict(zip(nazvy_dni, weekdays_pocet_polia))    
priemer_dictionary = dict(zip(nazvy_dni, weekdays_priemer_polia)) 
 
nazvy_dni_sk= ['pondelky', 'utorky', 'stredy', 'štvrtky', 'piatky', 'soboty', 'nedele']  
# changing keys of dictionary
pocet_dictionary = dict(zip(nazvy_dni_sk, list(pocet_dictionary.values())))
priemer_dictionary= dict(zip(nazvy_dni_sk, list(priemer_dictionary.values())))

for key, value in priemer_dictionary.items():
    b=mapb.pcolormesh(lon,lat,value*maska,cmap=plt.cm.jet,latlon=True)
    mapb.drawcountries(linewidth=3)
    mapb.drawrivers()
    cb=plt.colorbar(label='mol/m$^2$')
    font = matplotlib.font_manager.FontProperties( style='italic', size=16)
    cb.ax.yaxis.label.set_font_properties(font)
    plt.title('Priemerná hodnota troposférického stĺpca NO$_2$ za všetky ' +str(key)+' v roku '+str(rok))
    plt.clim(0, 0.00010)
    #plt.savefig('Priemerna hodnota troposferickeho stĺpca NO$_2$ za zimne obdobie '+str(date(2019,12,1))+' - '+str(date(2020,2,29))+'.png',bbox_inches='tight',dpi=600)
    plt.show()
    plt.clf()
'''
for key, value in priemer_dictionary.items():
    np.save(str(key)+'_'+str(rok),value*maska)
'''
for key, value in pocet_dictionary.items():
    b=mapb.pcolormesh(lon,lat,value*maska,cmap=plt.cm.jet,latlon=True)
    mapb.drawcountries(linewidth=3)
    mapb.drawrivers()
    cb=plt.colorbar(label='Počet dát')
    font = matplotlib.font_manager.FontProperties( style='italic', size=16)
    cb.ax.yaxis.label.set_font_properties(font)
    plt.title('Počet dát (všetky '+str(key)+' )v roku '+str(rok))
    #plt.savefig('Priemerna hodnota troposferickeho stĺpca NO$_2$ za zimne obdobie '+str(date(2019,12,1))+' - '+str(date(2020,2,29))+'.png',bbox_inches='tight',dpi=600)
    plt.show()
    plt.clf()

   
 
    
def getclosest_ij(nlats,nlons,latpt,lonpt):
    # find squared distance of every point on grid
    dist_sq = (nlats-latpt)**2 + (nlons-lonpt)**2  
    # 1D index of minimum dist_sq element
    minindex_flattened = dist_sq.argmin()    
    # Get 2D index for latvals and lonvals arrays from 1D index
    return np.unravel_index(minindex_flattened, nlats.shape)
    ##############################################################################################
tabulka=pd.read_csv('/data/karol/diplomovka/stanice_no2_2019_prizemne_koncentracie.csv')
# %matplotlib inline
for i, row in tabulka.iterrows():   
    priemery=[]
    zmena=[]
    den=[]
    for key, pole in priemer_dictionary.items():
        ix, iy=getclosest_ij(lat,lon,row['lat_x'],row['lon_x'])
        priemery.append(pole[ix, iy]) 
        zmena.append(((pole[ix, iy]-priemer[ix,iy])/priemer[ix,iy])*100)
        den.append(key)
        
    data = {'Deň': den,'Priemer': priemery,'Zmena': zmena}
    df = pd.DataFrame(data)
    
    df.plot(kind = 'line',
            x ='Deň',
            y ='Priemer' ,
            color = 'red')
    plt.title(str(row['name'])+' počas roka '+str(rok))
    plt.xlabel('Deň')
    plt.ylabel("Troposférický stĺpec NO$_2$ [mol/m$^2$]")
    plt.xticks(rotation='horizontal')
    plt.savefig(str(row['name'])+' za jednotlive dni v tyzdni v roku '+str(rok)+'.png',bbox_inches='tight',dpi=600)
    #plt.show()
    plt.clf()
    
    df.plot(kind = 'line',
            x ='Deň',
            y ='Zmena' ,
            color = 'red')
    plt.title(str(row['name'])+' počas roka '+str(rok))
    plt.xlabel('Deň')
    plt.ylabel("Zmena [%] oproti priemernej hodnote za celý rok")
    plt.xticks(rotation='horizontal')
    plt.savefig(str(row['name'])+' % zmena za jednotlive dni v tyzdni v roku '+str(rok)+'.png',bbox_inches='tight',dpi=600)
    #plt.show()
    plt.clf()
    
