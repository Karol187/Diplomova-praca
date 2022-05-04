#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 20:36:22 2022

@author: OMKO459
"""

import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.basemap import Basemap

dataset_2019=netCDF4.Dataset('/data/oko/dusan/sentinel5P/no2/2019qa05/post_data/tropospheric_no2.nc')
lon_2019= dataset_2019.variables['lon'][:,:]
lat_2019= dataset_2019.variables['lat'][:,:]



plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = 20,8
mapb=Basemap(projection='lcc',lat_1=46.24470138549805,lat_2=46.24470138549805,lat_0=48.66,lon_0=19.7,width=432780,height=216351,resolution='h')
Trop2019qa075=np.load('/data/karol/diplomovka/priemer_no2_2019.npy')
Trop2020qa075=np.load('/data/karol/diplomovka/priemer_no2_2020.npy')
Trop2019qa05=np.load('/data/karol/diplomovka_no2_qavalue_05/priemer_no2_2019.npy')
Trop2020qa05=np.load('/data/karol/diplomovka_no2_qavalue_05/priemer_no2_2020.npy')

Percentualny_rozdiel_2019=((Trop2019qa05-Trop2019qa075)/Trop2019qa075)*100
Percentualny_rozdiel_2020=((Trop2020qa05-Trop2020qa075)/Trop2020qa075)*100

b=mapb.pcolormesh(lon_2019,lat_2019,Percentualny_rozdiel_2019,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='%')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Pokles resp. rast [%] troposférického stĺpca NO$_2$ pre prahové hodnoty qa=0.5 oproti qa=0.75 za rok 2019')
plt.clim(-2,85)
plt.savefig('Pokles resp. rast [%] troposférického stĺpca NO$_2$ pre prahové hodnoty qa=0.5 oproti qa=0.75 za rok 2019.png',bbox_inches='tight',dpi=600)
plt.clf()

b=mapb.pcolormesh(lon_2019,lat_2019,Percentualny_rozdiel_2020,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='%')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Pokles resp. rast [%] troposférického stĺpca NO$_2$ pre prahové hodnoty qa=0.5 oproti qa=0.75 za rok 2020')
plt.clim(-2,85)
plt.savefig('Pokles resp. rast [%] troposférického stĺpca NO$_2$ pre prahové hodnoty qa=0.5 oproti qa=0.75 za rok 2020.png',bbox_inches='tight',dpi=600)
plt.clf()

print('Minimalny rozdiel v roku 2019 je:'+ str(np.nanmin((Percentualny_rozdiel_2019))))
print('Maximalny rozdiel v roku 2019 je:'+ str(np.nanmax((Percentualny_rozdiel_2019))))
print('Minimalny rozdiel v roku 2020 je:'+ str(np.nanmin((Percentualny_rozdiel_2020))))
print('Maximalny rozdiel v roku 2020 je:'+ str(np.nanmax((Percentualny_rozdiel_2020))))
