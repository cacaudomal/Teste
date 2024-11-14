# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 17:28:22 2024

@author: tedea
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 16:03:34 2022

@author: Clara Castilho Oliveira

 Dependencies: 
 -------------
     : matplotlib, pandas
     
"""

import matplotlib.pyplot as plt
import pandas as pd
import read_netcdf_01 as rn   
        
class irincdf():
    def __init__(self,filename):
        self.iridata = self._read(filename) 
        pass
    
    def _read(self,filename):
        #d = {}
        #for i in ["O+","N+","H+","He+","O2+","NO+","Ne","Tn","Ti","Te"]:
        self.d = rn.basencdf(filename)

        return self.d
    
    def plot_densidade_e(self, ne, h, data=""):
        """
        FUNÇÃO PARA PLOTAR A DENSIDADE DE ELÉTRONS COM A ALTURA.

        Parameters
        ----------
        ne : PANDA SERIES - FLOATS
            DESCRIPTION.
        h : PANDA SERIES
            DESCRIPTION.
        data : STRING, optional
            DATA PARA O QUAL O DADO FOI ADQUIRIDO. The default is "".

        Returns
        -------
        None.

        """
        plt.figure(figsize=(5,5))
        plt.plot(ne,h,label = "$N_e$ "+data)
        plt.xlabel("Densidade de elétrons ($m^{-3}$)")
        plt.ylabel("Altura (km)")
       
        plt.title("Densidade de elétrons \n " + data)
        
        #plt.xlim(left=10e5)
        plt.legend()
        plt.grid()
        #$plt.xscale('log',base=10)
       
        plt.show()
        