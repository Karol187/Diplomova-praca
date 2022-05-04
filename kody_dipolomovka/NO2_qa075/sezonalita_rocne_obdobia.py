#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 10:44:06 2021

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

datumy_2019_2020=datumy_2019+datumy_2020
tropospheric_no2_polia_2019_2020= tropospheric_no2_polia_2019+tropospheric_no2_polia_2020

def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))

##############################################################################################
'''
ZIMA:
'''
index_start=datumy_2019_2020.index(nearest(datumy_2019_2020,datetime(2019, 12, 1, 6, 0, 0, 0)))
index_end=datumy_2019_2020.index(nearest(datumy_2019_2020,datetime(2020, 2, 29, 15, 0, 0, 0)))
obdobie_datumy=datumy_2019_2020[index_start:index_end+1]
obdobie_polia=tropospheric_no2_polia_2019_2020[index_start:index_end+1]
priemer_2019_2020_obdobie=np.nanmean(obdobie_polia,axis=0)
pocet_platnych_dat_2019_2020_obdobie=np.count_nonzero(~np.isnan(obdobie_polia),axis=0)

np.save('zima_no2_pocet_dat',pocet_platnych_dat_2019_2020_obdobie*maska)
np.save('zima_no2_priemer',priemer_2019_2020_obdobie*maska)

b=mapb.pcolormesh(lon_2019,lat_2019,priemer_2019_2020_obdobie*maska,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='mol/m$^2$')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Priemerná hodnota troposférického stĺpca NO$_2$ za zimné obdobie '+str(date(2019,12,1))+' - '+str(date(2020,2,29)))
plt.clim(0, 0.00010)
plt.savefig('Priemerna hodnota troposferickeho stĺpca NO$_2$ za zimne obdobie '+str(date(2019,12,1))+' - '+str(date(2020,2,29))+'.png',bbox_inches='tight',dpi=600)
plt.clf()


b=mapb.pcolormesh(lon_2019,lat_2019,pocet_platnych_dat_2019_2020_obdobie*maska,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='Počet dát')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Počet platných dát za zimné obdobie '+str(date(2019,12,1))+' - '+str(date(2020,2,29)))
plt.clim(0,100)
plt.savefig('Pocet platnych dat za zimne obdobie '+str(date(2019,12,1))+' - '+str(date(2020,2,29))+'.png',bbox_inches='tight',dpi=600)
plt.clf()


'''
JAR:
'''
index_start=datumy_2019_2020.index(nearest(datumy_2019_2020,datetime(2020, 3, 1, 6, 0, 0, 0)))
index_end=datumy_2019_2020.index(nearest(datumy_2019_2020,datetime(2020, 5, 31, 15, 0, 0, 0)))
obdobie_datumy=datumy_2019_2020[index_start:index_end+1]
obdobie_polia=tropospheric_no2_polia_2019_2020[index_start:index_end+1]
priemer_2019_2020_obdobie=np.nanmean(obdobie_polia,axis=0)
pocet_platnych_dat_2019_2020_obdobie=np.count_nonzero(~np.isnan(obdobie_polia),axis=0)

np.save('jar_no2_pocet_dat',pocet_platnych_dat_2019_2020_obdobie*maska)
np.save('jar_no2_priemer',priemer_2019_2020_obdobie*maska)

b=mapb.pcolormesh(lon_2019,lat_2019,priemer_2019_2020_obdobie*maska,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='mol/m$^2$')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Priemerná hodnota troposférického stĺpca NO$_2$ za jarné obdobie '+str(date(2020,3,1))+' - '+str(date(2020,5,31)))
plt.clim(0, 0.00010)
plt.savefig('Priemerna hodnota troposferickeho stĺpca NO$_2$ za jarne obdobie '+str(date(2020,3,1))+' - '+str(date(2020,5,31))+'.png',bbox_inches='tight',dpi=600)
plt.clf()


b=mapb.pcolormesh(lon_2019,lat_2019,pocet_platnych_dat_2019_2020_obdobie*maska,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='Počet dát')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Počet platných dát za jarné obdobie '+str(date(2020,3,1))+' - '+str(date(2020,5,31)))
plt.clim(0,100)
plt.savefig('Pocet platnych dat za jarne obdobie '+str(date(2020,3,1))+' - '+str(date(2020,5,31))+'.png',bbox_inches='tight',dpi=600)
plt.clf()


