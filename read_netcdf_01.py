# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 17:17:43 2024

@author: Clara Castilho Oliveira
"""

import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd


#filename = "IRI.3D.2008001.nc"
#time = '0 days 00:00:00'
def get_data(filename):
    '''Read the file and convert its values from netcdf to pandas dataframe.

    Parameters
    ----------
    filename : STRING
        NAME OF THE FILE WITH THE DATA.
    name_vars : STRING LIST
        WHICH VARIABLES TO TAKE FROM DE FILE.

    Return
    -------
    data : DATAFRAME
        CONTAIN THE VARIABLES VALUES.

    '''
    with xr.open_dataset(filename) as f:
        #print("variables",f.variables) #getting info about variables measuring units
        data = f.to_dataframe() #getting all variables
        # sst variable
        
        #print("attr",f.attrs)
        #print(f.data_vars)
        #print(f.variables.keys()) # get all variable names
        #attrs = f.variables
    #convert from netcdf to dataframe
    #data = data.to_dataframe()
    
    return data#,attrs

def get_measuringunit(filename,name_vars):
    '''
    returns dict with name and measuring unit of the chosen variable

    Parameters
    ----------
    filename : STRING
        DESCRIPTION.
    name_vars : STRING
        DESCRIPTION.

    Return
    -------
    data : DICTIONARY
        DESCRIPTION.

    '''
    with xr.open_dataset(filename) as f:
        data = {i : f[i].attrs for i in name_vars} #getting info about name_vars measuring units    
    #print(data)
    
    return data

def pltcontour_data(data,variable,time,heigth):    
    varplot = data.loc[time,heigth,:,:].reset_index()
    
    fig,ax = plt.subplots(figsize=(8,5))
    
    ax.set_title("Density map of "+ variable +" in 2008")
    ax.set_ylabel("Latitude")
    ax.set_xlabel("Longitude")

    ax.grid(visible = True, alpha = 0.5)
     
    #  #plota o mapa de contornos
    #  #mudar cor das linhas
    a = ax.tricontourf(varplot["lon"],varplot["lat"],varplot[variable],15) 
    
    fig.colorbar(a,ax=ax,label="density of " + variable)
   
    plt.show() 

    
#======================================================    
class basencdf():
    """Class for reading de .nc file
    Data shape:
        

    """
    def __init__(self,filename):
        self.data = get_data(filename)
        
        #unitname = self.data.columns.to_list()
        self.munit = get_measuringunit(filename,self.data.columns.to_list())
        
    def __str__(self):
        return f'Unidedades: "{self.munit}"\n Dados \n\n {self.data}'
        #self.unitname = unitname
        
        
#a = basencdf('IRI.3D.2008001.nc')       
        
        
        