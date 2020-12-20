import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from termcolor import colored
import matplotlib.patches as mpatches
import csv

def getAndamentoEconomico():
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
        np.full( shape=(5222-5101+1), fill_value=1, dtype=np.int) #nota il +1 è perchè devi prevedere
    ))
    return andamento
ae = getAndamentoEconomico()

archive_file = open ('andamentoEconomico.csv', 'w')
wtr = csv.writer(archive_file, delimiter=',', lineterminator='\n')
for x in ae : wtr.writerow ([x])
archive_file.close()

