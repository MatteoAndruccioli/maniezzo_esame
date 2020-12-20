# Seed value
# Apparently you may use different seed values at each stage
seed_value= 1234

# 1. Set the `PYTHONHASHSEED` environment variable at a fixed value
import os
os.environ['PYTHONHASHSEED']=str(seed_value)

# 2. Set the `python` built-in pseudo-random generator at a fixed value
import random
random.seed(seed_value)

# 3. Set the `numpy` pseudo-random generator at a fixed value
import numpy as np
np.random.seed(seed_value)

# 4. Set the `tensorflow` pseudo-random generator at a fixed value
import tensorflow as tf
tf.compat.v1.set_random_seed(seed_value)

# 5. Configure a new global `tensorflow` session
from keras.models import Sequential
from keras.layers import Dense
session_conf = tf.compat.v1.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=1)
sess = tf.compat.v1.Session(graph=tf.compat.v1.get_default_graph(), config=session_conf)
tf.compat.v1.keras.backend.set_session(sess)

import pandas as pd
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import sys
import csv


#contiene i parametri che indicano come eseguire le previsioni per ogni indice
# nomefile(senza .csv) : [Multivariato, 2HiddenLayer, epochs, n_hidden_1, n_hidden_2, serieMax], i valori assenti sono stati rimpiazzati con dei "False"
parametersByIndex = {
    "FTSE_MIB_"   : [True, True, 400, 67, 34, 50000],
    "MSCI_EM"     : [True, False, 600, 67, False, 1300],
    "MSCI_EURO"   : [True, True, 400, 169, 133, 1700],
    "SP_500"      : [True, False, 100, 133, False, 4000],
    "All_Bonds"   : [False, True, 100, 133, 34],
    "GOLD_SPOT"   : [False, True, 400, 67, 67],
    "US_Treasury" : [False, True, 600, 67, 34]
}

serieMin = 0 # vecchio valore di minimo per le serie nel multivariato
scaledMin = 0   # valore di minimo per nuova scala per valori nel multivariato
scaledMax = 10  # valore di massimo per nuova scala per valori nel multivariato
forecast_window_size = 22*12 # numero di valori da prevedere, corrispondono circa ai valori relativi a un anno
npast = 22*6 # numero di valori contenuti nella sliding window che mi permettono di prevedere valore successivo, circa 6 mesi
#nota: 22 sono i giorni lavorativi in un mese circa

# Le seguenti variabili conterranno valori di parametri relativi alla serie che si sta analizzando (vanno aggiornati ogni volta)
currentSerieName = "" # nome della serie che si sta analizzando
current_is_multivariate = False
has_2_hidden_layers = False
n_epochs = 0 # numero di epoche usate per l'addestramento 
n_hidden_1 = 0 # numero di neuroni nell'hidden layer 1
n_hidden_2 = 0 # numero di neuroni nell'hidden layer 2
serieMax = 0 # valore di serieMax
trainMSE = 0
testMSE = 0


forecastDictionary = {}

# funzione che si occupa di aggiornare forecastDictionary man mano che l'esecuzione procede
def appendForecastToForecastDictionary(forecasts):
    forecastDictionary[currentSerieName] = forecasts


# funzione di debug stampa lo stato attuale dei parametri relativi alla serie corrente
def printCurrentParameters():
    arr = []
    arr.append("currentSerieName: " + currentSerieName)
    arr.append("current_is_multivariate: " + str(current_is_multivariate))
    arr.append("has_2_hidden_layers: " + str(has_2_hidden_layers))
    arr.append("n_epochs: " + str(n_epochs))
    arr.append("n_hidden_1: " + str(n_hidden_1))
    if(has_2_hidden_layers): arr.append("n_hidden_2: " + str(n_hidden_2))
    if(current_is_multivariate): arr.append("serieMax: " + str(serieMax))
    arr.append("trainMSE: " + str(trainMSE))
    arr.append("testMSE: " + str(testMSE))   
    for line in arr: print(line)
    print("----------------------------------------------------")
    return arr

#permette di ottenere il nome dell'indice a partire del nome del file 
def getIndexNameFromCsv(csvFileName): return csvFileName[:-4]

