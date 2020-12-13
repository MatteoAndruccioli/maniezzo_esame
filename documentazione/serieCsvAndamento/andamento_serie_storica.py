import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from termcolor import colored
import matplotlib.patches as mpatches

def show_piece(current):
    plt.rcParams["figure.figsize"] = (10,8) # redefines figure size
    plt.plot(current)
    plt.show()

def findMax(x, y):
    current = pd.read_csv(serieName, usecols=[0], names=['value'], header=0).values[x:y]
    value = max(current)
    #print("max = ", value)
    #print("indice parziale = ", np.where(current == value))
    #print("INDICE BASE = ",np.where(base == value))
    #print(colored('massimo ({}, {})'.format(np.where(base == value)[0], value), 'cyan'))
    #print("---------------------------------------------------")
    return np.where(base == value)[0]
    
def findMin(x, y):
    current = pd.read_csv(serieName, usecols=[0], names=['value'], header=0).values[x:y]
    value = min(current)
    #print("max = ", value)
    #print("indice parziale = ", np.where(current == value))
    #print("INDICE BASE = ",np.where(base == value))
    #print(colored('minimo ({}, {})'.format(np.where(base == value)[0], value), 'cyan'))
    #print("---------------------------------------------------")
    return np.where(base == value)[0]

def getYValues(indiciBase):
    toRet = []
    for elem in indiciBase:
        toRet.append(base[elem][0])
    return toRet

def printPlot(serieName, x, y):
    plt.plot(x, y, 'bo-')
    plt.title(serieName)
    plt.show()


names = ["FTSE_MIB_.csv", "MSCI_EM.csv", "MSCI_EURO.csv", "SP_500.csv"]

for name in names:
    dataset = pd.read_csv("./"+name, usecols=[0], names=['value'], header=0).values
    plt.rcParams["figure.figsize"] = (10,8) # redefines figure size
    plt.plot(dataset)
    plt.title(name)
    plt.show()


""" FTSE_MIB_.csv """
serieName = "FTSE_MIB_.csv"
base = pd.read_csv(serieName, usecols=[0], names=['value'], header=0).values

xValues_FTSE_MIB_ = [0]
#print(colored('partenza ({}, {})'.format(0, base[0]), 'cyan'))

temp = findMin(0, 1000)
xValues_FTSE_MIB_.append(temp[0])

temp = findMax(temp[0], 2000)
xValues_FTSE_MIB_.append(temp[0])

temp = findMin(temp[0], 2500)
xValues_FTSE_MIB_.append(temp[0])

temp = findMax(temp[0], 3000)
xValues_FTSE_MIB_.append(temp[0])

temp = findMin(temp[0], 3500)
xValues_FTSE_MIB_.append(temp[0])

temp = findMax(temp[0], 4100)
xValues_FTSE_MIB_.append(temp[0])

temp = findMin(temp[0], 4500)
xValues_FTSE_MIB_.append(temp[0])

temp = findMax(temp[0], 5000)
xValues_FTSE_MIB_.append(temp[0])

temp = findMin(temp[0], 5000)
xValues_FTSE_MIB_.append(temp[0])

temp = findMax(temp[0], 5200)
xValues_FTSE_MIB_.append(temp[0])

temp = findMin(temp[0], 5220)
xValues_FTSE_MIB_.append(temp[0])
#print(colored('arrivo ({}, {})'.format((len(base)-1), base[(len(base)-1)]), 'cyan'))
xValues_FTSE_MIB_.append(len(base)-1)
yValues_FTSE_MIB_ = getYValues(xValues_FTSE_MIB_)

print(colored('FTSE_MIB_', 'magenta'))
print(colored('xValues_FTSE_MIB_: ', 'cyan'), xValues_FTSE_MIB_)
print(colored('yValues_FTSE_MIB_: ', 'cyan'), yValues_FTSE_MIB_)
printPlot("FTSE_MIB", xValues_FTSE_MIB_, yValues_FTSE_MIB_)
print("---------------------------------------------------")





""" MSCI_EM.csv """
serieName = "MSCI_EM.csv"
base = pd.read_csv(serieName, usecols=[0], names=['value'], header=0).values

xValues_MSCI_EM = [0]
#print(colored('partenza ({}, {})'.format(0, base[0]), 'cyan'))

temp = findMin(0, 1000)
xValues_MSCI_EM.append(temp[0])

temp = findMax(temp[0], 2100)
xValues_MSCI_EM.append(temp[0])

temp = findMin(temp[0], 2800)
xValues_MSCI_EM.append(temp[0])

temp = findMax(temp[0], 3500)
xValues_MSCI_EM.append(temp[0])

temp = findMin(temp[0], 4500)
xValues_MSCI_EM.append(temp[0])

temp = findMax(temp[0], 5000)
xValues_MSCI_EM.append(temp[0])

temp = findMin(temp[0], 5220)
xValues_MSCI_EM.append(temp[0])
#print(colored('arrivo ({}, {})'.format((len(base)-1), base[(len(base)-1)]), 'cyan'))
xValues_MSCI_EM.append(len(base)-1)
yValues_MSCI_EM = getYValues(xValues_MSCI_EM)

print(colored('MSCI_EM', 'magenta'))
print(colored('xValues_MSCI_EM: ', 'cyan'), xValues_MSCI_EM)
print(colored('yValues_MSCI_EM: ', 'cyan'), yValues_MSCI_EM)
printPlot("MSCI_EM", xValues_MSCI_EM, yValues_MSCI_EM)
print("---------------------------------------------------")





""" MSCI_EURO.csv """
serieName = "MSCI_EURO.csv"
base = pd.read_csv(serieName, usecols=[0], names=['value'], header=0).values