'''
LETO:
'''
index_start=datumy_2019_2020.index(nearest(datumy_2019_2020,datetime(2020, 6, 1, 6, 0, 0, 0)))
index_end=datumy_2019_2020.index(nearest(datumy_2019_2020,datetime(2020, 8, 31, 15, 0, 0, 0)))
obdobie_datumy=datumy_2019_2020[index_start:index_end+1]
obdobie_polia=tropospheric_no2_polia_2019_2020[index_start:index_end+1]
priemer_2019_2020_obdobie=np.nanmean(obdobie_polia,axis=0)
pocet_platnych_dat_2019_2020_obdobie=np.count_nonzero(~np.isnan(obdobie_polia),axis=0)

np.save('leto_no2_pocet_dat',pocet_platnych_dat_2019_2020_obdobie*maska)
np.save('leto_no2_priemer',priemer_2019_2020_obdobie*maska)

b=mapb.pcolormesh(lon_2019,lat_2019,priemer_2019_2020_obdobie*maska,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='mol/m$^2$')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Priemerná hodnota troposférického stĺpca NO$_2$ za letné obdobie '+str(date(2020,6,1))+' - '+str(date(2020,8,31)))
plt.clim(0, 0.00010)
plt.savefig('Priemerna hodnota troposferickeho stĺpca NO$_2$ za letne obdobie '+str(date(2020,6,1))+' - '+str(date(2020,8,31))+'.png',bbox_inches='tight',dpi=600)
plt.clf()


b=mapb.pcolormesh(lon_2019,lat_2019,pocet_platnych_dat_2019_2020_obdobie*maska,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='Počet dát')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Počet platných dát za letné obdobie '+str(date(2020,6,1))+' - '+str(date(2020,8,31)))
plt.clim(0,100)
plt.savefig('Pocet platnych dat za letne obdobie '+str(date(2020,6,1))+' - '+str(date(2020,8,31))+'.png',bbox_inches='tight',dpi=600)
plt.clf()


'''
JESEN:
'''
index_start=datumy_2019_2020.index(nearest(datumy_2019_2020,datetime(2020, 9, 1, 6, 0, 0, 0)))
index_end=datumy_2019_2020.index(nearest(datumy_2019_2020,datetime(2020, 11, 30, 15, 0, 0, 0)))
obdobie_datumy=datumy_2019_2020[index_start:index_end+1]
obdobie_polia=tropospheric_no2_polia_2019_2020[index_start:index_end+1]
priemer_2019_2020_obdobie=np.nanmean(obdobie_polia,axis=0)
pocet_platnych_dat_2019_2020_obdobie=np.count_nonzero(~np.isnan(obdobie_polia),axis=0)

np.save('jesen_no2_pocet_dat',pocet_platnych_dat_2019_2020_obdobie*maska)
np.save('jesen_no2_priemer',priemer_2019_2020_obdobie*maska)

b=mapb.pcolormesh(lon_2019,lat_2019,priemer_2019_2020_obdobie*maska,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='mol/m$^2$')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Priemerná hodnota troposférického stĺpca NO$_2$ za jesenné obdobie '+str(date(2020,9,1))+' - '+str(date(2020,11,30)))
plt.clim(0, 0.00010)
plt.savefig('Priemerna hodnota troposferickeho stĺpca NO$_2$ za jesenne obdobie '+str(date(2020,9,1))+' - '+str(date(2020,11,30))+'.png',bbox_inches='tight',dpi=600)
plt.clf()


b=mapb.pcolormesh(lon_2019,lat_2019,pocet_platnych_dat_2019_2020_obdobie*maska,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='Počet dát')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Počet platných dát za jesenné obdobie '+str(date(2020,9,1))+' - '+str(date(2020,11,30)))
plt.clim(0,100)
plt.savefig('Pocet platnych dat za jesenne obdobie '+str(date(2020,9,1))+' - '+str(date(2020,11,30))+'.png',bbox_inches='tight',dpi=600)
plt.clf()