# aggiorna variabili relative ai parametri della serie analizzata 
def updateCurrentSeriesParameters(newCurrentSerieName): 
    #questo global serve per poter modificare le variabili d'ambiente, se no le prende per variabili locali
    global currentSerieName, current_is_multivariate, has_2_hidden_layers, n_epochs, n_hidden_1, n_hidden_2, serieMax
    currentSerieName = newCurrentSerieName
    current_is_multivariate = parametersByIndex[currentSerieName][0]
    has_2_hidden_layers = parametersByIndex[currentSerieName][1]
    n_epochs = parametersByIndex[currentSerieName][2]
    n_hidden_1 = parametersByIndex[currentSerieName][3]
    if (has_2_hidden_layers) : n_hidden_2 = parametersByIndex[currentSerieName][4]
    if (current_is_multivariate) : serieMax = parametersByIndex[currentSerieName][5]
    return parametersByIndex[currentSerieName]
    
#stampa i valori contenuti in forecast dentro al file csv
def printForecastsToCsv(forecasts, fileName = currentSerieName+'_previsioni.csv'):
   archive_file = open ("../pythonDir/previsioni/"+fileName, 'w')
   wtr = csv.writer(archive_file, delimiter=',', lineterminator='\n')
   for x in forecasts : wtr.writerow ([x])
   archive_file.close()

# stampa i metadati su un foglio csv
def printMetadataToCsv():   
   archive_file = open ("../pythonDir/metadata/"+currentSerieName+"_metadata.csv", 'w')
   wtr = csv.writer(archive_file, delimiter=',', lineterminator='\n')
   for x in printCurrentParameters() : wtr.writerow ([x])
   archive_file.close()
   
# calcola e stampa il valore di MSE su forecast, necessario passare come trueValues i valori di test
def print_MSE(forecasts, trueValues):
   global testMSE
   testMSE = np.square(np.subtract(forecasts,trueValues[:len(forecasts)])).mean() 
   print('Score on test: MSE = {0:0.2f} '.format(testMSE))

''' funzioni usate nel NON multivariato '''
# permette di calcolare le sliding window
def compute_windows(nparray, npast=1):
    dataX, dataY = [], [] # window and value
    for i in range(len(nparray)-npast-1):
        a = nparray[i:(i+npast), 0]
        dataX.append(a)
        dataY.append(nparray[i + npast, 0])
    return np.array(dataX), np.array(dataY)   
   
# predice i prossimi nValuesToForecast valori usando la rete model e basandosi sugli ultimi lastKnownValues valori
def forecastNValues(nValuesToForecast, model, lastKnownValues):
    predicted_values = []
    # uso una variabile di appoggio per i valori sulla base dei quali viene eseguita la predizione
    known_values = lastKnownValues 
    for i in range (0,nValuesToForecast):
        nextValue = forecastNextValue(model, known_values)
        predicted_values = np.append(predicted_values,[nextValue]) # valore previsto
        known_values = np.append(known_values[1:],[nextValue])
    return predicted_values
    
# funzione che permette di prevedere il prossimo valore secondo il modello passato
# model => rete mlp su cui è stato effettuato training
# last knownValues = i dati su cui baserò la previsione
def forecastNextValue(model, lastKnownValues):
    reshapedLastKnownValues = lastKnownValues.reshape((1,len(lastKnownValues))) #i valori devono essere non su un array verticale ma orizzontale per la previsione
    return model.predict(reshapedLastKnownValues, verbose=0) # è il prossimo valore previsto


''' funzioni usate nel multivariato '''

#prende un array e ne riscala i valori in un ragne a scelta
def changeScale(oldArray, newMin, newMax, oldMin, oldMax):
    toRet = []
    for oldValue in oldArray:
        newValue = (((oldValue - oldMin) * (newMax - newMin)) / (oldMax - oldMin)) + newMin
        toRet.append(newValue[0])
    return np.array(toRet)

