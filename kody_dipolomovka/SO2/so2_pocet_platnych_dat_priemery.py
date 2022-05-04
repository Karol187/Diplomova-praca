#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 16:45:51 2022

@author: OMKO459
"""

import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.basemap import Basemap

plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = 20,8

mapb=Basemap(projection='lcc',lat_1=46.24470138549805,lat_2=46.24470138549805,lat_0=48.66,lon_0=19.7,width=432780,height=216351,resolution='h')

dataset_so2=netCDF4.Dataset('/data/oko/dusan/sentinel5P/so2/2021/post_data/tropospheric_so2.nc')
dataset_so2qa=netCDF4.Dataset('/data/oko/dusan/sentinel5P/so2/2021qa/post_dataqa/tropospheric_so2.nc')
dataset_so2qa0=netCDF4.Dataset('/data/oko/dusan/sentinel5P/so2/2021qa0/post_dataqa0/tropospheric_so2.nc')
pocet_snimkov_so2= len(dataset_so2.variables['tropospheric_so2'][:,0,0])
pocet_snimkov_so2qa= 94# pocet snimkovod 1.9. do 24.11
pocet_snimkov_so2qa0= 98# pocet snimkovod 1.9. do 24.11
lon= dataset_so2.variables['lon'][:,:]
lat= dataset_so2.variables['lat'][:,:]
tropospheric_so2= dataset_so2.variables['tropospheric_so2'][:,:,:]
tropospheric_so2qa= dataset_so2qa.variables['tropospheric_so2'][:,:,:]
tropospheric_so2qa0= dataset_so2qa0.variables['tropospheric_so2'][:,:,:]

tropospheric_so2_polia=[]
for k in range (pocet_snimkov_so2):
     tropospheric_so2_polia.append(tropospheric_so2[k,:,:])
priemer_so2=np.nanmean(tropospheric_so2_polia,axis=0)

tropospheric_so2qa_polia=[]
for k in range (pocet_snimkov_so2qa):
     tropospheric_so2qa_polia.append(tropospheric_so2qa[k,:,:])
priemer_so2qa=np.nanmean(tropospheric_so2qa_polia,axis=0)

tropospheric_so2qa0_polia=[]
for k in range (pocet_snimkov_so2qa):
     tropospheric_so2qa0_polia.append(tropospheric_so2qa0[k,:,:])
priemer_so2qa0=np.nanmean(tropospheric_so2qa0_polia,axis=0)

pocet_platnych_dat_so2=np.count_nonzero(~np.isnan(tropospheric_so2_polia),axis=0)
pocet_platnych_dat_so2qa=np.count_nonzero(~np.isnan(tropospheric_so2qa_polia),axis=0)
pocet_platnych_dat_so2qa0=np.count_nonzero(~np.isnan(tropospheric_so2qa0_polia),axis=0)
maska=np.load('/data/oko/dusan/maska.npy')

###################################### PRIEMERY #######################################
b=mapb.pcolormesh(lon,lat,priemer_so2*maska,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='mol/m$^2$')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Priemerná hodnota celkového stĺpca SO$_2$ za obdobie od 1.9.2021 do 24.10.2021')
plt.clim(-0.0007, 0.003)
#plt.show()
plt.savefig('Priemerná hodnota celkového stĺpca so2 za obdobie od 1.9.2021 do 24.10.2021.png',bbox_inches='tight',dpi=600)
plt.clf()

b=mapb.pcolormesh(lon,lat,priemer_so2qa*maska,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='mol/m$^2$')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Priemerná hodnota celkového stĺpca SO$_2$ za obdobie od 1.9.2021 do 24.10.2021')
plt.clim(-0.0007, 0.003)
#plt.show()
plt.savefig('Priemerná hodnota celkového stĺpca so2qa za obdobie od 1.9.2021 do 24.10.2021.png',bbox_inches='tight',dpi=600)
plt.clf()

b=mapb.pcolormesh(lon,lat,priemer_so2qa0*maska,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='mol/m$^2$')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Priemerná hodnota celkového stĺpca SO$_2$ za obdobie od 1.9.2021 do 24.10.2021')
plt.clim(-0.0007, 0.003)
#plt.show()
plt.savefig('Priemerná hodnota celkového stĺpca so2qa0 za obdobie od 1.9.2021 do 24.10.2021.png',bbox_inches='tight',dpi=600)
plt.clf()
######################################## POCET DAT#####################################
b=mapb.pcolormesh(lon,lat,pocet_platnych_dat_so2*maska,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='Počet dát')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Počet platných dát za obdobie od 1.9.2021 do 24.10.2021')
plt.clim(0,125)
#plt.show()
plt.savefig('Počet platných dát so2 za obdobie od 1.9.2021 do 24.10.2021.png',bbox_inches='tight',dpi=600)
plt.clf()

b=mapb.pcolormesh(lon,lat,pocet_platnych_dat_so2qa*maska,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='Počet dát')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Počet platných dát za obdobie od 1.9.2021 do 24.10.2021')
plt.clim(0,125)
#plt.show()
plt.savefig('Počet platných dát so2qa za obdobie od 1.9.2021 do 24.10.2021.png',bbox_inches='tight',dpi=600)
plt.clf()

b=mapb.pcolormesh(lon,lat,pocet_platnych_dat_so2qa0*maska,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='Počet dát')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Počet platných dát za obdobie od 1.9.2021 do 24.10.2021')
plt.clim(0,125)
#plt.show()
plt.savefig('Počet platných dát so2qa0 za obdobie od 1.9.2021 do 24.10.2021.png',bbox_inches='tight',dpi=600)
plt.clf()