xValues_MSCI_EURO = [0]
#print(colored('partenza ({}, {})'.format(0, base[0]), 'cyan'))

temp = findMin(0, 1000)
xValues_MSCI_EURO.append(temp[0])

temp = findMax(temp[0], 2000)
xValues_MSCI_EURO.append(temp[0])

temp = findMin(temp[0], 2500)
xValues_MSCI_EURO.append(temp[0])

temp = findMax(temp[0], 3000)
xValues_MSCI_EURO.append(temp[0])

temp = findMin(temp[0], 3100)
xValues_MSCI_EURO.append(temp[0])

temp = findMax(temp[0], 4100)
xValues_MSCI_EURO.append(temp[0])

temp = findMin(temp[0], 4800)
xValues_MSCI_EURO.append(temp[0])

temp = findMax(temp[0], 5200)
xValues_MSCI_EURO.append(temp[0])

temp = findMin(temp[0], 5220)
xValues_MSCI_EURO.append(temp[0])
#print(colored('arrivo ({}, {})'.format((len(base)-1), base[(len(base)-1)]), 'cyan'))
xValues_MSCI_EURO.append(len(base)-1)
yValues_MSCI_EURO = getYValues(xValues_MSCI_EURO)

print(colored('MSCI_EURO', 'magenta'))
print(colored('xValues_MSCI_EURO: ', 'cyan'), xValues_MSCI_EURO)
print(colored('yValues_MSCI_EURO: ', 'cyan'), yValues_MSCI_EURO)
printPlot("MSCI_EURO", xValues_MSCI_EURO, yValues_MSCI_EURO)
print("---------------------------------------------------")



""" SP_500.csv """
serieName = "SP_500.csv"
base = pd.read_csv(serieName, usecols=[0], names=['value'], header=0).values

xValues_SP_500 = [0]
#print(colored('partenza ({}, {})'.format(0, base[0]), 'cyan'))

temp = findMin(0, 1000)
xValues_SP_500.append(temp[0])

temp = findMax(temp[0], 2000)
xValues_SP_500.append(temp[0])

temp = findMin(temp[0], 2500)
xValues_SP_500.append(temp[0])

temp = findMax(temp[0], 5200)
xValues_SP_500.append(temp[0])

temp = findMin(temp[0], 5220)
xValues_SP_500.append(temp[0])
#print(colored('arrivo ({}, {})'.format((len(base)-1), base[(len(base)-1)]), 'cyan'))
xValues_SP_500.append(len(base)-1)
yValues_SP_500 = getYValues(xValues_SP_500)

print(colored('SP_500', 'magenta'))
print(colored('xValues_SP_500: ', 'cyan'), xValues_SP_500)
print(colored('yValues_SP_500: ', 'cyan'), yValues_SP_500)
printPlot("SP_500", xValues_SP_500, yValues_SP_500)
print("---------------------------------------------------")


#prende un array e ne riscala i valori in un ragne 0<x<50000
def changeScale(oldArray):
    toRet = []
    newMin = min(yValues_FTSE_MIB_)
    newMax = max(yValues_FTSE_MIB_)
    oldMin = min(oldArray)
    oldMax = max(oldArray)
    for oldValue in oldArray:
        newValue = (((oldValue - oldMin) * (newMax - newMin)) / (oldMax - oldMin)) + newMin
        toRet.append(newValue)
    return toRet







""" 
    Creo il vettore andamento: 
        0 => economia in calo
        1 => economia in crescita
"""

andamento = np.concatenate((
    # indici[0,658] cala
    np.full( shape=(659-0), fill_value=0, dtype=np.int),
    # indici[628,1852] cresce
    np.full( shape=(1852-658), fill_value=1, dtype=np.int),
    # indici[1852,2221] cala
    np.full( shape=(2221-1852), fill_value=0, dtype=np.int),
    # indici[2221,2781] cresce
    np.full( shape=(2781-2221), fill_value=1, dtype=np.int),
    # indici[2781,2884] cala
    np.full( shape=(2884-2781), fill_value=0, dtype=np.int),
    # indici[2884,3811] cresce
    np.full( shape=(3811-2884), fill_value=1, dtype=np.int),
    # indici[3811,4029] cala
    np.full( shape=(4029-3811), fill_value=0, dtype=np.int),
    # indici[4029,5078] cresce
    np.full( shape=(5078-4029), fill_value=1, dtype=np.int),
    # indici[5078,5101] cala
    np.full( shape=(5101-5078), fill_value=0, dtype=np.int),
    # indici[5101,5222] cresce
    np.full( shape=(5222-5101), fill_value=1, dtype=np.int)
))

plt.plot(((andamento*2000)+50000), 'ro-')
plt.plot(xValues_FTSE_MIB_, changeScale(yValues_FTSE_MIB_), 'bo-')
plt.plot(xValues_MSCI_EM, changeScale(yValues_MSCI_EM), 'go-')
plt.plot(xValues_MSCI_EURO, changeScale(yValues_MSCI_EURO), 'mo-')
plt.plot(xValues_SP_500, changeScale(yValues_SP_500), 'yo-')

plt.title(serieName)
blue_patch = mpatches.Patch(color='blue', label='FTSE_MIB')
green_patch = mpatches.Patch(color='green', label='MSCI_EM')
magenta_patch = mpatches.Patch(color='magenta', label='MSCI_EURO ')
yellow_patch = mpatches.Patch(color='yellow', label='SP_500 ')
red_patch = mpatches.Patch(color='red', label='andamento ')
plt.legend(handles=[blue_patch, green_patch, magenta_patch, yellow_patch, red_patch])
plt.rc('legend',fontsize=10)
plt.rcParams["figure.figsize"] = (18,13)

plt.show()
