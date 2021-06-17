"""
@author: christianorr
"""
from datetime import datetime
import os
import sys
import subprocess
from pathlib import Path
import pickle
from operator import itemgetter
import pandas as pd
import seaborn as sns
import matplotlib


class best:
    def __init__(self):
        self.timestamp = datetime.now()
        self.path = os.getcwd()
        os.system("module load xds")

    def convertTuple(self, tup):
        str = "".join(tup)
        return str

    def get_input(self):
        print("You are here:", self.path)
        searchpath = input("Where to search for HKL files (abs or rel): ")
        hkl_list = list(Path(searchpath).rglob("*[I].[H][K][L]"))
        print("Found", len(hkl_list), "files")
        for a in hkl_list:
            print(a)
        self.inpnumber = int(input("\nNumber of datasets: "))
        if self.inpnumber > 1:
            self.inpnumberstatic = self.inpnumber
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
        self.reslist = [
            res1,
            res2,
            res3,
            res4,
            res5,
            res6,
            res7,
            res8,
            res9,
            res10,
            res11,
            res12,
            res13,
        ]
        self.shells = (
            "10 5 "
            + str(res3)
            + " "
            + str(res4)
            + " "
            + str(res5)
            + " "
            + str(res6)
            + " "
            + str(res7)
            + " "
            + str(res8)
            + " "
            + str(res9)
            + " "
            + str(res10)
            + " "
            + str(res11)
            + " "
            + str(res12)
            + " "
            + str(res13)
        )
        print(
            "Because you gave a resolution of "
            + str(res)
            + " the resolution shells used are: "
            + str(self.shells)
        )
        print("")
        quality = int(
            input(
                """Score the diffraction quality 1-3
                (1 is bad, 2 is okay, 3 is amazing): """
            )
        )
        xscalePrep = open("XSCALEPREP.INP", "w")
        inpline = "INPUT_FILE="
        while self.inpnumber > 0:
            self.inpnumber = self.inpnumber - 1
            dataline = input("Enter dataset: ")
            xscalePrep = open("XSCALEPREP.INP", "a")
            xscalePrep.write(inpline)
            xscalePrep.write(dataline)
            xscalePrep.write("\n")
            xscalePrep.close()
        else:
            print("\nThat's all the inputs I am expecting!")
        with open(dataline, "r") as infile:
            for line in infile:
                if line.startswith("!SPACE_GROUP_NUMBER="):
                    words = line.split()
                    sg = words[-1]
                    self.sg = int(sg)
                if line.startswith("!X-RAY_WAVELENGTH="):
                    words = line.split()
                    wavelen = words[-1]
                    self.wavelen = float(wavelen)
        if self.sg <= 2:
            sym = 1
        if 3 <= self.sg <= 15:
            sym = 2
        if 16 <= self.sg <= 74:
            sym = 3
        if 75 <= self.sg <= 167:
            sym = 4
        if 168 <= self.sg:
            sym = 5
        if self.wavelen <= 3:
            wav = 1
        if self.wavelen > 3:
            wav = 2
        self.ref_corr_fact = sym * wav * quality * 3
        print("\nUsing a reflection/correction factor of " + str(self.ref_corr_fact))
        if os.path.exists(os.path.join(self.path, "XSCALE.INP")):
            os.remove(os.path.join(self.path, "XSCALE.INP"))
        else:
            pass
        if os.path.exists(os.path.join(self.path, "all.csv")):
            os.remove(os.path.join(self.path, "all.csv"))
        else:
            pass
        self.defaults = (
            "OUTPUT_FILE=XSCALE.HKL",
            "RESOLUTION_SHELLS=" + str(self.shells),
            "FRIEDEL'S_LAW=FALSE",
            "MERGE=FALSE",
            "REFLECTIONS/CORRECTION_FACTOR=" + str(self.ref_corr_fact),
            "STRICT_ABSORPTION_CORRECTION=TRUE",
        )
        with open("XSCALE.INP", "a") as infile:
            for line in self.defaults:
                infile.write(line)
                infile.write("\n")
        xscale = open("XSCALE.INP", "a")
        xscalePrep = open("XSCALEPREP.INP", "r")
        for line in xscalePrep.readlines():
            xscale.write(line)


    def analyse(self, lp_file, res, name):
        with open(lp_file, "r") as file, open(
            (os.path.join(self.path, "tempout.csv")), "w"
        ) as out:
            for line in file:
                if line.lstrip().startswith(str(res) + "0 "):
                    line = (
                        line[0:51] + " " + line[51:62] + " " + line[62:89] + " " + line[89:]
                    )
                    out.write(",".join(line.split()) + "," + str(name) + "\n")
        with open((os.path.join(self.path, "tempout.csv")), "r") as file:
            dataline = file.read().splitlines(True)
        with open((os.path.join(self.path, "all.csv")), "a") as file:
            file.writelines(dataline[:1])

    def writepickle(self):
        print("Dumping pickle")
        with open("inps.pkl", "wb") as f:
            pickle.dump([self.reslist, self.n], f)

    def run_xscale_par(self):
        print("Running initial XSCALE")
        subprocess.run(["xscale_par"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def xdscc12_ify(self):
        print("Running xdscc12")
        subprocess.run(["xdscc12", "XSCALE.HKL"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(os.path.join(self.path, "XSCALE.INP")):
            os.rename(os.path.join(self.path, "XSCALE.INP"), os.path.join(self.path, "XSCALE.INP_original"))
        else:
            pass
        if os.path.exists(os.path.join(self.path, "XSCALE.LP")):
            os.rename(os.path.join(self.path, "XSCALE.LP"), os.path.join(self.path, "XSCALE.LP_original"))
        else:
            pass
        with open("XSCALE.INP.rename_me", "r") as infile, open("XSCALE.INP", "a") as outfile:
            for line in self.defaults:
                outfile.write(line)
                outfile.write("\n")
            for line in infile:
                if line.startswith("INPUT_FILE="):
                    outfile.write(line)
        self.n = 1
        ins = (self.inpnumberstatic - 1)
        while (self.inpnumberstatic - 1) > 0:
            print("XSCALE round", self.n, "of", ins)
            self.inpnumberstatic -= 1
            subprocess.run(["xscale_par"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            for j in self.reslist:
                self.analyse("XSCALE.LP", j, self.n)
            with open("XSCALE.INP", "r") as infile:
                lines = infile.readlines()
            with open("XSCALE.INP", "w") as infile:
                infile.writelines([line for line in lines[:-1]])
            self.n +=1
        with open((os.path.join(self.path, "all.csv")), "r") as file:
            data = file.read()
            data = data.replace("%", "")
            data = data.replace("*", "")
        with open((os.path.join(self.path, "all.csv")), "w") as file:
            file.write(data)

    def cudf_results(self):
        with open("inps.pkl", "rb") as f:
            ([self.reslist, self.n]) = pickle.load(f)
        data = pd.read_csv("all.csv", header=None, usecols=[0, 4, 8, 9, 10, 11, 12, 13, 14])
        data.columns = [
            "res",
            "completeness",
            "isigi",
            "rmeas",
            "cchalf",
            "anomcorr",
            "sigano",
            "nano",
            "ident",
        ]
        data.set_index(["ident", "res"], inplace=True)
        data.sort_index(inplace=True)
        sanity_pass = []
        for i in range(1, self.n, 1):
            for j in self.reslist:
                comp = data.loc[(i, j), "completeness"]
                isigi = data.loc[(i, j), "isigi"]
                rmeas = data.loc[(i, j), "rmeas"]
                cchalf = data.loc[(i, j), "cchalf"]
                ac = data.loc[(i, j), "anomcorr"]
                if (cchalf > 25):
                    sanity_pass += [(i, j, ac)]
                else:
                    continue
        best_results = []
        for k in self.reslist:
            m = []
            for l in (x for x in sanity_pass if x[1] == k):
                m += [(l)]
            try:
                ds = max(m, key=itemgetter(2))[0]
                bestano = max(m, key=itemgetter(2))[2]
                if bestano > 10:
                    print(
                        "To a resolution of",
                        k,
                        "the best run is",
                        ds,
                        "with an anomcorr of",
                        bestano,
                    )
                    best_results += [(k, bestano, ds)]
                else:
                    print(
                        "To a resolution of",
                        k,
                        "the best run is",
                        ds,
                        "but this has an anomcorr of",
                        bestano,
                        "which indicates this may not be suitable for phasing.",
                    )
                    best_results += [(k, bestano, ds)]
            except:
                print("No data at", k, "A passed the sanity check.")
        
            
if __name__ == "__main__":
    xzuiichi = best()
    xzuiichi.get_input()
    xzuiichi.run_xscale_par()
    xzuiichi.xdscc12_ify()
    xzuiichi.writepickle()
    xzuiichi.cudf_results()
