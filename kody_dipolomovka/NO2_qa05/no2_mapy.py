#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 10:44:04 2021

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

dataset_2019=netCDF4.Dataset('/data/oko/dusan/sentinel5P/no2/2019qa05/post_data/tropospheric_no2.nc')
dataset_2020=netCDF4.Dataset('/data/oko/dusan/sentinel5P/no2/2020qa05/post_data/no2_trop_grid.nc')
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

rozdiel=priemer_2020-priemer_2019
percentalny_rozdiel= ((priemer_2020-priemer_2019)/priemer_2019)*100
pocet_platnych_dat_2019=np.count_nonzero(~np.isnan(tropospheric_no2_polia_2019),axis=0)
pocet_platnych_dat_2020=np.count_nonzero(~np.isnan(tropospheric_no2_polia_2020),axis=0)
maska=np.load('/data/oko/dusan/maska.npy')



b=mapb.pcolormesh(lon_2019,lat_2019,priemer_2019*maska,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='mol/m$^2$')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Priemerná hodnota troposférického stĺpca NO$_2$ za rok 2019')
plt.clim(0, 0.00010)
plt.savefig('Priemerná hodnota troposférického stĺpca NO$_2$ za rok 2019.png',bbox_inches='tight',dpi=600)
plt.clf()

b=mapb.pcolormesh(lon_2020,lat_2020,priemer_2020*maska,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='mol/m$^2$')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Priemerná hodnota troposférického stĺpca NO$_2$ za rok 2020')
plt.clim(0, 0.00010)
plt.savefig('Priemerná hodnota troposférického stĺpca NO$_2$ za rok 2020.png',bbox_inches='tight',dpi=600)
plt.clf()

b=mapb.pcolormesh(lon_2020,lat_2020,rozdiel*maska,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='mol/m$^2$')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Rozdiel (2020-2019) troposférického stĺpca NO$_2$')
plt.clim(-0.00001, 0.00001)
plt.savefig('Rozdiel (2020-2019) troposférického stĺpca NO$_2$.png',bbox_inches='tight',dpi=600)
plt.clf()

b=mapb.pcolormesh(lon_2020,lat_2020,percentalny_rozdiel*maska,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='%')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Pokles resp. rast [%] troposférického stĺpca NO$_2$ v roku 2020 oproti roku 2019')
#plt.clim(50,150)
plt.savefig('Pokles resp. rast [%] troposférického stĺpca NO$_2$ v roku 2020 oproti roku 2019.png',bbox_inches='tight',dpi=600)
plt.clf()

b=mapb.pcolormesh(lon_2019,lat_2019,pocet_platnych_dat_2019*maska,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='Počet dát')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Počet platných dát v roku 2019')
plt.clim(440,540)
plt.savefig('Počet platných dát v roku 2019.png',bbox_inches='tight',dpi=600)
plt.clf()

b=mapb.pcolormesh(lon_2020,lat_2020,pocet_platnych_dat_2020*maska,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='Počet dát')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Počet platných dát v roku 2020')
plt.clim(440,540)
plt.savefig('Počet platných dát v roku 2020.png',bbox_inches='tight',dpi=600)
plt.clf()



b=mapb.pcolormesh(lon_2020,lat_2020,(pocet_platnych_dat_2020-pocet_platnych_dat_2019)*maska,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='Počet dát (rozdiel)')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Rozdiel (2020-2019) v počte platných dát')
plt.clim(-40,55)
plt.savefig('Rozdiel (2020-2019) v počte platných dát.png',bbox_inches='tight',dpi=600)
plt.clf()

b=mapb.pcolormesh(lon_2019,lat_2019, ((pocet_platnych_dat_2019/pocet_snimkov_2019)*100)*maska,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='%')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Frakcia [%] platných dát v roku 2019')
plt.clim(50,100)
plt.savefig('Frakcia [%] platných dát v roku 2019.png',bbox_inches='tight',dpi=600)
plt.clf()

b=mapb.pcolormesh(lon_2020,lat_2020,((pocet_platnych_dat_2020/pocet_snimkov_2020)*100)*maska,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='%')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Frakcia [%] platných dát v roku 2020')
plt.clim(50,100)
plt.savefig('Frakcia [%] platných dát v roku 2020.png',bbox_inches='tight',dpi=600)
plt.clf()








print('Minimalny pocet platnych dat v roku 2019 je:'+ str(np.nanmin((pocet_platnych_dat_2019)*maska)))
print('Maximalny pocet platnych dat v roku 2019 je:'+ str(np.nanmax((pocet_platnych_dat_2019)*maska)))
print('Minimalny pocet platnych dat v roku 2020 je:'+ str(np.nanmin((pocet_platnych_dat_2020)*maska)))
print('Maximalny pocet platnych dat v roku 2020 je:'+ str(np.nanmax((pocet_platnych_dat_2020)*maska)))


#min max frakcie platnych dat



print('Minimalny rozdiel v platnych datach (2020-2019) je:'+ str(np.nanmin((pocet_platnych_dat_2020-pocet_platnych_dat_2019)*maska)))
print('Maximalny rozdiel v platnych datach (2020-2019) je:'+ str(np.nanmax((pocet_platnych_dat_2020-pocet_platnych_dat_2019)*maska)))
#min max frakcie platnych dat
print('Minimalna frakcia platnych dat v roku 2019 v % je:'+ str(np.nanmin((pocet_platnych_dat_2019/pocet_snimkov_2019)*100*maska)))
print('Maximalna frakcia platnych dat v roku 2019 v % je:'+ str(np.nanmax((pocet_platnych_dat_2019/pocet_snimkov_2019)*100*maska)))

print('Minimalna frakcia platnych dat v roku 2020 v % je:'+ str(np.nanmin((pocet_platnych_dat_2020/pocet_snimkov_2020)*100*maska)))
print('Maximalna frakcia platnych dat v roku 2020 v % je:'+ str(np.nanmax((pocet_platnych_dat_2020/pocet_snimkov_2020)*100*maska)))







np.save('priemer_no2_2019',priemer_2019*maska)
np.save('priemer_no2_2020',priemer_2020*maska)
np.save('pocet_platnych_dat_2019',pocet_platnych_dat_2019*maska)
np.save('pocet_platnych_dat_2020',pocet_platnych_dat_2020*maska)