# versione di changeScale per array di scalari
def changeScaleScalar(oldArray, newMin, newMax, oldMin, oldMax):
    toRet = []
    for oldValue in oldArray:
        newValue = (((oldValue - oldMin) * (newMax - newMin)) / (oldMax - oldMin)) + newMin
        toRet.append(newValue)
    return np.array(toRet)
   
   
# permette di calcolare le sliding window
def compute_windows_multivar(nparray, andamento, npast=1):
    dataX, dataY = [], [] # window and value
    for i in range(len(nparray)-npast-1):
        a = np.append(nparray[i:(i+npast)], andamento[(i+npast)])
        dataX.append(a)
        dataY.append(nparray[i + npast])
    return np.array(dataX), np.array(dataY)
                                     

# predice i prossimi nValuesToForecast valori usando la rete model e basandosi sugli ultimi lastKnownValues valori
def forecastNValues_multivar(nValuesToForecast, model, lastKnownValues, andamentoEconomicoFuturo):
    predicted_values = []
    # uso una variabile di appoggio per i valori sulla base dei quali viene eseguita la predizione
    known_values = lastKnownValues 
    for i in range (0,nValuesToForecast):
        nextValue = forecastNextValue_multivar(model, known_values)
        predicted_values = np.append(predicted_values,[nextValue]) # aggiungo il nuovo valore previsto
        known_values = known_values[:len(known_values)-1] # droppo il vecchio valore relativo all'andamento dell'economia
        known_values = np.append(known_values, [nextValue])
        known_values = np.append(known_values, andamentoEconomicoFuturo[i])
        known_values = known_values[1:]
    return predicted_values
    
# funzione che permette di prevedere il prossimo valore secondo il modello passato
# model => rete mlp su cui è stato effettuato training
# last knownValues = i dati su cui baserò la previsione
def forecastNextValue_multivar(model, lastKnownValues):
    reshapedLastKnownValues = lastKnownValues.reshape((1,len(lastKnownValues))) #i valori devono essere non su un array verticale ma orizzontale per la previsione
    return model.predict(reshapedLastKnownValues, verbose=0) # è il prossimo valore previsto



''' funzioni per la stampa dei plot'''

# stampa un grafico unicamente con i dati di train e test
def print_train_and_test(train, test, titolo):
   plt.rcParams["figure.figsize"] = (14,10)
   plt.plot(train)
   plt.plot(np.concatenate((np.full(len(train),np.nan), test)), color="green")
   plt.title(titolo)
   blue_patch = mpatches.Patch(color='blue', label='Train')
   green_patch = mpatches.Patch(color='green', label='Test')
   plt.legend(handles=[blue_patch, green_patch])
   plt.rc('legend',fontsize=40)
   plt.show() 
   
# stampa un grafico con i dati di train e test e predizioni su train e su test NON sono le forecast
def print_train_test_and_predicts(dataset, train, test, trainPredict, testPredict, titolo):
   plt.rcParams["figure.figsize"] = (14,10)
   plt.plot(dataset)
   plt.plot(np.concatenate((np.full(npast+1,np.nan),trainPredict[:,0])), color="green")
   plt.plot(np.concatenate((np.full(len(train)+npast+1,np.nan), testPredict[:,0])), color="magenta")
   plt.title(titolo)
   blue_patch = mpatches.Patch(color='blue', label='Train_test')
   green_patch = mpatches.Patch(color='green', label='trainPredict')
   magenta_patch = mpatches.Patch(color='magenta', label='testPredict')
   plt.legend(handles=[blue_patch, green_patch, magenta_patch])
   plt.rc('legend',fontsize=20)
   plt.show()

   
# stampa un grafico con i dati di train e test e forecast
def print_train_test_forecast(train, test, forecasted_values, titolo):
   plt.rcParams["figure.figsize"] = (14,10)
   plt.plot(train)
   plt.plot(np.concatenate((np.full(len(train),np.nan), test)), color="green")
   plt.plot(np.concatenate((np.full(len(train),np.nan), forecasted_values)), color="pink")
   plt.title(titolo)
   blue_patch = mpatches.Patch(color='blue', label='Train')
   green_patch = mpatches.Patch(color='green', label='Test')
   pink_patch = mpatches.Patch(color='pink', label='Forecasts ' + str(forecast_window_size))
   plt.legend(handles=[blue_patch, green_patch, pink_patch])
   plt.rc('legend',fontsize=20)
   plt.show()
   
   
