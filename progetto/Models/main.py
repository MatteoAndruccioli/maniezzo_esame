import os, sys
import numpy as np
import random as rnd
import forecastByMLP as mlp
import forecastProcessing 
import pso
import pandas as pd
import json

returnWeight = 0.8
riskWeight = 0.2

def printJSON(dictionaryToPrint, fileName):
    with open('../pythonDir/risultati/'+fileName+'.json', 'w', encoding='utf-8') as f:
        json.dump(dictionaryToPrint, f, ensure_ascii=False, indent=4)

def stampAllInfo(portfolioKeys, resPSO, additionalInfo):
    data = {}
    data["horizon"] = "12"
    for i in range(len(portfolioKeys)):
        data[portfolioKeys[i]] = resPSO["xsolbest"][i]
    # ho preparato il file che interessa al prof ora lo stampo nel file "portfolio"
    printJSON(data, "portfolio")
    data2 = {}
    data2.update(data)
    # aggiungo altri dati di interesse e li stampo full_result
    data2["media_mobile_fitbest"] = resPSO["media_mobile"]
    data2["stdev_fitbest"] = resPSO["stdev"]
    data2["fitbest"] = resPSO["fitbest"]
    data2["returnWeight"] = returnWeight
    data2["riskWeight"] = riskWeight
    data2.update(additionalInfo)
    printJSON(data2, "full_result")
    return data


# permette creare un portfolio (dictionary con coppie (nome_indice, percentuale)) 
def computePortfolio(position, portfolioKeys): 
    portfolio = {}
    for i in range(len(portfolioKeys)):
        portfolio[portfolioKeys[i]] = position[i]
    return portfolio

def compute_fitness(position, processor, portfolioKeys):
    portfolio = computePortfolio(position, portfolioKeys)
    mm_stdev = processor.compute(portfolio)
    media_mobile = mm_stdev["returnMediaMobile"]
    risk = mm_stdev["stdev"]
    #return (returnWeight*media_mobile)+(riskWeight*(1/risk))
    print("fitness: {0}".format((returnWeight*media_mobile)-(riskWeight*risk*100)))
    return {
        "fitness" : (returnWeight*media_mobile)-(riskWeight*risk*100), #moltiplico per 100 per far si che risk abbia lo stesso ordine di grandezza di returnWeight
        "media_mobile" : media_mobile,
        "risk" : risk
    }


def goPSO(processor, portfolioKeys):
    resPSO = -np.inf # è il risultato, siccome vuole minimizzare, lo fissa ad un valore altissimo (infinito) così poi può solo calare
    
    niter = 100 # numero di iterazioni che deve compiere PSO
    popsize = 50 # numero di particelle
    nhood_size = 10 # n° particelle di neighborhood per lbest
    
    # alcuni valori che caratterizzano i vincoli sulle dimensioni
    numvar = 7 # n° di dimensioni, nel nostro caso saranno 7
    xmin = 0.05 # valore minimo che può assumere una dimensione
    xmax = 0.70 # valore massimo che può assumere una dimensione
    
    toPrint = {}
    toPrint.update({ "niter" : niter, "popsize": popsize, "nhood_size": nhood_size })
        
    # runna algoritmo di ottimizzazione 
    PSO = pso.ParSwarmOpt(xmin,xmax, processor, portfolioKeys) # istanzio la classe ParSwarmOpt (permette di effettuare il calcolo)
    resPSO = PSO.pso_solve(popsize, numvar, niter, nhood_size) # lancio algoritmo di pso
    toRet = stampAllInfo(portfolioKeys, resPSO, toPrint)
    return toRet;

# andamentoEconomico.csv FTSE_MIB_.csv MSCI_EM.csv MSCI_EURO.csv SP_500.csv All_Bonds.csv GOLD_SPOT.csv US_Treasury.csv

if __name__ == "__main__": 
    # cambia working directory to script path
   abspath = os.path.abspath(__file__)
   dname = os.path.dirname(abspath)
   os.chdir(dname)
   
   # stampo info sugli argomenti passati da chi chiama lo script
   print('MAPE Number of arguments:', len(sys.argv)) # Scrive la lunghezza del vettore degli argomenti (argv).
   print('MAPE Argument List:', str(sys.argv), 'andamentoEconomico:',sys.argv[1])   

   # dictionary contenente le previsioni nella forma di array(n,)
   #forecastedData = getDataFromCsv(sys.argv[1:len(sys.argv)]) 
   forecastedData = mlp.makePrevisions(sys.argv[1:len(sys.argv)]) 
   
   reshapedForecastedData = {}
   portfolioKeys = []
   for e in forecastedData.keys() : 
       # faccio un reshape del dictionary forecastedData perchè la classe processing lavora su un dictionary contenente array(n,1)
       reshapedForecastedData[e] = forecastedData[e].reshape(len(forecastedData[e]),1)
       # riempio portfolioKeys
       portfolioKeys.append(e)
   
   # inizializzo l'oggetto che processerà i dati di previsione
   ammontare_portafoglio = 100000 #euro investiti al day1 
   nValoriInMediaMobile = 20
   processor = forecastProcessing.ForecastsProcessor(ammontare_portafoglio, nValoriInMediaMobile, reshapedForecastedData)
   
   indexedDataDiff = processor.getIndexedDataDiff()
   
   res = goPSO(processor, portfolioKeys)
   





