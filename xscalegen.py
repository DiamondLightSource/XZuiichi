#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 16:46:33 2019

@author: christianorr
"""
import subprocess

defaults = ("OUTPUT_FILE=XSCALE.HKL",
"RESOLUTION_SHELLS=20 10 8 6 4 3 2.5 2.2 2.1 2 1.9 1.8 1.7 1.6 1.5 1.4 1.3 1",
"!INCLUDE_RESOLUTION_RANGE=",
"!MERGE=TRUE",
"!FRIEDEL'S_LAW=FALSE",
"!REFLECTIONS/CORRECTION_FACTOR=50",
"!STRICT_ABSORPTION_CORRECTION=TRUE")

inpnumber = input("How many datasets are there? ")
inpnumber = int(inpnumber)
inpline = ("INPUT_FILE=../")

xscaleinp = open("XSCALE.INP","w")
    
for line in defaults:
    xscaleinp.write(line)
    xscaleinp.write("\n")
xscaleinp.close()

xscaleinp = open("XSCALE.INP","a")

for i in range(inpnumber):
    xscaleinp.write(inpline)
    xscaleinp.write("\n")
xscaleinp.close()

print("Modify XSCALE.INP file with the correct paths")

cont = input("Okay to continue? (y/n): ")
if cont == "y":
    print("Moving on...")
else:
    exit(0)

#subprocess.run(["module load xds"])
subprocess.run(["xscale_par"])
