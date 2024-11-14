# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 14:07:36 2021

@author: Clara Castilho Oliveira

Contains freqcol class.

 Dependencies: 
 -------------
     : numpy, matplotlib, pandas
     
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class freqcol():
    """
    Classe para calcular as frequências de colisão dadas segundo Adachi et. al. 2017.
    
    ...
    
    Dependencies: 
    -------------
        : numpy, matplotlib, pandas       
        
    Attributes
    ----------
    nN2 : LIST FLOAT
        densidade de N2, [m^3] NRLMSISE2
    nO2 : LIST FLOAT
        densidade de O2 [m^3] NRLMSISE2
    nO : LIST FLOAT
        densidade de O [m^3] NRLMSISE2    
    Ti : PANDA SERIES
        TEMPERATURA DOS ÍONS EM [K].
    Tn : PANDA SERIES
        TEMPERATURA DAS PARTÍCULAS NEUTRAS EM [K].
    h : PANDA SERIES
        ALTURAS NAS QUAIS OS VALORES SERÃO CALCULADOS [km].
        
    Methods
    ----------
        set_Temp(self,Te,Tn,Ti)
        set_Tr(self,Ti,Tn)
        set_atmNeutra(self,nN2,nO2,nO)
        calc_freq(self,h)
        calc_fen(self)
        plot_freq_h(self)
        
    """
    
    def __init__(self, nN2, nO2, nO,Te,Tn,Ti):        
        self.calc_freq(nN2, nO2, nO,Te,Tn,Ti)
    
    def calc_Tr(self,Ti,Tn):
        """
        CRIA UMA PANDA SERIE COM OS VALORES DA TEMPERATURA RELATIVA E PREENCHE SEUS VALORES.

        Parameters
        ----------
        Ti : PANDA SERIES
            TEMPERATURA DOS ÍONS EM [K].
        Tn : PANDA SERIES
            TEMPERATURA DAS PARTÍCULAS NEUTRAS EM [K].

        Returns
        -------
        None.

        """
        Tr = (Ti + Tn)/2  
        return Tr
        
        
    def calc_freq(self,nN2, nO2, nO,Te,Tn,Ti):
        """
        Cálculo das frequêncisa de colisão dos íon O+, ion 1 e elétrons com as partículas neutras.        
        Equações retiradas do trabalho de Adachi et. al, 2017.
    
        Parameters
        ----------
        h : DATAFRAME
            ALTURA PARA QUAL A FREQUÊNCIA DE COLISÃO SERÁ CALCULADA [km]
            
        Returns
        -------
            freqcol : DATAFRAME 
                UM DATAFRAME CUJAS COLUNAS SÃO RESPECTIVAMENTE:
                fen : frequência de colisão dos elétrons com as partículas neutras [Hz]
                fin1 : frequência de colisão do íon 1 com as partículas neutras [Hz]
                fin2 : frequência de colisão do íon 2 com as partículas neutras [Hz]
                H(km) : ALTURA PARA QUAL A FREQUÊNCIA DE COLISÃO FOI CALCULADA [km]
        """
        print('\nCalculating Collision Frequency...')
        Tr = self.calc_Tr(Ti,Tn)
        
        fen = self.calc_fen(nN2, nO2, nO, Te)
        #print("\n\nfreqcol fen : ",fen)
        
        fin1 = (4.29 * nN2 + 4.23 * nO2 + 2.41 * nO) * 1e-16
       # print("\n\nfreqcol fin1 : ",fin1)
        
        fin2 = 6.82e-16*nN2 + 6.66e-16*nO2 + 3.32e-17*nO * np.sqrt(Tr) * (1.08 - 0.139*np.log10(Tr) + 4.51e-3*(np.log10(Tr)**2))
        #print("\n\nfreqcol fin2 : ",fin2)
        
        #print("\n\ncalc_freq- fen:",type(fen))
        
        #print("\nFREQCOL - calc_freq- freqcol: ",self.freqcol)
        self.e = fen
        self.ion1 = fin1
        self.ion2 = fin2
        
        self.resul = pd.concat([fen,fin1,fin2], axis=1, keys=["fen","fin1","fin2"])
        
        print("Done")
        
        #return freqcol
        
    def calc_fen(self,nN2, nO2, nO,Te):
        fen = 2.33e-17 * nN2 * (1 - 1.21e-4*Te) * Te 
        + 1.82e-16 * nO2 * (1 + 3.6e-2*np.sqrt(Te)) * np.sqrt(Te) 
        + 8.9e-17*nO * (1 + 5.7e-4*Te) * np.sqrt(Te)
        #print("\n\nfreqcol fen : ",fen)
    
        return fen
    
    def calc_fin1(self,nN2, nO2, nO):
        fin1 = (4.29 * nN2 + 4.23 * nO2 + 2.41 * nO) * 1e-16
        #print("\n\nfreqcol fin1 : ",fin1)
        
        return fin1
    
    def calc_fin2(self,nN2, nO2, nO,Te,Tn,Ti):
        Tr = self.calc_Tr(Ti,Tn)
        
        fin2 = 6.82e-16*nN2 + 6.66e-16*nO2 + 3.32e-17*nO * np.sqrt(Tr) * (1.08 - 0.139*np.log10(Tr) + 4.51e-3*(np.log10(Tr)**2))
        #print("\n\nfreqcol fin2 : ",fin2)
        
        return fin2
    
    def plot_freq_h(self):
        """
        CRIA PERFIL DE ALTURA DAS FREQUÊNCIAS DE COLISÕES.

        Returns
        -------
        None.

        """
        fig,ax = plt.subplots()
        
        ax.semilogx(self.freqcol["fen"],self.freqcol["H(km)"],'-', label='fen (Hz)')
        ax.semilogx(self.freqcol["fin1"],self.freqcol["H(km)"],'-', label='fin1 (Hz)')
        ax.semilogx(self.freqcol["fin2"],self.freqcol["H(km)"],'-', label='fin2 (Hz)')
        
        ax.set_title("Frequências de Colisão")
        ax.set_xlabel("$log_{10}$ Frequência de Colisão ($Hz$)")
        ax.set_ylabel("Altura (km)")
        
        ax.legend()
        ax.grid(True)
    
    
#======= TESTE ==========================
# filenameiri = "IRI.3D.2008001.nc"
# filenamemsise = "NRLMSIS2.0.3D.2008001.nc"

# iri1 = iri.irincdf(filenameiri)
# msise = msise2.nrlmsisenetcdf(filenamemsise)

# lat = 35
# lon = 125
# time = '0 days 00:00:00'


# nomearqMSISE = "nrlmsise_lat69_lon19_z300_s5_data30MAR2012_h6UT.txt"
# nomearqIRI = "IRI2016_lat69_lon19_z300_s5_data30MAR2012_h6UT.txt"

# tmsise = msise2.nrlmsise(nomearqMSISE)
# tiri = iri.iri(nomearqIRI)

# freq = freqcol(tmsise.dado["N2 (m-3)"], tmsise.dado["O2 (m-3)"], tmsise.dado["O (m-3)"], tiri.dado["Te/K"], tiri.dado["Tn/K"], tiri.dado["Ti/K"],tiri.dado["H(km)"])

