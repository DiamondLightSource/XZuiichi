import subprocess
import sys
import os
import pandas as pd

path = os.getcwd()
print(path)

res1, res2, res3, res4, res5, res6, res7, res8, res9, res10, res11, res12, res13 = 10.0, 5.0, 4.8, 4.6, 4.5, 4.3, 4.1, 3.9, 3.7, 3.5, 3.4, 3.2, 3.0

lp = input('Where is the LP file? ')
print(lp)

def analyse(lp_file, res):
    with open (lp_file, 'r') as file, open((os.path.join(path, 'tempout.csv')), 'w') as out:
        for line in file:
            if line.startswith(str(res) + "0"):
                out.write(','.join(line.split()) + '\n')
    with open((os.path.join(path, 'tempout.csv')), 'r') as file:
        dataline = file.read().splitlines(True)
    with open((os.path.join(path, 'out.csv')), 'a') as file:
        file.writelines(dataline[:1])

reslist = [res1, res2, res3, res4, res5, res6, res7, res8, res9, res10, res11, res12, res13]

for i in reslist:
    analyse(lp, reslist)