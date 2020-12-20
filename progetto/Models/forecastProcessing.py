import pandas as pd, numpy as np, os
import math

import pandas as pd, numpy as np, os
import math

'''
    Funzioni di utility
'''

# carica i dati dai csv in un dictionary
def getDataFromCsv(fileNames):
    dictionary = {}
    for value in fileNames:
        dictionary[value] = pd.read_csv('./IndiciPrevistiCsv/'+value).to_numpy()
    return dictionary


#funzione che restituisce un array di float64, ottenuti come differenza
def computeDiffArray(indexes):
    indexesDiff = []
    i = 1
    while i < len(indexes):
        indexesDiff.append(((indexes[i]-indexes[i-1])/indexes[i-1])[0])
        i = i+1
    return indexesDiff

# restituisce dictionary con tutti diff dei valori di indice
def computeIndexedDataDiff(allIndexValues):
    dictionary = {}
    for key in allIndexValues: 
        dictionary[key] = computeDiffArray(allIndexValues[key])
    return dictionary

# restituisce un vettore contenente il valore day by day del portfolio per uno specifico indice
def computeIndexPortfolioValueDayByDay(indexDiffs, percentage, totAmount):
    dayByDayValues = []
    dayByDayValues.append(totAmount*percentage)
    i = 1
    while i < len(indexDiffs):
        dayByDayValues.append((1+indexDiffs[i])*dayByDayValues[i-1])
        i = i+1
    return dayByDayValues

# restituisce un dizionario che associa ad ogni nomeFileCsv una lista dei valori assunti dall'investimento sui quei titoli finanziari
def computeDailyIndexedValues(allIndexDiff, portafoglio, totAmount):
    dictionary = {}
    for key in allIndexDiff: 
        dictionary[key] = computeIndexPortfolioValueDayByDay(allIndexDiff[key], portafoglio[key], totAmount)
    return dictionary

# restituisce un vettore che contiene i valore dell'ammontare investito day by day
def computePortfolioValues(allValoriDaily):
    valPort = []
    i = 0
    firstKey = list(allValoriDaily.keys())[0]
    while i < len(allValoriDaily[firstKey]):
        currentValSum = 0.0;   
        for key in allValoriDaily: 
            currentValSum = currentValSum + allValoriDaily[key][i] 
        valPort.append(currentValSum) 
        i = i+1
    return valPort

# restituisxe un vettore contenente la variazione normalizzata dei valori assunti dal portafoglio di investimenti nel tempo
def computePortfolioDiff(valPort):
    variazPort = []
    i = 1
    while i < len(valPort):
        variazPort.append((valPort[i]-valPort[i-1])/valPort[i-1]) 
        i = i+1
    return variazPort

# restituisce un vettore contenente i valori di media mobile assunti dal portafoglio nel tempo
def computeMovingAverage(values,nval):
    medie = []
    i = 0
    while (i+nval) <= len(values):
        medie.append(sum(values[i:(i+nval)])/nval) 
        i = i+1
    return medie

# calcola il valore dello scarto quadratico tra un valore del portfolio e il valore calcolato in media mobile
def computeSquaredError(values, mediaMobile):
    sqErrors = []
    i = 0
    while (i) < len(values):
        sqErrors.append((values[i]-mediaMobile[i])**2) 
        i = i+1
    return sqErrors




''' per processare tutto istanzi un elemento di questa classe '''
class ForecastsProcessor:
    def __init__(self, _totAmount, _nvalues, data):
        self.totAmount = _totAmount  # ammontare dell'investimento iniziale == valore iniziale del portafogli
        self.nvalues = _nvalues  # numero di giorni di cui si compone la finestra per la realizzazione della media mobile
        # dictionary che ha in chiave il nome del file csv e in valore i dati calcolati come
        # differenza dei valori letti dal csv
        self.indexedDataDiff = computeIndexedDataDiff(data) 
        self.dailyBasedIndexedPortfolioValues = []
        self.dailyBasedPortfolioValues = []
        self.portfolioDiff = []
        self.movingAverage = []
        self.squaredErrorList = []
        
    def getIndexedDataDiff(self): return self.indexedDataDiff
    def getDailyBasedIndexedPortfolioValues(self): return self.dailyBasedIndexedPortfolioValues
    def dailyBasedPortfolioValues(self): return self.dailyBasedPortfolioValues
    def getPortfolioDiff(self): return self.portfolioDiff
    def getMovingAverage(self): return self.movingAverage
    def getSquaredErrorList(self): return self.squaredErrorList
         
    #calcola valori di (returnMediaMobile, stdev) => li ritorna nella forma di un dictionary
    def compute(self, portfolio):
        # dictionary (nome file csv, lista contenente tutti i valori assunti dall'investimento sullo specifico indice day-by-day)
        self.dailyBasedIndexedPortfolioValues = computeDailyIndexedValues(self.indexedDataDiff, portfolio, self.totAmount)
        # lista contenente il valore complessivo dell'investimento day by day
        self.dailyBasedPortfolioValues = computePortfolioValues(self.dailyBasedIndexedPortfolioValues)
        # lista contenente la variazione del valore del portafoglio di investimenti
        self.portfolioDiff = computePortfolioDiff(self.dailyBasedPortfolioValues)
        # media mobile calcolata sui valori day by day assunti dal portafoglio di investimento
        self.movingAverage = computeMovingAverage(self.dailyBasedPortfolioValues,self.nvalues)
        # (colonna AC excel) lista cotenente gli errori quadratici tra la media mobile e il valore effettivo del portafoglio in una certa data
        # nota che è necessario rimuovere i primi nvalues-1 valori, sui quali è impossibile calcolare la media mobile 
        self.squaredErrorList = computeSquaredError(self.dailyBasedPortfolioValues[(self.nvalues-1):], self.movingAverage)
        # (cella AE4 excel) è l'ultima media mobile calcolata, sarà quella restituita come valore del portafoglio a fine investimento
        returnMediaMobile =  self.movingAverage[len(self.movingAverage)-1]
        # (cella AE5 excel) è il valore della deviazione standard che verrà restituito per valutare la bontà della previsione
        stdev = math.sqrt(sum(self.squaredErrorList)/len(self.squaredErrorList))
        print("returnMediaMobile: ", returnMediaMobile)
        print("stdev: ", stdev)
        return { "returnMediaMobile": returnMediaMobile, "stdev": stdev}     
    
    
