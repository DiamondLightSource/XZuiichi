#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: christianorr
"""
import subprocess
import sys
import os
from itertools import combinations
from itertools import islice

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
inpnumber = input("How many datasets are there? ")
inpnumberstatic = inpnumber
inpnumberstaticint = int(inpnumber)
inpnumber = int(inpnumber)
inpnumberline = inpnumber
inpline = ("INPUT_FILE=")

#Kill script if only one dataset to be given
if (inpnumber > 1):
    print("")
else:
    print("There is no point running crimp with only 1 input file...")
    sys.exit()

#Write default XSCALE.INP commands -  can make this customisable in future
defaults = ("OUTPUT_FILE=XSCALE.HKL",
"RESOLUTION_SHELLS=10 5 4 3.8 3.6 3.4 3.2 3 2.8 2.6 2.5 2.4 2.3 2.2 2.1 2.0",
"!INCLUDE_RESOLUTION_RANGE=",
"!MERGE=TRUE",
"FRIEDEL'S_LAW=FALSE",
"REFLECTIONS/CORRECTION_FACTOR=10",
"!STRICT_ABSORPTION_CORRECTION=TRUE")

#Set up the output log file
xscaleout = open("XSCALEOUT.LP","w")
xscaleout.write("Welcome to XYZ!")
xscaleout.write("\n")
xscaleout.close()

#Write the XSCALE input from user input
xscalePrep = open("XSCALEPREP.INP","w")
while (inpnumberline > 0):
    inpnumberline = inpnumberline - 1
    dataline = input("Enter dataset: ")
    xscalePrep = open("XSCALEPREP.INP","a")
    xscalePrep.write(inpline)
    xscalePrep.write(dataline)
    xscalePrep.write("\n")
    xscalePrep.close()
else:
    print("That's all the inputs I am expecting!")

print("Check XSCALE.INP...")

cont = input("Okay to continue? (y/n): ")
if cont == "y":
    print("Moving on...")
else:
    sys.exit()
    
#Prep input for permutations
xscalePrep = open("XSCALEPREP.INP")
lineprep = xscalePrep.readlines()
print(lineprep)
print(len(lineprep))
print("")

#Loop through all combinations
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

        #with open(path + "/XSCALE.LP", "r") as f:
        #    for line in f:
        #        if line == "CONTROL CARDS":
        #            xscaleout = open("XSCALEOUT.LP","a")
        #            xscaleout.write(''.join(islice(f, 8)))
        #            xscaleout.close()
        
        
        #=======================================================================
        # with open(path + '/XSCALE.LP', 'r') as f:
        #     for line in f:
        #         if line == 'CONTROL CARDS\n':
        #             for i in range(8):
        #                 print(next(lines).strip())
        
         

        
        #=======================================================================

        # 
        #=======================================================================
        
