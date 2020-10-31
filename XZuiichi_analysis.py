import subprocess
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from operator import itemgetter
from statistics import mode 


path = os.getcwd()
print(path)
combinations = 26
reslist = [10.00, 5.00, 4.70, 4.50, 4.20, 3.90, 3.60, 3.40, 3.10, 2.80, 2.50, 2.30, 2.00]

data = pd.read_csv("all.csv", header=None, engine='c', usecols=[0, 4, 8, 9, 10, 11, 12, 13, 14])
data.columns = ['res', 'completeness', 'isigi', 'rmeas', 'cchalf', 'anomcorr', 'sigano', 'nano', 'ident']
data.set_index(['ident', 'res'], inplace=True)
data.sort_index(inplace=True)

sanity_pass = []
for i in range(1, combinations, 1):
    for j in reslist:
        comp = data.loc[(i, j), 'completeness']
        isigi = data.loc[(i, j), 'isigi']
        rmeas = data.loc[(i, j), 'rmeas']
        cchalf = data.loc[(i, j), 'cchalf']
        ac = data.loc[(i, j), 'anomcorr']
        if (comp > 80) and (isigi > 1) and (rmeas < 100) and (cchalf > 25):
            sanity_pass += [(i, j, ac)]
        else:
            continue

id, res, ano = 0, 1, 2

# work in progress
best_results = []
for k in reslist:
    m = []
    for l in ( x for x in sanity_pass if x[1] == k ):
        m += [(l)]
    try:
        ds = max(m, key=itemgetter(2))[0]
        bestano = max(m, key=itemgetter(2))[2]
        if bestano > 10:
            print('To a resolution of', k , 'the best run is', ds, 'with an anomcorr of', bestano)
            best_results += [(k, bestano, ds)]
        else:
            print('To a resolution of', k , 'the best run is', ds, 'but this has an anomcorr of', bestano, 'which indicates this may not be suitable for phasing.')
            best_results += [(k, bestano, ds)]
    except:
        print('No data at', k, 'A passed the sanity check.')

x_val = [x[0] for x in best_results]
y_val = [x[1] for x in best_results]
c_val = [x[2] for x in best_results]
fig, ax = plt.subplots(1,1)
ax.scatter(x_val, y_val, c=cm.Spectral([i * 10 for i in c_val]))
ax.plot(x_val, y_val, 'b-')
plt.axhline(y=9, color='r', linestyle='--')
ax.invert_xaxis()
plt.show()

best_run = mode(c_val)
print('The best run appears to be number', best_run)