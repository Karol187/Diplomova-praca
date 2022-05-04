#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 10:49:03 2022

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
import numpy.ma as ma
plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = 20,8
mapb=Basemap(projection='lcc',lat_1=46.24470138549805,lat_2=46.24470138549805,lat_0=48.66,lon_0=19.7,width=432780,height=216351,resolution='h')
maska=np.load('/data/oko/dusan/maska.npy')

dataset=netCDF4.Dataset('/data/oko/dusan/sentinel5P/AER/2019/post_data/aer_354_38.nc')
lon= dataset.variables['lon'][:,:]
lat= dataset.variables['lat'][:,:]
aer= dataset.variables['aer_354_38'][:,:,:]
pocet_snimkov= len(dataset.variables['aer_354_38'][:,0,0])

aer_polia=[]
aer_polia_positive=[]
aer_polia_negative=[]
for k in range (pocet_snimkov):
     aer_polia.append(aer[k,:,:])  
     aer_polia_positive.append(np.where(aer[k,:,:]<0,np.nan,aer[k,:,:])) 
     aer_polia_negative.append(np.where(aer[k,:,:]>0,np.nan,aer[k,:,:])) 
priemer_2019=np.nanmean(aer_polia,axis=0)     
priemer_2019_positive=np.nanmean(aer_polia_positive,axis=0)     
priemer_2019_negative=np.nanmean(aer_polia_negative,axis=0)   
pocet_platnych_dat_positive=np.count_nonzero(~np.isnan(aer_polia_positive),axis=0)
pocet_platnych_dat_negative=np.count_nonzero(~np.isnan(aer_polia_negative),axis=0)

print('Minimalny pocet platnych dat kladnych je:'+ str(np.nanmin((pocet_platnych_dat_positive)*maska)))
print('Maximalny pocet platnych dat kladnych je:'+ str(np.nanmax((pocet_platnych_dat_positive)*maska)))
print('Minimalny pocet platnych dat zapornych je:'+ str(np.nanmin((pocet_platnych_dat_negative)*maska)))
print('Maximalny pocet platnych dat zapornych je:'+ str(np.nanmax((pocet_platnych_dat_negative)*maska)))


b=mapb.pcolormesh(lon,lat,pocet_platnych_dat_positive*maska,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='Počet hodnôt')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Počet kladných hodnôt')

plt.savefig('Počet kladných hodnot.png',bbox_inches='tight',dpi=600)
plt.clf()

b=mapb.pcolormesh(lon,lat,pocet_platnych_dat_negative*maska,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='Počet hodnôt')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Počet záporných hodnôt')

plt.savefig('Počet záporných hodnot.png',bbox_inches='tight',dpi=600)
plt.clf()

b=mapb.pcolormesh(lon,lat,priemer_2019*maska,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='AI 354/388nm')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Priemerná hodnota aerosólového indexu za rok 2019')
#plt.show()
plt.savefig('Priemerná hodnota aerosólového indexu za rok 2019.png',bbox_inches='tight',dpi=600)
plt.clf()

b=mapb.pcolormesh(lon,lat,priemer_2019_positive*maska,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='AI 354/388nm')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Priemerná hodnota vypočítaná z kladných hodnôt aerosólového indexu za rok 2019')
#plt.show()
plt.savefig('Priemerná hodnota vypočítaná z kladných hodnôt aerosólového indexu za rok 2019.png',bbox_inches='tight',dpi=600)
plt.clf()

b=mapb.pcolormesh(lon,lat,priemer_2019_negative*maska,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='AI 354/388nm')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Priemerná hodnota vypočítaná zo záporných hodnôt aerosólového indexu za rok 2019')
#plt.show()
plt.savefig('Priemerná hodnota vypočítaná zo záporných hodnôt aerosólového indexu za rok 2019.png',bbox_inches='tight',dpi=600)
plt.clf()

np.save('priemer_aer_2019',priemer_2019*maska)
np.save('priemer_aer_2019_positive',priemer_2019_positive*maska)
np.save('aer_pocet_platnych_dat_positive_2019',pocet_platnych_dat_positive*maska)
np.save('priemer_aer_2019_negative',priemer_2019_negative*maska)
np.save('aer_pocet_platnych_dat_negative_2019',pocet_platnych_dat_negative*maska)





