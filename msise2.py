#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 16:17:20 2022

@author: Clara Castilho Oliveira

 Dependencies: 
 -------------
     : matplotlib, pandas
     
"""

import pandas as pd
import matplotlib.pyplot as plt
import read_netcdf as rn

class nrlmsise():
    def __init__(self,nome_arq):
        self._read_data(nome_arq)
        self._convert_cm3tom3()
    
    def _read_data(self,nomearq):
         """
         READ AND STORE TXT DATA FROM NRLMSISE2 IN A PANDAS DATAFRAME.
    
         Parameters
         ----------
         nomearq : STRING
             NAME OF THE FILE IN WHICH THE DATA IS KEPT
    
         """
         guarda_dado = []
         with open(nomearq,"r") as arq: 
             dado = arq.readlines() #le todas as linhas do arquivo
        
         for i in range(len(dado)):
             guarda_dado.append(dado[i].split())#separa os valores no string da linha pro seus próprios espaços
         
         dado_float = [list(map(float,i)) for i in guarda_dado]
         
         self.data = pd.DataFrame(dado_float, columns =  ["Year","Mon","Day","DOY","hour","H(km)","Lat","Lon","O (cm-3)","N2 (cm-3)","O2 (cm-3)","air(gm/cm3)","Tn(K)","exoT(K)","He (cm-3)","Ar (cm-3)","H (cm-3)","N (cm-3)","F107", "F107a","apdaily","ap0-3","ap3-6","ap6-9","ap9-12","ap12-33","ap33-59"])   

        
    def _convert_cm3tom3(self):
        for i in ("O (cm-3)","N2 (cm-3)","O2 (cm-3)","He (cm-3)","Ar (cm-3)","H (cm-3)","N (cm-3)"):
            #print("\n\nfora SI:\n",self.data[i])
            self.data[i] = self.data[i] * 1e6
            #print("\nno SI",self.data[i])
            
        self.data.columns = ["Year","Mon","Day","DOY","hour","H(km)","Lat","Lon","O (m-3)","N2 (m-3)","O2 (m-3)","air(gm/cm3)","Tn(K)","exoT(K)","He (m-3)","Ar (m-3)","H (m-3)","N (m-3)","F107", "F107a","apdaily","ap0-3","ap3-6","ap6-9","ap9-12","ap12-33","ap33-59"]
        
    def plot_concentration(self,data):
        #plt.figure(figsize=(5,5))
        H = data["H(km)"]
        lat = list(data["Lat"])
        lon = list(data["Lon"])
        hour = list(data["hour"])
        fig, ax = plt.subplots(figsize=(10, 5))
        
        ax.semilogx(data["O (m-3)"],H,'-', label='O')
        ax.semilogx(data["O2 (m-3)"],H,'-', label='$O_2$')
        ax.plot(data["N2 (m-3)"],H, label='$N_2$')
        ax.semilogx(data["H (m-3)"],H,'-', label='H')
        ax.semilogx(data["He (m-3)"],H,'-', label='He')
        #ax.semilogx(data["N (cm-3)"],data["Heigth(km)"],'-', label='N')
        ax.semilogx(data["Ar (m-3)"],H,'-', label='Ar')

        ax.set_title('Perfil da Composição da Atmosfera Neutra\n lat: ' +
                     str(lat[0]) +
                     " lon:" + str(lon[0]) +
                     " hour: " + str(hour[0]))
        
        ax.set_xlabel("$log_{10}$ Densidade ($m^{-3}$)")
        ax.set_ylabel("Altura (km)")
         
        #plt.xlim(left=10e2)
        
        ax.legend()
        ax.grid(True)
   
    
#======================================================        
        
class nrlmsisenetcdf():
    def __init__(self,filename):
        self.msise = self._read(filename) 
        self._convert_cm3tom3()
        
    def _read(self,filename):
        d = {}
        for i in ["O","N2","O2","MASS","NT","ET","He","AR","AO","H","N"]:
            d[i] = rn.basencdf(filename, i)
            
        return d
    
    def _convert_cm3tom3(self):
        for i in ["O","N2","O2","MASS","NT","ET","He","AR","AO","H","N"]:
            self.msise[i].data = self.msise[i].data*1e6
            self.msise[i].munit['units'] = self.msise[i].munit['units']+" * 1e6"
            

filename = "NRLMSIS2.0.3D.2008001.nc"    
a = nrlmsisenetcdf(filename)  
  
#nomearqMSISE = "NRLMSISE_lat69_lon19_z300_s5_data30MAR2012_h6UT.txt"
#msise = nrlmsise(nomearqMSISE)

#msise.plot_concentration(msise.data)
# msise.plot_concentracoes()

# nomearqMSISE = "NRLMSISE2_lat-25_lon125_z0_750_s_5data01JAN2000_h00LT.txt"
# msise_b =  nrlmsise(nomearqMSISE)
# msise_b.plot_concentracoes()

#print(a.data)