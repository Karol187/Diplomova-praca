#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 09:28:05 2021

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
#funkction which fidns ix and iy indexes of grid
def getclosest_ij(nlats,nlons,latpt,lonpt):
    # find squared distance of every point on grid
    dist_sq = (nlats-latpt)**2 + (nlons-lonpt)**2  
    # 1D index of minimum dist_sq element
    minindex_flattened = dist_sq.argmin()    
    # Get 2D index for latvals and lonvals arrays from 1D index
    return np.unravel_index(minindex_flattened, nlats.shape)
#########################
pole_priemerne_2019=np.load('/data/karol/diplomovka_no2_qavalue_05/priemer_no2_2019.npy')
pole_priemerne_2020=np.load('/data/karol/diplomovka_no2_qavalue_05/priemer_no2_2020.npy')
dataset_2019=netCDF4.Dataset('/data/oko/dusan/sentinel5P/no2/2019qa05/post_data/tropospheric_no2.nc')
dataset_2020=netCDF4.Dataset('/data/oko/dusan/sentinel5P/no2/2020qa05/post_data/no2_trop_grid.nc')
lon_2019= dataset_2019.variables['lon'][:,:]
lat_2019= dataset_2019.variables['lat'][:,:]
lon_2020= dataset_2020.variables['lon'][:,:]
lat_2020= dataset_2020.variables['lat'][:,:]



tabulka_2019=pd.read_csv('/data/karol/diplomovka/stanice_no2_2019_prizemne_koncentracie.csv')
tabulka_2020=pd.read_csv('/data/karol/diplomovka/stanice_no2_2020_prizemne_koncentracie.csv')

################################################################################


import numpy as np
x=[] #hodnoty v gridovom bode 
for i,row in tabulka_2019.iterrows():
    lat_x=row['lat_x']
    lon_x=row['lon_x']
    ix, iy = getclosest_ij(lat_2019,lon_2019,row['lat_x'],row['lon_x'])
    x.append(pole_priemerne_2019[ix,iy])
y=tabulka_2019['no2']
y=np.array([y])
x=np.array([x])
x=x[0,:]
y=y[0,:]
from sklearn.metrics import mean_squared_error

logfit_parameters = np.polyfit(np.log(x),y,1)
print(logfit_parameters)
yfit=logfit_parameters[0]*np.log(x)+logfit_parameters[1]
rsq=(np.corrcoef(np.log(x),y)[0,1])**2
print(rsq)
rmse = mean_squared_error(y, yfit, squared=False)
print(rmse)
plt.plot(x,y,'o')
xp = np.linspace(0,0.0001,1000)
plt.ylim(0,45)
plt.plot(xp,logfit_parameters[0]*np.log(xp)+logfit_parameters[1],'r--')
plt.xlabel('Priemerná ročná hodnota troposférického stĺpca [mol/$m^{2}$]')
plt.ylabel('Priemerná ročná koncentrácia [$\mu$g.$m^{-3}$] ')
plt.title('Logaritmická regresia, rok 2019, $R^{2}$ = '+str(rsq.round(3))+', RMSE = '+str(rmse.round(3)))

#plt.savefig('Logaritmicky fit, rok 2020.png' ,bbox_inches='tight',dpi=600)
plt.show()
#np.save('logaritmicka_predikcia_2020.npy',(logfit_parameters[0]*np.log(pole_priemerne_2020)+logfit_parameters[1]))
#plt.clf()

b=mapb.pcolormesh(lon_2019,lat_2019,(logfit_parameters[0]*np.log(pole_priemerne_2019)+logfit_parameters[1]),cmap=plt.cm.jet,latlon=True)
mapb.drawcountries(linewidth=3)
mapb.drawrivers()
cb=plt.colorbar(label='$\mu$g.$m^{-3}$')
font = matplotlib.font_manager.FontProperties( style='italic', size=16)
cb.ax.yaxis.label.set_font_properties(font)
plt.title('Prízemné koncentrácie za rok 2019 (logaritmická regresia)') 
plt.clim(0,45)

#plt.savefig('Prízemné koncentrácie za rok 2020 logaritmická regresia.png' ,bbox_inches='tight',dpi=600)
plt.show()
#plt.clf()

 