#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 11 11:31:28 2021

@author: OMKO459
"""


import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt


plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = 20,8

df19=pd.read_csv('/data/karol/diplomovka/no2_velka_tabulka_2019.csv')
df20=pd.read_csv('/data/karol/diplomovka/no2_velka_tabulka_2020.csv')

df19['Datetime'] = pd.to_datetime(df19['Datumy'])
df19 = df19.set_index(['Datetime'])
df19=df19.drop(columns=['Datumy', 'Unnamed: 0'])
df19=df19.replace('--', np.nan)

df20['Datetime'] = pd.to_datetime(df20['Datumy'])
df20 = df20.set_index(['Datetime'])
df20=df20.drop(columns=['Datumy', 'Unnamed: 0'])
df20=df20.replace('--', np.nan)

# df19.to_csv('no2_velka_tabulka_2019_index_datum.csv')
# df20.to_csv('no2_velka_tabulka_2020_index_datum.csv')

