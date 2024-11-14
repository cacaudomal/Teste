# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 11:42:46 2023

@author: Clara Castilho Oliveira


 Dependencies: 
 -------------
     : numpy, scipy, matplotlib, pandas, pathlib, nrlmsise2, iri2, freqcol
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

#import pyigrf_clara_0_4 as igrf
import freqcol_0_6 as fc
import geopandas as gpd
#import msise2
#import iri2_0_4 as iri

class gyrofrequency():
    def __init__(self,B):
        self.me = 9.109389e-31 #Massa do elétron em repouso [kg]
        self.mi1 = 5.065e-26 #Massa do íon 1 uma mistura de NO+ (75%) e O2+ (25%) (30.5 u.m.a.) [kg]
        self.mi2 = 2.657e-26 #Massa do íon 2 (O+) [kg] (16 a.m.u)
        self.e = -1.602177e-19 #Carga do elétron [C]

        self.result = self.calc_all_girofreq(B)
        
        
    def calc_girofreq(self,mi,B):
        """
        Funcao para cálculo da girofrequência ou frequência de ciclotron da
        partícula num ponto.
        
        Parameters
        ----------
        B : FLOAT
            campo magnético em [T]
        mi : FLOAT
            massa do íon ou do elétron [kg]    
        q : FLOAT
            carga do íon/elétron [C]
        
        Returns:
        ----------
        wi : FLOAT
            girofrequencia [Hz]
            
        """
        wi = np.sqrt(self.e**2) * np.sqrt(B**2)/mi
        
        return wi 
    
    
    def _prepplot_2dgrid(self,values,h):
        '''
        PREPARES DATA FOR PLOTTING IN 2D SURFACE.

        Parameters
        ----------
        values : DATA FRAME
            DESCRIPTION.
        h : FLOAT
            DESCRIPTION.

        Returns
        -------
        X : TYPE
            DESCRIPTION.
        Y : TYPE
            DESCRIPTION.
        value2dformat : TYPE
            DESCRIPTION.

        '''
        values_plot = values.loc[h].reset_index() #leaving the multindex to use normal indexing
        
        X,Y = np.meshgrid(values_plot['lon'].unique() - 180,values_plot['lat'].unique())
    
        value2dformat = pd.DataFrame([])
        for i in values_plot['lon'].unique():
            value2dformat[i] = values.loc[h,:,i]
            #print('\n\n i',i,'\nvalues2dformat[i]\n',value2dformat[i],'\n\n values.loc[]',values.loc[h,:,i])
            
        return X,Y,value2dformat
    
    
    def calc_all_girofreq(self,B) -> pd.DataFrame:        
        print("calculando as freqcol all: start ")
        wi1 = self.calc_girofreq(self.mi1, B)
        wi2 = self.calc_girofreq(self.mi2, B)
        we = self.calc_girofreq(self.me, B)
        #print("\n\ncondiono_adachi calc_all_girofreq  wi1: ",wi1,"\nwi2:",wi2,"\nwe5:",we)
        
        girofreq = pd.concat([we,wi1,wi2], axis=1, keys = ["we","wi1","wi2"])
        
        print("Done")
        
        return girofreq
   
          
    # def plot_gyrfreq(self,girofreq):
        
    #     #h = self.msise2.data["H(km)"]
        
    #     plt.figure(figsize=(5,5))

    #     #plt.plot(self.girofreq["we"],h,label="we")
    #     plt.plot(self.girofreq["wi1"],h,label="wi1")
    #     plt.plot(self.girofreq["wi2"],h,label="wi2")

    #     plt.title("girofrequencias com a altura (km)")
    #     plt.ylabel("Height (km)")
    #     plt.xlabel("$log_{10}$ Frequência de Ciclotron (Hz)")
    #     plt.legend()
    #     #plt.xscale('log')  

    #     plt.grid()
    #     plt.show()

    def plot_gyrmap(self,datatoplot, h, time=" ", localscope=True, savemap = False,filename="gyrofrequency"):
        """
        PLOTS GYROFREQUENCIES DATA ON A MAP.

        Parameters
        ----------
        datatoplot : DATAFRAME
            THE DATA FRAME CONTAINING THE CALCULATED GYROFREQUENCIES. IT SHOULD BE ALREADY FILTERED FOR A GIVEN MOMENT IN TIME.
        h : FLOAT
            Height in [km] for which the data is to be ploted.
        time : STRING, optional
            TIME IN WHICH THE DATA IS TO BE PLOTTED. The default is " ".
        localscope : BOOLEAN, optional
            SAYS WHETER THE DATA IS TO BE PLOTED AGAINST THE WHOLE MAP OR THE DATA'S BORDER. The default is True.
        savemap : BOOLEAN, optional
            WHETHER THE MAP IS TO BE SAVED OR NOT. The default is False.
        filename : STRING, optional
            NAME OF THE FILE TO WHICH THE IMAGE WILL BE SAVED. The default is "gyrofrequency".

        Returns
        -------
        None.

        """
        sizefig = (10,15)
        countries = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
        
        fig,ax = plt.subplots(3,1,figsize = sizefig, dpi = 300,layout = 'tight')
        fig.suptitle("Angular Gyrofrequency \nAltitude: "+str(h) + " km - Time: " + str(time))
        #fig.tight_layout()
        
        columns = ['we','wi1',
                   'wi2']
        
        titles = ['Electron',"Ion 1",'O+']
        
        for i in range(3):
            X,Y,values = self._prepplot_2dgrid(datatoplot[columns[i]],h)
            #print("\nvalues",values,"\nX",X,"\nY",Y)
            #print(values.columns.values.max())
            
            cntr = ax[i].contourf(X,Y,values,levels=10,cmap='jet')
            contour = ax[i].contour(X,Y,values,levels=10,colors='black', linewidths=0.5)
            plt.clabel(contour, inline = True, fontsize=8)
            
            ax[i].set_title(titles[i])
            ax[i].set_xlabel("Longitude")
            ax[i].set_ylabel("Latitude")
            ax[i].grid(visible = True, alpha = 0.5)
            
            countries.plot(ax = ax[i], color = "white",figsize = sizefig, alpha = 0.3)
            cbar = fig.colorbar(cntr, ax = ax[i], label = "Hz")
            
            if localscope==True:
                #putting map limits
                scopeaddtofilename="local"
                ax[i].set_xlim([values.columns.values.min()-180, values.columns.values.max()-180])
                ax[i].set_ylim([values.index.values.min(), values.index.values.max()])#gets smaller and bigger values of latitude from values rows name.
            else:
                scopeaddtofilename="global"
                pass
                
        if savemap == True:
            fig.savefig("plot_" + scopeaddtofilename +"_"+ str(filename) + str(h)+'km.png', dpi = 300, transparent=True)
            


