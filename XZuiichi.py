#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: christianorr
"""
import subprocess, sys, os
from itertools import combinations

# Python3 code to convert tuple into string 
def convertTuple(tup): 
    str =  ''.join(tup) 
    return str

print("""
__   __ ______      _ _      _     _
\ \ / /|___  /     (_|_)    | |   (_)
 \ V /    / / _   _ _ _  ___| |__  _
 /   \   / / | | | | | |/ __| '_ \| |
/ /^\ \./ /__| |_| | | | (__| | | | |
\/   \/\_____/\__,_|_|_|\___|_| |_|_|

              C ORR 2019
              """)

#Setup - probably a neater way of doing this...
path = os.getcwd()
print("You are here: " + path)
cut_or_comb = input("XZuiichi can test all possible (c)ombinations of the \
                    data or systematically (r)emove them in reverse order \
                    to analyse where signal drops. Type c for the \
                    combination option (takes MUCH longer for lots of data \
                    sets, best not to include more than 14 as this will\
                    take weeks+). Type r for the systematic removal \
                    option. *** ").lower
inpnumber = int(input("How many datasets are there? "))
inpnumberstatic = inpnumber
inpline = ("INPUT_FILE=")

#Kill script if only one dataset to be given
if (inpnumber > 1):
    print("")
else:
    print("There is no point running XZuiichi with only 1 input file...")
    sys.exit()

res = float(input("Resolution cutoff: "))
resgaps = ((5 - res) / 11)
shells = "10 5 "+str(round((res+(10*resgaps)), 1))+" "+ \
str(round((res+(9*resgaps)), 1))+" "+str(round((res+(8*resgaps)), 1))+" "+ \
str(round((res+(7*resgaps)), 1))+" "+str(round((res+(6*resgaps)), 1))+" "+ \
str(round((res+(5*resgaps)), 1))+" "+str(round((res+(4*resgaps)), 1))+" "+ \
str(round((res+(3*resgaps)), 1))+" "+str(round((res+(2*resgaps)), 1))+" "+ \
str(round((res+resgaps), 1))+" "+str(round(res, 1))
print("Because you gave a resolution of "+str(res)+" the resolution shells used are: "+str(shells))
print("")
quality = int(input("Score the diffraction quality 1-3 (1 is bad, 2 is okay, 3 is amazing): "))

#Set up the output log file
xscaleout = open("XSCALEOUT.LP","w")
xscaleout.write("XZuiichi\n")
xscaleout.close()

#Write the XSCALE input from user input
xscalePrep = open("XSCALEPREP.INP","w")
while (inpnumber > 0):
    inpnumber = inpnumber - 1
    dataline = input("Enter dataset: ")
    xscalePrep = open("XSCALEPREP.INP","a")
    xscalePrep.write(inpline)
    xscalePrep.write(dataline)
    xscalePrep.write("\n")
    xscalePrep.close()
else:
    inpnumber = inpnumberstatic
    print("That's all the inputs I am expecting!")

with open(dataline) as infile:
        for line in infile:
            if line.startswith("!SPACE_GROUP_NUMBER="):
                words = line.split()
                sg = words[-1]
                sg = int(sg)
            if line.startswith("!X-RAY_WAVELENGTH="):
                words = line.split()
                wavelen = words[-1]
                wavelen = float(wavelen)

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
print("Using a reflection/correction factor of "+str(ref_corr_fact))

#Write default XSCALE.INP commands -  can make this customisable in future
defaults = ("OUTPUT_FILE=XSCALE.HKL",
shells,
"FRIEDEL'S_LAW=FALSE",
"REFLECTIONS/CORRECTION_FACTOR="+ref_corr_fact,
"STRICT_ABSORPTION_CORRECTION=TRUE")
    
#Prep input for permutations
if cut_or_comb == "c":
    xscalePrep = open("XSCALEPREP.INP")
    lineprep = xscalePrep.readlines()
    print(lineprep)
    print(len(lineprep))
    print("")

#Loop through all combinations
if cut_or_comb == "c":
    for size in range(2,len(lineprep)+1):
        for i in combinations(lineprep,size):
            toRun = convertTuple(i)
            xscaleinp = open("XSCALE.INP","w")    
            for line in defaults:
                xscaleinp.write(line)
                xscaleinp.write("\n")
            xscaleinp.write(toRun)
            xscaleinp.close()
            subprocess.run(["xscale_par"])
            xscalelp = open("XSCALE.LP","r")
            xscaleout = open("XSCALEOUT.LP","a")
            xscaleout.write(xscalelp.read())
            xscaleout.close()
            xscalelp.close()
        
#Run XSCALE on input file and log output, delete last line of input file, repeat
if cut_or_comb == "r":
    inpnumberline = inpnumber
    xscaleinp = open("XSCALE.INP","a")
    for line in defaults:
        xscaleinp.write(line)
        xscaleinp.write("\n")
    infiles = open("XSCALEPREP.INP","r")
    xscaleinp.write(infiles.read())
    infiles.close()
    xscaleinp.close()
    while (inpnumber > 0):
        inpnumber = inpnumber - 1
        subprocess.run(["xscale_par"])      
        xscalelp = open("XSCALE.LP","r")
        xscaleout = open("XSCALEOUT.LP","a")
        xscaleout.write(xscalelp.read())
        xscaleout.close()
        xscalelp.close()
        readFile = open("XSCALE.INP")
        lines = readFile.readlines()
        readFile.close()
        xscaleinp = open("XSCALE.INP","w")
        xscaleinp.writelines([item for item in lines[:-1]])
        xscaleinp.close()
    else:
        print("Processing finished")