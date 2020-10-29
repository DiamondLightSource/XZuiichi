import subprocess
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

path = os.getcwd()
print(path)
combinations = 26
resshel = [10.0, 5.00, 4.70, 4.50, 4.20, 3.90, 3.60, 3.40, 3.10, 2.80, 2.50, 2.30, 2.00]

data = pd.read_csv("all.csv", header=None, engine='c', usecols=[0, 4, 8, 9, 10, 11, 12, 13, 14])
data.columns = ['res', 'completeness', 'isigi', 'rmeas', 'cchalf', 'anomcorr', 'sigano', 'nano', 'ident']
data.set_index(['ident', 'res'], inplace=True)
data.sort_index(inplace=True)

sanity_pass = []
for i in range(1, combinations, 1):
    for j in resshel:
        comp = data.loc[(i, j), 'completeness']
        isigi = data.loc[(i, j), 'isigi']
        rmeas = data.loc[(i, j), 'rmeas']
        cchalf = data.loc[(i, j), 'cchalf']
        if (comp > 80) and (isigi > 1) and (rmeas < 100) and (cchalf > 25):
            sanity_pass += [(i, j)]
        else:
            print(i, j, ' did not pass sanity check')
print(sanity_pass)