#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 09:07:29 2022

@author: OMKO459
"""

import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.basemap import Basemap
from datetime import datetime
from datetime import timedelta
plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = 20,8

mapb=Basemap(projection='lcc',lat_1=46.24470138549805,lat_2=46.24470138549805,lat_0=48.66,lon_0=19.7,width=432780,height=216351,resolution='h')

dataset_so2=netCDF4.Dataset('/data/oko/dusan/sentinel5P/so2/2019/post_data/tropospheric_so2.nc')
pocet_snimkov_so2= len(dataset_so2.variables['tropospheric_so2'][:,0,0])
lon= dataset_so2.variables['lon'][:,:]
lat= dataset_so2.variables['lat'][:,:]
tropospheric_so2= dataset_so2.variables['tropospheric_so2'][:,:,:]


tropospheric_so2_polia=[]
for k in range (pocet_snimkov_so2):
     tropospheric_so2_polia.append(tropospheric_so2[k,:,:])
priemer_so2=np.nanmean(tropospheric_so2_polia,axis=0)

pocet_platnych_dat_so2=np.count_nonzero(~np.isnan(tropospheric_so2_polia),axis=0)
maska=np.load('/data/oko/dusan/maska.npy')



b=mapb.pcolormesh(lon,lat,priemer_so2*maska,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='mol/m$^2$')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Priemerná hodnota celkového stĺpca SO$_2$ za rok 2019')
#plt.show()
plt.savefig('Priemerná hodnota celkového stĺpca so2 za rok 2019.png',bbox_inches='tight',dpi=600)
plt.clf()

b=mapb.pcolormesh(lon,lat,pocet_platnych_dat_so2*maska,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='Počet dát')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Počet platných dát SO$_2$ za rok 2019')
plt.clim(50,300)
#plt.show()
plt.savefig('Počet platných dát so2 za rok 2019.png',bbox_inches='tight',dpi=600)
plt.clf()
########POROVNANIE POCTU PLATNYCH DAT MEDZI SO2 A NO2#################

pocet_platnych_dat_no2=np.load('/data/karol/diplomovka/pocet_platnych_dat_2019.npy')

b=mapb.pcolormesh(lon,lat,pocet_platnych_dat_no2*maska,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='Počet dát')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Počet platných dát NO$_2$ za rok 2019')
plt.clim(50,300)
#plt.show()
plt.savefig('Počet platných dát no2 za rok 2019 pre ucel porovnania s so2.png',bbox_inches='tight',dpi=600)
plt.clf()

b=mapb.pcolormesh(lon,lat,((pocet_platnych_dat_so2-pocet_platnych_dat_no2)/pocet_platnych_dat_no2)*100*maska,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='%')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('((SO$_2$-NO$_2$)/NO$_2$)*100% za rok 2019')
#plt.show()
plt.savefig('Percentualny rozdiel v pocte platnych dat medzi no2 a so2 za rok 2019.png',bbox_inches='tight',dpi=600)
plt.clf()