# stampa un grafico con i dati di test e forecast
def print_test_forecast(test, forecasted_values, titolo):
   plt.rcParams["figure.figsize"] = (14,10)
   plt.plot(test[:forecast_window_size], color="green")
   plt.plot(forecasted_values, color="pink")
   plt.title(titolo)
   green_patch = mpatches.Patch(color='green', label='Test')
   pink_patch = mpatches.Patch(color='pink', label='Forecasts ' + str(forecast_window_size))
   plt.legend(handles=[green_patch, pink_patch])
   plt.rc('legend',fontsize=20)
   plt.show()
   
   
   
""" FUNZIONE DA CHIAMARE ESTERNAMENTE """
def makePrevisions(csvFileArray) :
    # cambia working directory to script path
   abspath = os.path.abspath(__file__)
   dname = os.path.dirname(abspath)
   os.chdir(dname)
   
   # stampo info sugli argomenti passati da chi chiama lo script
   print('MAPE Number of arguments:', len(csvFileArray)) # Scrive la lunghezza del vettore degli argomenti (argv).
   print('MAPE Argument List:', str(csvFileArray), 'andamentoEconomico:',csvFileArray[0])                              
   # input andamentoEconomico.csv FTSE_MIB_.csv MSCI_EM.csv MSCI_EURO.csv SP_500.csv All_Bonds.csv GOLD_SPOT.csv US_Treasury.csv


   ''' Carico i dati dai file ricevuti da linea di comando '''
   # carico in andamentoEconomico la serie che individua andamentoEconomico, usata nel multivariato
   andamentoEconomico = pd.read_csv("../pythonDir/serieStoriche/"+csvFileArray[0]).values.astype('float32')
   
   # carico nell'array indexNames tutti i nomi di indici (legati ai file passati al lancio) 
   indexNames = [] #questo array conterrà i nomi di tutti i documenti passati meno il primo che sarà "andamentoEconomico.csv"
   for i in range(1, len(csvFileArray)): indexNames.append(getIndexNameFromCsv(csvFileArray[i]))
   
   
   ''' Devo applicare le seguenti operazioni a tutte le serie che mi passano '''
   for indexName in indexNames:
       # aggiorno le variabili d'ambiente relative alla serie corrente
       updateCurrentSeriesParameters(indexName)    
       # carico la serie che processo in questa iterazione
       dataset = pd.read_csv("../pythonDir/serieStoriche/"+currentSerieName+".csv").values.astype('float32')
       
       ''' Devo ora determinare i valori delle variabili train, test, trainX, trainY, testX, testY, n_batch_size '''
       dataset_0_10, train, test, trainX, trainY, testX, testY = [], [], [], [], [], [], []
       n_batch_size = 0
       
       cutpoint = len(dataset)-forecast_window_size

       # è necessario distinguere il caso del multivariato: richiede scaling dei valori 
       if (current_is_multivariate):
           #cambio il range dei dati della serie storica per farlo rientrare in [scaledMin, scaledMax] 
           dataset_0_10 = changeScale(dataset, scaledMin, scaledMax, serieMin, serieMax)
                      
           # split dei dati in train - test sets
           train, test = dataset_0_10[:cutpoint], dataset_0_10[cutpoint:]
           #print("Len train={0}, len test={1}".format(len(train), len(test)))

           # calcolo i valori delle sliding window di train e test così da poter fare training e forecast 
           trainX, trainY = compute_windows_multivar(train, andamentoEconomico, npast)
           testX, testY = compute_windows_multivar(test, andamentoEconomico, npast)
           
           # calcolo n_batch_size
           n_batch_size=len(trainX)
           
           #printa train e test
           print_train_and_test(train, test, "Dati di Train e Test - " + currentSerieName)
       else :
           # split dei dati in train - test sets   
           train, test = dataset[:cutpoint], dataset[cutpoint:]
           #print("Len train={0}, len test={1}".format(len(train), len(test)))

           # calcolo i valori delle sliding window di train e test così da poter fare training e forecast 
           trainX, trainY = compute_windows(train, npast)
           testX, testY = compute_windows(test, npast)
           
           # calcolo n_batch_size
           n_batch_size=len(train)-npast-1
       
           #printa train e test
           print_train_and_test(train, test[:,0], "Dati di Train e Test - " + currentSerieName)
       
       
       ''' Ora è necessario creare la rete neurale, con attenzione al numero di hidden layers '''
       n_input_dim = npast
       if (current_is_multivariate): n_input_dim = npast+1 # input aggiuntivo relativo all'andamento economico
       
       model = Sequential()
       model.add(Dense(n_hidden_1, input_dim=n_input_dim, activation='relu')) 
       if (has_2_hidden_layers): model.add(Dense(n_hidden_2, activation='relu')) # 2° lvl hidden
       model.add(Dense(1)) # prevedo sempre il solo valore successivo => 1 neurone di output
       model.compile(loss='mean_squared_error', optimizer='adam')
       
       # eseguo il training della rete neurale 
       model.fit(trainX, trainY, epochs=n_epochs, batch_size=n_batch_size, verbose=2) 
       
       
       ''' effettuo una valutazione del training su test e train, grafico i risultati '''
       trainScore = model.evaluate(trainX, trainY, verbose=0)
       trainMSE = trainScore
       print('Score on train: MSE = {0:0.2f} '.format(trainScore))
       trainPredict = model.predict(trainX) # prediction sul train 
       testPredict = model.predict(testX) # predictions sul test    
       if (current_is_multivariate): print_train_test_and_predicts(dataset, train, test, trainPredict, testPredict, "TrainTest, TrainPredict, TestPredict - " + currentSerieName)
       else : print_train_test_and_predicts(dataset, train, test[:,0], trainPredict, testPredict, "TrainTest, TrainPredict, TestPredict - " + currentSerieName)
       
       ''' effettuo previsione dei prossimi forecast_window_size valori'''
       last_row_trainX = trainX[len(trainX)-1]
       
       
       forecast_to_print = []
       if (current_is_multivariate): # nota i dati andranno riportati sulla scala originale
           
           #l'andamento economico futuro sono i valori a partire da quello successivo all'ultimo usato nella sliding window di train
           forecasted_values = forecastNValues_multivar(forecast_window_size, model, last_row_trainX, andamentoEconomico[len(train):]) 
           
           print_train_test_forecast(train, test, forecasted_values, "Dati di Train, Test e Forecast scalati - " + currentSerieName)
           print_test_forecast(test, forecasted_values, "Dati di Test e Forecast scalati - " + currentSerieName)
           
           print_MSE(forecasted_values, test)
           
           ''' Riporto i dati sulla scala originale'''
           
           scale_forecasted_values = changeScaleScalar(forecasted_values, serieMin, serieMax, scaledMin, scaledMax)
           scale_test = changeScaleScalar(test, serieMin, serieMax, scaledMin, scaledMax)
           scale_train = changeScaleScalar(train, serieMin, serieMax, scaledMin, scaledMax)
           
           print_train_test_forecast(scale_train, scale_test, scale_forecasted_values, "Dati di Train, Test  e Forecast - " + currentSerieName)
           print_test_forecast(scale_test, scale_forecasted_values, "Dati di Test  e Forecast - " + currentSerieName)
           forecast_to_print = scale_forecasted_values
       else :
           forecasted_values = forecastNValues(forecast_window_size, model, last_row_trainX) 
           print_train_test_forecast(train, test[:,0], forecasted_values, "Dati di Train, Test e Forecast - " + currentSerieName)
           print_test_forecast(test[:,0], forecasted_values, "Dati di Test e Forecast - " + currentSerieName) 
           print_MSE(forecasted_values, test)
           forecast_to_print = forecasted_values
           
       printForecastsToCsv(forecast_to_print, currentSerieName+'_forecasts.csv')
       printMetadataToCsv()
       appendForecastToForecastDictionary(forecast_to_print)
   return forecastDictionary
   
   
   
   
   
   
   
   
   
   