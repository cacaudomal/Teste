# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 17:52:16 2024

@author: tedea
"""

# -*- coding: utf-8 -*-
"""
Created on thus 29 15:31:44 2024
@author: Clara Castilho Oliveira
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import freqcol_0_6 as fc
import pyigrf_clara_0_6 as igrf
import conductivity0_9_5 as cond
#from pathlib import Path

import irinetcdf_02 as iri
import msise2Netcdf as msise



#====  Lendo Dados 
# IRI
namefileiri = "IRI.3D.2008001.nc"
iriteste = iri.irincdf(namefileiri)

# NRLMSISE
filenamemsise2 = "NRLMSIS2.0.3D.2008001.nc"
msisetest = msise.nrlmsisenetcdf(filenamemsise2)

# IGRF
resIGRF = "teste2024"
dado = igrf.IGRF(-80,-180,100,2008,resIGRF + '_2') #preciso garantir que estão nas mesmas coordenadas

#calcigrf = dado.calc_grid(intervalo_h = 20, lim_h = 500, intervalo_lat=10, lim_lat=90, intervalo_lon=20, lim_lon=180)
calcigrf = dado.get_grid(resIGRF + '_2' + "_grid.csv")

dado.Dfgrid['Longitude'] = 180 + dado.Dfgrid['Longitude'] #so it will be from 0 to 360 instead
dado.Dfgrid = dado.going_to_multiindex(dado.Dfgrid)
dado.Dfgrid.index.names = ['ht','lat','lon'] #putting the same index names as the rest of the data to allow join operations

#==== Calculating Conductivities
#= Calculating colision frequencies
freqc = fc.freqcol(msisetest.msise.data["N2"],
            msisetest.msise.data["O2"],
            msisetest.msise.data["O"],
            iriteste.iridata.data['Te'],
            iriteste.iridata.data['Tn'],
            iriteste.iridata.data['Ti'])

#= Calculating Angular Gyrofrequency
gyrofreq = cond.gyrofrequency(dado.Dfgrid["B(T)"])

#= Calculating Relative Contruibution Parammeter
conductivity = cond.condiono_adachi()

conductivity.calc_prelativa_all(iriteste.iridata.data["O+"],
                        iriteste.iridata.data["NO+"],
                        iriteste.iridata.data["O2+"],
                        iriteste.iridata.data["Ne"])

#Alining Data by putting everything in a same Data Frame
conductivity.calcvaluesdf = gyrofreq.result.join(freqc.resul.copy(),
                          how = 'inner') #inner para ficarem só as coordenadas que ambos dataframes tem

#= Ordering multiindex
conductivity.calcvaluesdf = conductivity.calcvaluesdf.reset_index().sort_values(['time','ht','lat','lon']).set_index(['time','ht','lat','lon'])


#= Calculating Hall and Pedersen Conductivities
# Hall
conductivity.calc_Hall(conductivity.calcvaluesdf["fen"],
                       conductivity.calcvaluesdf["fin1"],
                       conductivity.calcvaluesdf["fin2"], 
                       conductivity.calcvaluesdf['wi1'],
                       conductivity.calcvaluesdf['wi2'],
                       conductivity.calcvaluesdf['we'],
                       conductivity.p1,
                       conductivity.p2,
                       iriteste.iridata.data['Ne'],
                       dado.Dfgrid["B(T)"]).dropna()

#the igrf data keeps pulling the time index to the deeper level gotta beware of 
#that when plotting

# Pedersen
conductivity.calc_Pedersen(conductivity.calcvaluesdf["fen"],
                       conductivity.calcvaluesdf["fin1"],
                       conductivity.calcvaluesdf["fin2"], 
                       conductivity.calcvaluesdf['wi1'],
                       conductivity.calcvaluesdf['wi2'],
                       conductivity.calcvaluesdf['we'],
                       conductivity.p1,
                       conductivity.p2,
                       iriteste.iridata.data['Ne'],
                       dado.Dfgrid["B(T)"]).dropna()

#==== Plotting

when = 0 
h = 100
#gyrofreq.plot_gyrmap(gyrofreq.result,h=h, localscope=True, savemap = True,filename="gyrofrequency_clara_teste")

conductivity.plot_2dgrid(conductivity.CondH.loc[:,:,:,'0 days 00:00:00'].dropna(),h,'Hall Conductivity at ' + str(h) + " km altitude\n" )
conductivity.plot_2dgrid(conductivity.CondP.loc[:,:,:,'0 days 00:00:00'].dropna(),h,'Pedersen Conductivity at ' + str(h) + " km altitude\n" )