class condiono_adachi():
    def __init__(self):
        self.me = 9.109389e-31 #Massa do elétron em repouso [kg]
        self.e = -1.602177e-19 #Carga do elétron [C]
        self.mi1 = 5.065e-26 #Massa do íon 1 uma mistura de NO+ (75%) e O2+ (25%) (30.5 u.m.a.) [kg]
        self.mi2 = 2.657e-26 #Massa do íon 2 (O+) [kg] (16 a.m.u)        
    
    def _calc_pRelativa(self,rhoi,ne):
        """
        Calcula a densidade numérica relativa da espécie ionica. Brekke (1993).
        
        Parameters
        ----------
        rhoi : PANDA SERIES FLOAT
            densidade do íon [m^-3]     
        ne : PANDA SERIES FLOAT
            Densidade de elétrons [elétrons/m^3]
        
        Returns:
        ----------
        pi : PANDA SERIES FLOAT
            densidade numérica relativa (Brekke,1983)
            
        """    
        pi = rhoi/ne        
        return pi
    
    
    def calc_prelativa_all(self, rho_íonO, rho_íonNO, rho_íonO2, ne):
        print("Calculating relative contribution parameters...")
        #self.rho1,self.rho2 = self.calc_rho_numion(rho_íonO,rho_íonNO,rho_íonO2,ne)
        rho1,rho2 = self.calc_rho_numion(rho_íonO,rho_íonNO,rho_íonO2,ne)

        self.p1 = self._calc_pRelativa(rho1, ne)
        self.p2 = self._calc_pRelativa(rho2, ne)
        print("Done")
        
        return self.p1,self.p2
           
    
    def calc_rho_numion(self,rho_íonO,rho_íonNO,rho_íonO2,ne):
        """
        Calcula a Densidade numérica dos íons O+ e fictício 1 (Brekke,1983).
        Razão entre o número de íons e o volume.
        
        Parameters
        ----------
        rho_íonO : LIST FLOAT
            concentração do íon O+ [%]

        rho_íonNO : LIST FLOAT
            concentração do íon NO+ [%]

        rho_íonO2 : LIST FLOAT
            concentração do íon O2+ [%]

        ne : LIST FLOAT
            Densidade de elétrons [elétrons/m^3]
        
        Returns:
        ----------
        rhoi1  : FLOAT
            densidade do íon fictício 1 [m^-3]
        rhoi2 : FLOAT
            densidade do íon O+ [m^-3]    
        """   
        #densidade do íon ficticio 1 [m^-3]
        rhoi1 = (rho_íonNO + rho_íonO2)/ne
        #print(self.h[i],"rho1",rhoi1,"m^-3")
    
        #densidade do íon O+ [m^-3]
        rhoi2 = rho_íonO/ne
        #print("rhoi2",rhoi2,"m^-3\n")
        return rhoi1, rhoi2
        
    
    def e(self,rhoN2,rhoO2,rhoO,Te,Tn,Ti,h):
        '''     
        CALCULA AS FREQUÊNCIAS DE COLISÃO.

        Parameters
        ----------
        rhoN2 : PANDA SERIES - FLOAT
           DENSITY OF N2 AT A GIVEN HEIGHT [m^3]
        rhoO2 : PANDA SERIES - FLOAT
            DENSITY OF O2 AT A GIVEN HEIGHT [m^3] 
        rhoO : PANDA SERIES - FLOAT
            DENSITY OF O AT A GIVEN HEIGHT [m^3] 
            
        Te : PANDA SERIES - FLOAT
            TEMPERATURA DOS ELÉTRONS [K].
        Ti : PANDA SERIES - FLOAT
            TEMPERATURA DOS ÍONS [K].
        Tn : PANDA SERIES - FLOAT
            TEMPERATURA DAS PARTÍCULAS NEUTRAS [K].

        Returns
        -------
            self.Freq : DATAFRAME
        '''
        a = fc.freqcol(rhoN2, rhoO2, rhoO, Te, Tn,Ti,h)
        self.Freq = a.calc_freq(h)
        #print("\n\Condutividade_0_7 - type freq : ",type(self.Freq),"\n")
        
        return self.Freq
        
    
    def calc_Hall(self,fen,fin1,fin2,wi1,wi2,we,p1,p2,ne,B):
        """
        CALCULA A CONDUTIVIDADE DE HALL APARTIR DAS EQUAÇÕES DE Adachi et al.
        Earth, Planets and Space (2017).

        Parameters
        ----------
        fen : PANDA SERIES
            frequência de colisão dos elétrons com as partículas neutras [Hz].
        fin1 : PANDA SERIES
            frequência de colisão do íon 1 com as partículas neutras [Hz].
        fin2 : PANDA SERIES
            frequência de colisão do íon 2 com as partículas neutras [Hz].
        wi1 : PANDA SERIES
            girofrequência do íon 1 [Hz].
        wi2 : PANDA SERIES
            girofrequência do íon 2 [Hz].
        we : PANDA SERIES
            girofrequência do elétron [Hz].
        p1 : TYPE
            DESCRIPTION.
        p2 : TYPE
            DESCRIPTION.
        ne : TYPE
            densidade de elétrons em [m^-3].
        B : TYPE
            intensidade do campo magnético da Terra [T].

        Returns
        -------
        self.condH : TYPE
            DESCRIPTION.

        """         
        print("\n== Calculando a Condutividade de Hall")
            
        a1 = (wi2**2)/(wi2**2 + fin2**2)
        b1 = (wi1**2)/(wi1**2 + fin1**2)
        c1 = (we**2)/(we**2 + fen**2)

        soma = c1 - (p1*b1) - (p2*a1)
        d = (ne * np.sqrt(self.e**2))/B

        self.CondH  = d * soma
        print("Done")
        return self.CondH   
            
    
    def calc_Pedersen(self,fen,fin1,fin2,wi1,wi2,we,p1,p2,ne,B):
        """
        CALCULA A CONDUTIVIDADE DE PEDERSEN APARTIR DAS EQUAÇÕES DE Adachi et al.
        Earth, Planets and Space (2017).

        Parameters
        ----------
        fen : PANDA SERIES
            frequência de colisão dos elétrons com as partículas neutras [Hz].
        fin1 : PANDA SERIES
            frequência de colisão do íon 1 com as partículas neutras [Hz].
        fin2 : PANDA SERIES
            frequência de colisão do íon O+ com as partículas neutras [Hz].
        wi1 : PANDA SERIES
            girofrequencia do íon 1 [Hz].
        wi2 : TYPE
            girofrequência do íon O+ [Hz].
        we : TYPE
            DESCRIPTION.
        p1 : TYPE
            DESCRIPTION.
        p2 : TYPE
            DESCRIPTION.
        ne : TYPE
            DESCRIPTION.
        B : TYPE
            DESCRIPTION.
        rho_íonNO : TYPE
            DESCRIPTION.

        Returns
        -------
        self.CondP : TYPE
            DESCRIPTION.

        """
        d = 0
        soma = 0
        
        print("\n== Calculando a condutividade de Pedersen")
        
        a1 = (wi2 * fin2)/(wi2**2 + fin2**2)
        b1 = (wi1 * fin1)/(wi1**2 + fin1**2)
        c1 = (we * fen)/(we**2 + fen**2)
            
        soma = c1 + p1 * b1 + p2 * a1
        d = (ne * np.sqrt(self.e**2))/B
        
        self.CondP = d * soma
        print("Done\n")
        
        return self.CondP
       
    def save_to_csv(data,filename):
        """
        SALVA OS DADOS GUARDADOS NUM DATAFRAME NUM ARQUIVO.
        
        parameters
        -------
        filename : STRING
            NAME, WITHOUT FILE TYPE, OF THE CREATED FILE.
            
        data : DATAFRAME
            VALORES CALCULADOS QUE SERÃO SALVOS NO ARQUIVO. 

        """
        data.to_csv(filename + ".csv",sep=",",header=True)
        print("condiono_0_9_5- _salva_dataframe : arquivo", filename," Salvo.\n")
           
    #======= Plotting functions
    
    def _prepplot_2dgrid(self,values,h):
        '''
        PREPARES DATA FOR PLOTTING IN 2D SURFACE.

        Parameters
        ----------
        values : DATA FRAME
            DESCRIPTION.
        h : FLOAT
            DESCRIPTION.

        Returns
        -------
        X : TYPE
            DESCRIPTION.
        Y : TYPE
            DESCRIPTION.
        value2dformat : TYPE
            DESCRIPTION.

        '''
        values_plot = values.loc[h].reset_index() #leaving the multindex to use normal indexing
        
        X,Y = np.meshgrid(values_plot['lon'].unique() - 180,values_plot['lat'].unique())
    
        value2dformat = pd.DataFrame([])
        for i in values_plot['lon'].unique():
            value2dformat[i] = values.loc[h,:,i]
            #print('\n\n i',i,'\nvalues2dformat[i]\n',value2dformat[i],'\n\n values.loc[]',values.loc[h,:,i])
            
        return X,Y,value2dformat
    
    # def prepplot_valueto2Dgrid(values,h):
    #     value2dformat = pd.DataFrame([])
    #     values_plot = values.loc[h].reset_index() #leaving the multindex to use normal indexing
        
    #     for i in values_plot['lon'].unique():
    #         value2dformat[i] = values.loc[h,:,i]
    #         #print('\n\n i',i,'\nvalues2dformat[i]\n',value2dformat[i],'\n\n values.loc[]',values.loc[h,:,i])
        
    #     return value2dformat

    # def prepplot_creat2Dgrid(values,h):
    #     values_plot = values.loc[h].reset_index() #leaving the multindex to use normal indexing
        
    #     X,Y = np.meshgrid(values_plot['lon'].unique() - 180, values_plot['lat'].unique())
        
    #     return X,Y
    
    def plot_2dgrid(self,values,h,title=" ") -> None:
        sizefig = (10,15)
        #values_plot = values.loc[h].reset_index() #leaving the multindex to use normal indexing
        countries = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    
        # X,Y = np.meshgrid(values_plot['lon'].unique() - 180,values_plot['lat'].unique())
    
        # value2dformat = pd.DataFrame([])
        # for i in values_plot['lon'].unique():
        #     value2dformat[i] = values.loc[h,:,i]
        
        X,Y,value2dformat = self._prepplot_2dgrid(values,h)
        
        fig, ax = plt.subplots()
        cntr = ax.contourf(X,Y,value2dformat,cmap="jet")
        contour = ax.contour(X,Y,value2dformat,colors='black', linewidths=0.5)
        ax.clabel(contour, inline = True, fontsize = 8)
    
        countries.plot(ax=ax,color = "white",figsize=sizefig, alpha = 0.4)
        
        ax.set_title(title)
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.set_xlim([-180, 160])
        ax.set_ylim([-80,80])
        ax.grid(visible = True, alpha = 0.5)
        
        fig.colorbar(cntr, ax=ax, label='conductivity [S/m]',location = 'bottom')

    # def plot_Hall(self):
    #     h = self.msise2.data["H(km)"]
    #     plt.figure(figsize=(5,5))
        
    #     condH = [self.CondH[i] * -1 for i in range(len(self.CondH))]
        
    #     plt.plot(condH,h)
    #     plt.xscale('log')
    #     plt.ylabel("Height (km)")
    #     plt.xlabel("$log_{10}$ Conductivity (S/m)",fontsize=15)
    #     #ax.legend(title="Hour")
    #     plt.title("Hall conductivity")
    #     plt.grid()  
        
    #     plt.show()
          
        
    # def plot_Pedersen(self):
    #     plt.figure(figsize=(5,5))
        
    #     plt.plot(self.CondP,self.msise2.data["H(km)"],label="Pedersen Conductivity")
       
    #     plt.xscale('log')

    #     plt.ylabel("Height (km)")
    #     plt.xlabel("$log_{10}$ Conductivity (S/m)",fontsize=15)
    #     plt.title("Pedersen conductivity")  
    #     plt.grid()  
        
    #     plt.show()

    # def plot_hfreqcol(self):
    #     h = self.Freq["H(km)"]
        
    #     plt.figure(figsize=(5,5))

    #     plt.plot(self.Freq["fen"],h,label="electron")
    #     plt.plot(self.Freq["fin1"],h,label="ficticious ion 1")
    #     plt.plot(self.Freq["fin2"],h,label="O+")
        
    #     plt.title('Collision Frequency')
    #     plt.xlabel("$log_{10}$ Collision Frequency (Hz)")
    #     plt.ylabel("Height (km)")
        
    #     plt.xscale('log')  

    #     plt.legend()
    #     plt.grid()
        
    #     plt.show()
