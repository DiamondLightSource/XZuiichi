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


# Python3 code to convert tuple into string
def convertTuple(tup):
    str = "".join(tup)
    return str


def analyse(lp_file, res, name):
    with open (lp_file, 'r') as file, open((os.path.join(path, 'tempout.csv')), 'w') as out:
        for line in file:
            if line.lstrip().startswith(str(res) + '0'):
                out.write(','.join(line.split()) + '\n')
    with open((os.path.join(path, 'tempout.csv')), 'r') as file:
        dataline = file.read().splitlines(True)
    with open((os.path.join(path, name + '.csv')), 'a') as file:
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

hkl_list = list(Path("../").rglob("*.[H][K][L]"))
print(hkl_list)

# Setup - probably a neater way of doing this...
os.system("module load xds")
path = os.getcwd()
p = Path(path)
os.system('find ' + str(p.parent) + ' "XDS_ASCII.HKL" -type f -not -path "*/\.*" | sort')
print("You are here: " + path)
print( 
    """XZuiichi can test all possible (c)ombinations of the
data or systematically (r)emove them in reverse order
to analyse where signal drops. Type c for the
combination option (takes MUCH longer for lots of data
sets, best not to include more than 14 as this will
take weeks+). Type r for the systematic removal
option. """
)
inpnumber = int(input("How many datasets are there? "))
inpnumberstatic = inpnumber
inpline = "INPUT_FILE="
cut_or_comb = "c"

# Kill script if only one dataset to be given
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
    print("That's all the inputs I am expecting!")
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
print("Using a reflection/correction factor of " + str(ref_corr_fact))

# Write XSCALE.INP commands 
defaults = (
    "OUTPUT_FILE=XSCALE.HKL",
    "RESOLUTION_SHELLS=" + str(shells),
    "FRIEDEL'S_LAW=FALSE",
    "REFLECTIONS/CORRECTION_FACTOR=" + str(ref_corr_fact),
    "STRICT_ABSORPTION_CORRECTION=TRUE",
)

# Prep input for permutations
if cut_or_comb == "c":
    xscalePrep = open("XSCALEPREP.INP")
    lineprep = xscalePrep.readlines()
    print(lineprep)
    print(len(lineprep))
    print("")
#xs_df = pd.DataFrame(columns=('Resolution', 'ObsRef', 'UniRef', 'PosRef', 'Completeness', 'RObs', 'RExp', 'Compared', 'ISigI', 'RMeas', 'CCHalf', 'AnomCorr', 'SigAno', 'NAno'))

# Loop through all combinations
if cut_or_comb == "c":
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
            ref.write(str(size )+ "\n")
            ref.write(toRun + "\n")
            subprocess.run(["xscale_par"])
            xscalelp = open("XSCALE.LP", "r")
            for j in reslist:
                analyse("XSCALE.LP", j, size)
            xscaleout = open("XSCALEOUT.LP", "a")
            xscaleout.write(xscalelp.read())
            xscaleout.close()
            xscalelp.close()

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
