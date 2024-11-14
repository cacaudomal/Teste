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
import freqcol_0_5 as fc
#import msise2
#import iri2_0_4 as iri


class condiono_adachi():
    def __init__(self):
        self.me = 9.109389e-31 #Massa do elétron em repouso [kg]
        self.e = -1.602177e-19 #Carga do elétron [C]
        self.mi1 = 5.065e-26 #Massa do íon 1 uma mistura de NO+ (75%) e O2+ (25%) (30.5 u.m.a.) [kg]
        self.mi2 = 2.657e-26 #Massa do íon 2 (O+) [kg] (16 a.m.u)
        
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
    
    def calc_all_girofreq(self,B):
        girofreq = pd.DataFrame(columns = ["wi1","wi2","we"])
        
        print("calculando as freqcol all: start ")
        wi1 = self.calc_girofreq(self.mi1, B)
        wi2 = self.calc_girofreq(self.mi2, B)
        we = self.calc_girofreq(self.me, B)
        #print("\n\ncondiono_adachi calc_all_girofreq  wi1: ",wi1,"\nwi2:",wi2,"\nwe5:",we)
        
        self.agirofreq = pd.concat([we,wi1,wi2], axis=1, keys = ["we","wi1","wi2"])
        
        # girofreq["wi1"] = wi1
        # girofreq["wi2"] = wi2
        # girofreq["we"] = we
        
        print("Done")
        
        return self.agirofreq
        
    
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
    
    
    def calc_prelativa_all(self,rho_íonO,rho_íonNO,rho_íonO2,ne):
        self.rho1,self.rho2 = self.calc_rho_numion(rho_íonO,rho_íonNO,rho_íonO2,ne)
        
        self.p1 = self._calc_pRelativa(self.rho1, ne)
        self.p2 = self._calc_pRelativa(self.rho2, ne)
        
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
        
    
    def calc_freqcol(self,rhoN2,rhoO2,rhoO,Te,Tn,Ti,h):
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
        print("Calculando a Condutividade de Hall")
            
        a1 = (wi2**2)/(wi2**2 + fin2**2)
        b1 = (wi1**2)/(wi1**2 + fin1**2)
        c1 = (we**2)/(we**2 + fen**2)

        soma = c1 - (p1*b1) - (p2*a1)
        d = (ne * self.e)/B

        self.CondH  = d * soma
        
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
        
        print("===== Calculando a condutividade de Pedersen =====")
        
        a1 = (wi2 * fin2)/(wi2**2 + fin2**2)
        b1 = (wi1 * fin1)/(wi1**2 + fin1**2)
        c1 = (we * fen)/(we**2 + fen**2)
            
        soma = c1 + p1 * b1 + p2 * a1
        d = (ne * np.sqrt(self.e**2))/B
        
        self.CondP = d * soma
        
        return self.CondP
       
#======= Plotting functions        

    def plot_Hall(self):
        h = self.msise2.data["H(km)"]
        plt.figure(figsize=(5,5))
        
        condH = [self.CondH[i] * -1 for i in range(len(self.CondH))]
        
        plt.plot(condH,h)
        plt.xscale('log')
        plt.ylabel("Height (km)")
        plt.xlabel("$log_{10}$ Conductivity (S/m)",fontsize=15)
        #ax.legend(title="Hour")
        plt.title("Hall conductivity")
        plt.grid()  
        
        plt.show()
          
        
    def plot_Pedersen(self):
        plt.figure(figsize=(5,5))
        
        plt.plot(self.CondP,self.msise2.data["H(km)"],label="Pedersen Conductivity")
       
        plt.xscale('log')

        plt.ylabel("Height (km)")
        plt.xlabel("$log_{10}$ Conductivity (S/m)",fontsize=15)
        plt.title("Pedersen conductivity")  
        plt.grid()  
        
        plt.show()
           
        
    def plot_girofreq(self):
        
        h = self.msise2.data["H(km)"]
        
        plt.figure(figsize=(5,5))

        #plt.plot(self.girofreq["we"],h,label="we")
        plt.plot(self.girofreq["wi1"],h,label="wi1")
        plt.plot(self.girofreq["wi2"],h,label="wi2")

        plt.title("girofrequencias com a altura (km)")
        plt.ylabel("Height (km)")
        plt.xlabel("$log_{10}$ Frequência de Ciclotron (Hz)")
        plt.legend()
        #plt.xscale('log')  

        plt.grid()
        plt.show()


    def plot_freqcol(self):
        h = self.Freq["H(km)"]
        
        plt.figure(figsize=(5,5))

        plt.plot(self.Freq["fen"],h,label="electron")
        plt.plot(self.Freq["fin1"],h,label="ficticious ion 1")
        plt.plot(self.Freq["fin2"],h,label="O+")
        
        plt.title('Collision Frequency')
        plt.xlabel("$log_{10}$ Collision Frequency (Hz)")
        plt.ylabel("Height (km)")
        
        plt.xscale('log')  

        plt.legend()
        plt.grid()
        
        plt.show()
