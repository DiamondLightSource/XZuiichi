#!/bin/bash

echo "Just have to python3 first..."
echo ""

module load python/3
module load xds

echo "Finding all XDS_ASCII files in ../"
echo ""

cd ..
find $(pwd) -name "XDS_ASCII.HKL" -type f -not -path '*/\.*' | sort
cd -

echo ""

time /home/i23user/bin/XSCALECombine/XZuiichi.py

grep -e "           CORRECTION FACTORS AS FUNCTION OF IMAGE NUMBER & RESOLUTION" -B 35 -e " ========== STATISTICS OF INPUT DATA SET ==========" -B 20 XSCALEOUT.LP > SHORTOUT.LP