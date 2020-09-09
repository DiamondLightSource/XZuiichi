import subprocess
import sys
import os
import pandas as pd

path = os.getcwd()
print(path)

res1, res2, res3, res4, res5, res6, res7, res8, res9, res10, res11, res12, res13 = 10.0, 5.0, 4.8, 4.6, 4.5, 4.3, 4.1, 3.9, 3.7, 3.5, 3.4, 3.2, 3.0

columnlist = ['res', 'obsref', 'uniref', 'posref', 'comp', 'robs', 'rexp', 'compar', 'isigi', 'rmeas', 'cchalf', 'anomcorr', 'sigano', 'nano', 'run']

df = pd.read_csv('all.csv', index_col=[14, 0], names=columnlist)

print(df)