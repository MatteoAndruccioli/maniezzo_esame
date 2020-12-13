import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import os, math, sys, io, base64


names = ["All_Bonds.csv", "FTSE_MIB_.csv", "GOLD_SPOT.csv", "MSCI_EM.csv", "MSCI_EURO.csv", "SP_500.csv", "US_Treasury.csv"]

for name in names:
    dataset = pd.read_csv("./"+name, usecols=[0], names=['value'], header=0).values
    plt.rcParams["figure.figsize"] = (10,8) # redefines figure size
    plt.plot(dataset)
    plt.title(name)
    plt.show()




