# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 02:37:17 2024


@author: tedea
"""

import read_netcdf_01 as rn

class nrlmsisenetcdf():
    '''Reads data from nrlmsise 2 model in NetCDF format'''
    def __init__(self,filename):
        self.msise = self._read(filename) 
        self._convert_cm3tom3()
        
    def _read(self,filename):
        d = rn.basencdf(filename)
        #print("_read msise2 type d: ",type(d))    
        return d
    
    def _convert_cm3tom3(self):
        for i in ["O","N2","O2","MASS","He","AR","AO","H","N"]:
            self.msise.data[i] = self.msise.data[i] * 1e6
            self.msise.munit[i]['units'] = self.msise.munit[i]['units'] + " * 1e6"
            #print(i,type(self.msise))
            
# a = nrlmsisenetcdf("NRLMSIS2.0.3D.2008001.nc")
# a.msise

# for i in ["O","N2","O2","MASS","NT","ET","He","AR","AO","H","N"]:
#      #print(a.msise[i].munit)
#      print('\n\n',a.msise[i].data.head)
#      a.msise[i].data.index

