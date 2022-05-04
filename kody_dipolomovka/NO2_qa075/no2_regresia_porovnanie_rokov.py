#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 13:16:30 2021

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


dataset_2019=netCDF4.Dataset('/data/oko/dusan/sentinel5P/no2/2019/post_data/no2_trop_grid.nc')
lon_2019= dataset_2019.variables['lon'][:,:]
lat_2019= dataset_2019.variables['lat'][:,:]
 
regresia_19=np.load('/data/karol/diplomovka/regresne_pole_2019.npy')
regresia_20=np.load('/data/karol/diplomovka/regresne_pole_2020.npy')


b=mapb.pcolormesh(lon_2019,lat_2019,regresia_20-regresia_19,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='$\mu$g.$m^{-3}$')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Rozdiel: (2020-2019)') 
#plt.show()
plt.savefig('Prízemné koncentrácie (2020-2019).png' ,bbox_inches='tight',dpi=600)
plt.clf()

b=mapb.pcolormesh(lon_2019,lat_2019,((regresia_20-regresia_19)/regresia_19)*100,cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='%')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('((2020-2019)/2019)*100%') 
#plt.show()
plt.savefig('Prízemné koncentrácie relativna zmena (2019-2019).png' ,bbox_inches='tight',dpi=600)
plt.clf()
