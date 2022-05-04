#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 14:41:46 2021

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
plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = 20,8

mapb=Basemap(projection='lcc',lat_1=46.24470138549805,lat_2=46.24470138549805,lat_0=48.66,lon_0=19.7,width=432780,height=216351,resolution='h')
maska=np.load('/data/oko/dusan/maska.npy')

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
priemer_2019=np.nanmean(tropospheric_no2_polia_2019,axis=0)

tropospheric_no2_polia_2020=[]
for k in range (pocet_snimkov_2020):
     tropospheric_no2_polia_2020.append(tropospheric_no2_2020[k,:,:])
priemer_2020=np.nanmean(tropospheric_no2_polia_2020,axis=0)

datumy_2019=[]
for s in (dataset_2019.variables['times'][:]):
    dates = datetime(2019, 1, 1,11,15,46,949999)+ timedelta(seconds=s)
    datumy_2019.append(dates)

datumy_2020=[]
for s in (dataset_2020.variables['times'][:]):
    dates = datetime(2020, 1, 1,10,32,12,742616)+ timedelta(seconds=s)
    datumy_2020.append(dates)
    
def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))


month = [1,2,3,4,5,6,7,8,9,10,11,12]
day = [31, 28, 31,30,31,30,31,31,30,31,30,31]

for i,j in zip(month,day):
    index_start=datumy_2019.index(nearest(datumy_2019,datetime(2019, i, 1, 6, 0, 0, 0)))
    index_end=datumy_2019.index(nearest(datumy_2019,datetime(2019, i, j, 15, 0, 0, 0)))
    mesiac_datumy=datumy_2019[index_start:index_end+1]
    mesiac_polia=tropospheric_no2_polia_2019[index_start:index_end+1]
    priemer_2019_mesiac=np.nanmean(mesiac_polia,axis=0)
    pocet_platnych_dat_2019_mesiac=np.count_nonzero(~np.isnan(mesiac_polia),axis=0)
    
    b=mapb.pcolormesh(lon_2019,lat_2019,priemer_2019_mesiac*maska,cmap=plt.cm.jet,latlon=True)
    mapb.drawcountries(linewidth=3)
    mapb.drawrivers()
    cb=plt.colorbar(label='mol/m$^2$')
    font = matplotlib.font_manager.FontProperties( style='italic', size=16)
    cb.ax.yaxis.label.set_font_properties(font)
    plt.title('Priemerná hodnota troposférického stĺpca NO$_2$ za obdobie '+str(date(2019,i,1))+' - '+str(date(2019,i,j)))
    plt.clim(0, 0.00010)
    plt.savefig('Priemerna hodnota troposferickeho stĺpca NO$_2$ za obdobie '+str(date(2019,i,1))+' - '+str(date(2019,i,j))+'.png',bbox_inches='tight',dpi=600)
    plt.clf()
    
    b=mapb.pcolormesh(lon_2019,lat_2019,pocet_platnych_dat_2019_mesiac*maska,cmap=plt.cm.jet,latlon=True)
    mapb.drawcountries(linewidth=3)
    mapb.drawrivers()
    cb=plt.colorbar(label='Počet dát')
    font = matplotlib.font_manager.FontProperties( style='italic', size=16)
    cb.ax.yaxis.label.set_font_properties(font)
    plt.title('Počet platných dát za obdobie '+str(date(2019,i,1))+' - '+str(date(2019,i,j)))
    plt.clim(0,50)
    plt.savefig('Pocet platnych dat za obdobie '+str(date(2019,i,1))+' - '+str(date(2019,i,j))+'.png',bbox_inches='tight',dpi=600)
    plt.clf()

month = [1,2,3,4,5,6,7,8,9,10,11,12]
day = [31, 29, 31,30,31,30,31,31,30,31,30,31]

for i,j in zip(month,day):
    index_start=datumy_2020.index(nearest(datumy_2020,datetime(2020, i, 1, 6, 0, 0, 0)))
    index_end=datumy_2020.index(nearest(datumy_2020,datetime(2020, i, j, 15, 0, 0, 0)))
    mesiac_datumy=datumy_2020[index_start:index_end+1]
    mesiac_polia=tropospheric_no2_polia_2020[index_start:index_end+1]
    priemer_2020_mesiac=np.nanmean(mesiac_polia,axis=0)
    pocet_platnych_dat_2020_mesiac=np.count_nonzero(~np.isnan(mesiac_polia),axis=0)
    
    b=mapb.pcolormesh(lon_2019,lat_2019,priemer_2020_mesiac*maska,cmap=plt.cm.jet,latlon=True)
    mapb.drawcountries(linewidth=3)
    mapb.drawrivers()
    cb=plt.colorbar(label='mol/m$^2$')
    font = matplotlib.font_manager.FontProperties( style='italic', size=16)
    cb.ax.yaxis.label.set_font_properties(font)
    plt.title('Priemerná hodnota troposférického stĺpca NO$_2$ za obdobie '+str(date(2020,i,1))+' - '+str(date(2020,i,j)))
    plt.clim(0, 0.00010)
    plt.savefig('Priemerna hodnota troposferickeho stĺpca NO$_2$ za obdobie '+str(date(2020,i,1))+' - '+str(date(2020,i,j))+'.png',bbox_inches='tight',dpi=600)
    plt.clf()
    
    b=mapb.pcolormesh(lon_2019,lat_2019,pocet_platnych_dat_2020_mesiac*maska,cmap=plt.cm.jet,latlon=True)
    mapb.drawcountries(linewidth=3)
    mapb.drawrivers()
    cb=plt.colorbar(label='Počet dát')
    font = matplotlib.font_manager.FontProperties( style='italic', size=16)
    cb.ax.yaxis.label.set_font_properties(font)
    plt.title('Počet platných dát za obdobie '+str(date(2020,i,1))+' - '+str(date(2020,i,j)))
    plt.clim(0,50)
    plt.savefig('Pocet platnych dat za obdobie '+str(date(2020,i,1))+' - '+str(date(2020,i,j))+'.png',bbox_inches='tight',dpi=600)
    plt.clf()

















































































'''
index_start=datumy_2020.index(nearest(datumy_2020,datetime(2020, 1, 1, 0, 0, 0, 0)))
index_end=datumy_2020.index(nearest(datumy_2020,datetime(2020, 1, 31, 15, 0, 0, 0)))
mesiac_datumy=datumy_2020[index_start:index_end+1]
mesiac_polia=tropospheric_no2_polia_2020[index_start:index_end+1]
priemer_2020_mesiac=np.nanmean(mesiac_polia,axis=0)
pocet_platnych_dat_2020_mesiac=np.count_nonzero(~np.isnan(mesiac_polia),axis=0)

b=mapb.pcolormesh(lon_2020,lat_2020,priemer_2020_mesiac*maska,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='mol/m$^2$')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Hodnota troposférického stĺpca NO$_2$'+str(nearest(datumy_2019,datetime(2019, 3, 2, 0, 0, 0, 0))))
plt.clim(0, 0.00010)
plt.show()


b=mapb.pcolormesh(lon_2020,lat_2020,pocet_platnych_dat_2020_mesiac*maska,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='mol/m$^2$')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Hodnota troposférického stĺpca NO$_2$'+str(nearest(datumy_2019,datetime(2019, 3, 2, 0, 0, 0, 0))))

plt.show()
'''

