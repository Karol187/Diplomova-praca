#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 08:41:23 2021

@author: OMKO459
"""

import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
%matplotlib inline
df=pd.read_csv('no2_velka_tabulka_2020_index_datum.csv')
df['Datetime']=pd.to_datetime(df['Datetime'])
df = df.set_index(['Datetime'])
df = df.rename(columns=lambda x: x.replace('Hodnoty ', ''))
df_all=df.between_time('10:00:00', '13:00:00').count().to_frame(name='cely cas')
df_sort_1=df.between_time('10:00:00', '10:30:00').count().to_frame(name='10:00-10:30')
df_sort_2=df.between_time('10:30:00', '11:00:00').count().to_frame(name='10:30-11:00')
df_sort_3=df.between_time('11:00:00', '11:30:00').count().to_frame(name='11:00-11:30')
df_sort_4=df.between_time('11:30:00', '12:00:00').count().to_frame(name='11:30-12:00')
df_sort_5=df.between_time('12:00:00', '12:30:00').count().to_frame(name='12:00-12:30')
df_sort_6=df.between_time('12:30:00', '13:00:00').count().to_frame(name='12:30-13:00')
Zoznam=[]
for i in (df_sort_1,df_sort_2,df_sort_3,df_sort_4,df_sort_5,df_sort_6):
    Zoznam.append(i)
DF=pd.concat(Zoznam,axis=1)
DFT=DF.T
DFTUT=DFT.drop(columns=['Bratislava, Mamateyova', 'Stará Lesná, AÚ SAV, EMEP','Topoľníky, Aszód, EMEP','Ružomberok, Riadok','Žilina, Obežná','Jelšava, Jesenského','Humenné, Nám. slobody','Bratislava, Jeséniova','Prievidza, Malonecpalská','Nitra, Janíkovce','Banská Bystrica, Zelená','Kojšovská hoľa','Gánovce, Meteo. st.','Starina, Vodná nádrž, EMEP','Chopok, EMEP'])
DFTUT.plot.bar()
plt.legend(bbox_to_anchor=(1.0, 1.0))
plt.xticks(rotation='vertical')
plt.title('Počet dát nad UT stanicami, (rok 2020)')
plt.xlabel('Čas')
plt.ylabel('Počet dát')
plt.savefig('pocet_dat_UT_stanice_2020',bbox_inches='tight',dpi=600)
plt.clf()

DFTUB=DFT.drop(columns=['Bratislava, Jeséniova','Bratislava, Trnavské Mýto','Martin, Jesenského','Trnava, Kollárova','Trenčín, Hasičská','Banská Bystrica,Štefánik. náb.','Malacky, Mierové námestie','Prešov, arm. gen. L. Svobodu','Košice, Štefánikova','Nitra, Štúrova','Stará Lesná, AÚ SAV, EMEP','Topoľníky, Aszód, EMEP','Kojšovská hoľa','Gánovce, Meteo. st.','Starina, Vodná nádrž, EMEP','Chopok, EMEP'])
DFTUB.plot.bar()
plt.legend(bbox_to_anchor=(1.0, 1.0))
plt.xticks(rotation='vertical')
plt.xticks(rotation='vertical')
plt.title('Počet dát nad UB stanicami, (rok 2020)')
plt.xlabel('Čas')
plt.ylabel('Počet dát')
plt.savefig('pocet_dat_UB_stanice_2020',bbox_inches='tight',dpi=600)
plt.clf()

DFTRB=DFT.drop(columns=['Bratislava, Mamateyova','Ružomberok, Riadok','Žilina, Obežná','Jelšava, Jesenského','Humenné, Nám. slobody','Bratislava, Jeséniova','Prievidza, Malonecpalská','Nitra, Janíkovce','Banská Bystrica, Zelená','Bratislava, Trnavské Mýto','Martin, Jesenského','Trnava, Kollárova','Trenčín, Hasičská','Banská Bystrica,Štefánik. náb.','Malacky, Mierové námestie','Prešov, arm. gen. L. Svobodu','Košice, Štefánikova','Nitra, Štúrova'])
DFTRB.plot.bar()
plt.legend(bbox_to_anchor=(1.0, 1.0))
plt.xticks(rotation='vertical')
plt.xticks(rotation='vertical')
plt.title('Počet dát nad RB stanicami, (rok 2020)')
plt.xlabel('Čas')
plt.ylabel('Počet dát')
plt.savefig('pocet_dat_RB_stanice_2020',bbox_inches='tight',dpi=600)
plt.clf()
