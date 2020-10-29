import subprocess
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

path = os.getcwd()
print(path)
combinations = 26

data = pd.read_csv("all.csv", header=None, engine='c')
data.columns = ['res', 'obs', 'uniq', 'pos', 'completeness', 'robs', 'rexp', 'compared', 'isigi', 'rmeas', 'cchalf', 'anomcorr', 'sigano', 'nano', 'ident']

data.set_index(['ident', 'res'], inplace=True)

data.sort_index(inplace=True)

for i in range(1, combinations, 1):
    showme = data.loc[(i, 3.4), 'obs']
    print(str(i) + " " + str(showme / 23))

print(data)