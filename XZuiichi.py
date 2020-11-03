#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: christianorr
"""
import subprocess
import sys
import os
from itertools import combinations
from pathlib import Path
import pandas as pd
import shutil
import time
import math as m
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from operator import itemgetter
from statistics import mode
os.system("module load global/cluster >/dev/null 2>&1; module load xds")

if os.path.exists('all.csv'):
    os.remove('all.csv')
else:
    pass

# Python3 code to convert tuple into string
def convertTuple(tup):
    str = "".join(tup)
    return str


def analyse(lp_file, res, name):
    with open (lp_file, 'r') as file, open((os.path.join(path, 'tempout.csv')), 'w') as out:
        for line in file:
            if line.lstrip().startswith(str(res) + '0 '):
                out.write(','.join(line.split()) + ',' + str(name) + '\n')
    with open((os.path.join(path, 'tempout.csv')), 'r') as file:
        dataline = file.read().splitlines(True)
    with open((os.path.join(path, 'all.csv')), 'a') as file:
        file.writelines(dataline[:1])


print(
    """
__   __ ______      _ _      _     _
\ \ / /|___  /     (_|_)    | |   (_)
 \ V /    / / _   _ _ _  ___| |__  _
 /   \   / / | | | | | |/ __| '_ \| |
/ /^\ \./ /__| |_| | | | (__| | | | |
\/   \/\_____/\__,_|_|_|\___|_| |_|_|

              C ORR 2019
              """
)

path = os.getcwd()
print("Finding .HKL files nearby (../). If you don't see what you were expecting, try running XZuiichi up a directory\n")
hkl_list = list(Path("../").rglob("*[A][S][C][I][I].[H][K][L]"))
for a in hkl_list:
    print(os.path.join(path, a))
os.system("module load xds")
path = os.getcwd()
print("\nYou are here: " + path)
print(
    """\nXZuiichi can test all possible (c)ombinations of the
data or systematically (r)emove them in reverse order
to analyse where signal drops. Type c for the
combination option (takes MUCH longer for lots of data
sets, best not to include more than 14 as this will
take weeks+). Type r for the systematic removal
option.\n"""
)
big_zuiichi = str(input("Big Zuiichi?! ")).lower()
inpnumber = int(input("\nHow many datasets are there? "))

combination = 0

for r in range(2, inpnumber, 1):
    x = (m.factorial(inpnumber) / (m.factorial(r) * (m.factorial((inpnumber - r)))))
    combination = x + combination

combination = combination + 1

print("Based on " + str(inpnumber) + " input files, there are " + str(int(combination)) + " unique combinations of the data")

inpnumberstatic = inpnumber
inpline = "INPUT_FILE="
cut_or_comb = "c"

if inpnumber > 1:
    print("")
else:
    print("There is no point running XZuiichi with only 1 input file...")
    sys.exit()
res = float(input("Resolution cutoff: "))
resgaps = (5 - res) / 11
res1, res2, res3, res4, res5, res6, res7, res8, res9, res10, res11, res12, res13 = (
    10.0,
    5.0,
    round((res + (10 * resgaps)), 1),
    round((res + (9 * resgaps)), 1),
    round((res + (8 * resgaps)), 1),
    round((res + (7 * resgaps)), 1),
    round((res + (6 * resgaps)), 1),
    round((res + (5 * resgaps)), 1),
    round((res + (4 * resgaps)), 1),
    round((res + (3 * resgaps)), 1),
    round((res + (2 * resgaps)), 1),
    round((res + resgaps), 1),
    round(res, 1),
)
reslist = [res1, res2, res3, res4, res5, res6, res7, res8, res9, res10, res11, res12, res13]
shells = ("10 5 " + str(res3) + " " + str(res4) + " " + str(res5) + " " + str(res6) + " " + str(res7) + " " + str(res8) + " " + str(res9) + " " + str(res10) + " " + str(res11) + " " + str(res12) + " " + str(res13))
print(
    "Because you gave a resolution of "
    + str(res)
    + " the resolution shells used are: "
    + str(shells)
)
print("")
quality = int(
    input(
        """Score the diffraction quality 1-3
        (1 is bad, 2 is okay, 3 is amazing): """
    )
)

# Set up the output log file
xscaleout = open("XSCALEOUT.LP", "w")
xscaleout.write("XZuiichi\n")
xscaleout.close()

# Write the XSCALE input from user input
xscalePrep = open("XSCALEPREP.INP", "w")
while inpnumber > 0:
    inpnumber = inpnumber - 1
    dataline = input("Enter dataset: ")
    xscalePrep = open("XSCALEPREP.INP", "a")
    xscalePrep.write(inpline)
    xscalePrep.write(dataline)
    xscalePrep.write("\n")
    xscalePrep.close()
else:
    inpnumber = inpnumberstatic
    print("\nThat's all the inputs I am expecting!")
with open(dataline, "r") as infile:
    for line in infile:
        if line.startswith("!SPACE_GROUP_NUMBER="):
            words = line.split()
            sg = words[-1]
            sg = int(sg)
        if line.startswith("!X-RAY_WAVELENGTH="):
            words = line.split()
            wavelen = words[-1]
            wavelen = float(wavelen)

#decide onreflections per correction factor
if sg <= 2:
    sym = 1
if 3 <= sg <= 15:
    sym = 2
if 16 <= sg <= 74:
    sym = 3
if 75 <= sg <= 167:
    sym = 4
if 168 <= sg:
    sym = 5
if wavelen <= 3:
    wav = 1
if wavelen > 3:
    wav = 2
ref_corr_fact = sym * wav * quality * 3
print("\nUsing a reflection/correction factor of " + str(ref_corr_fact))

# Write XSCALE.INP commands 
defaults = (
    "OUTPUT_FILE=XSCALE.HKL",
    "RESOLUTION_SHELLS=" + str(shells),
    "FRIEDEL'S_LAW=FALSE",
    "REFLECTIONS/CORRECTION_FACTOR=" + str(ref_corr_fact),
    "STRICT_ABSORPTION_CORRECTION=TRUE",
)

# Write script file for qsub
xsp = (
    "module load xds",
    "xscale_par",
    "rm *.cbf XZu* XSCALE.HKL xsp.sh",
)

# Prep input for permutations
if cut_or_comb == "c":
    xscalePrep = open("XSCALEPREP.INP")
    lineprep = xscalePrep.readlines()
    print("")
#xs_df = pd.DataFrame(columns=('Resolution', 'ObsRef', 'UniRef', 'PosRef', 'Completeness', 'RObs', 'RExp', 'Compared', 'ISigI', 'RMeas', 'CCHalf', 'AnomCorr', 'SigAno', 'NAno'))

# Loop through all combinations - local machine
if cut_or_comb == "c" and big_zuiichi != "y":
    n = 1
    for size in range(2, len(lineprep) + 1):
        for i in combinations(lineprep, size):
            toRun = convertTuple(i)
            xscaleinp = open("XSCALE.INP", "w")
            for line in defaults:
                xscaleinp.write(line)
                xscaleinp.write("\n")
            xscaleinp.write(toRun)
            xscaleinp.close()
            ref = open("LIST_REF.OUT", "a")
            ref.write(str(n)+ "\n")
            ref.write(toRun + "\n")
            subprocess.run(["xscale_par"])
            xscalelp = open("XSCALE.LP", "r")
            for j in reslist:
                analyse("XSCALE.LP", j, n)
            xscaleout = open("XSCALEOUT.LP", "a")
            xscaleout.write(xscalelp.read())
            xscaleout.close()
            xscalelp.close()
            n = n + 1
    with open((os.path.join(path, 'all.csv')), 'r') as file:
        data = file.read()
        data = data.replace("%","")
        data = data.replace("*","")
    with open((os.path.join(path, 'all.csv')), 'w') as file:
        file.write(data)

# loop through all combinations - science cluster BIG ZUIICHI!
if cut_or_comb == "c" and big_zuiichi == "y":
    n = 1
    pbar = tqdm(desc="Submitting jobs", total=int(combination), dynamic_ncols=True)
    for size in range(2, len(lineprep) + 1):
        for i in combinations(lineprep, size):
            path_to_del = os.path.join(path, str(n))
            if os.path.exists(path_to_del):
                shutil.rmtree(path_to_del)
            if not os.path.exists(str(n)):
                os.mkdir(path_to_del)
            toRun = convertTuple(i)
            xscaleinp = open("./" + str(n) + "/XSCALE.INP", "w")
            for line in defaults:
                xscaleinp.write(line)
                xscaleinp.write("\n")
            xscaleinp.write(toRun)
            xscaleinp.close()
            xsp_write = open("./" + str(n) + "/xsp.sh", "w")
            for line in xsp:
                xsp_write.write(line)
                xsp_write.write("\n")
            xsp_write.close()
            os.chmod(os.path.join(path, str(n)) + "/xsp.sh", 0o775)
            os.system("cd ./" + str(n) + "; qsub -P i23 -N XZu_" + str(n) + " -pe smp 4 -cwd xsp.sh >/dev/null 2>&1")
            pbar.update(1)
            pbar.refresh()
            n = n + 1
    q = subprocess.Popen("qstat", stdout=subprocess.PIPE)
    q = len(q.stdout.read())
    print("")
    pbar = tqdm(desc="Jobs finished", total=int(combination), dynamic_ncols=True)   
    while q > 2:
        t = subprocess.Popen("qstat", stdout=subprocess.PIPE)
        q = len(t.stdout.readlines())
        l = combination - (q - 2)
        pbar.n = int(l)
        pbar.refresh()
        time.sleep(2)
    else:
        print("\nDone processing, moving on to analysis")

if cut_or_comb == "c" and big_zuiichi == "y":
    n = 1
    print("")
    pbar = tqdm(desc="Analysing", total=int(combination), dynamic_ncols=True)
    for size in range(2, len(lineprep) + 1):
        for i in combinations(lineprep, size):
            for j in reslist:
                analyse(str(n) + "/XSCALE.LP", j, n)
            pbar.n = int(n)
            pbar.refresh()
            n = n + 1
    with open((os.path.join(path, 'all.csv')), 'r') as file:
        data = file.read()
        data = data.replace("%","")
        data = data.replace("*","")
    with open((os.path.join(path, 'all.csv')), 'w') as file:
        file.write(data)

# XSCALE on input file and log output, delete last line of input file, repeat
if cut_or_comb == "r":
    inpnumberline = inpnumber
    xscaleinp = open("XSCALE.INP", "a")
    for line in defaults:
        xscaleinp.write(line)
        xscaleinp.write("\n")
    infiles = open("XSCALEPREP.INP", "r")
    xscaleinp.write(infiles.read())
    infiles.close()
    xscaleinp.close()
    while inpnumber > 0:
        inpnumber = inpnumber - 1
        subprocess.run(["xscale_par"])
        xscalelp = open("XSCALE.LP", "r")
        xscaleout = open("XSCALEOUT.LP", "a")
        xscaleout.write(xscalelp.read())
        xscaleout.close()
        xscalelp.close()
        readFile = open("XSCALE.INP")
        lines = readFile.readlines()
        readFile.close()
        xscaleinp = open("XSCALE.INP", "w")
        xscaleinp.writelines([item for item in lines[:-1]])
        xscaleinp.close()
    else:
        print("Processing finished")

data = pd.read_csv("all.csv", header=None, engine='c', usecols=[0, 4, 8, 9, 10, 11, 12, 13, 14])
data.columns = ['res', 'completeness', 'isigi', 'rmeas', 'cchalf', 'anomcorr', 'sigano', 'nano', 'ident']
data.set_index(['ident', 'res'], inplace=True)
data.sort_index(inplace=True)

sanity_pass = []
for i in range(1, int(combination), 1):
    for j in reslist:
        comp = data.loc[(i, j), 'completeness']
        isigi = data.loc[(i, j), 'isigi']
        rmeas = data.loc[(i, j), 'rmeas']
        cchalf = data.loc[(i, j), 'cchalf']
        ac = data.loc[(i, j), 'anomcorr']
        if (comp > 80) & (isigi > 1) & (rmeas < 100) & (cchalf > 25):
            sanity_pass += [(i, j, ac)]
        else:
            continue

id, res, ano = 0, 1, 2

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
fig.savefig('ResolutionVsAnomcorr.jpg', dpi=600)

best_run = mode(c_val)
print('\nThe best run appears to be number', best_run)

os.mkdir(path + 'best')
shutil.copy2(os.path.join(path, best_run) + '/XSCALE.INP', os.path.join(path, 'best'))
subprocess.run(["xscale_par"], cwd=os.path.join(path, 'best'))

if cut_or_comb == "c" and big_zuiichi == "y":
    print("")
    pbar = tqdm(desc="Cleaning up", total=int(combination))
    for i in range(1, int(combination) + 1, 1):
        path_to_del = os.path.join(path, str(i))
        if os.path.exists(path_to_del):
            shutil.rmtree(path_to_del)
            pbar.refresh()

print("\nXZuiichi finished. Best data can be found in the folder 'best'")