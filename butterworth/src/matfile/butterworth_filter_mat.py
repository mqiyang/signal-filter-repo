# this script read in the input file and apply the filter to the data
# be mindful that the butterworth filter will make the tail of your data bad, so run longer that what you need
# eg: run 130au if you need the data in 100au (it will depend the data you have)
# via Mengqi Yang
# ------------------------------
# You need to specify:
# - ecut: your cutoff energy in eV
# - ecut2: need to specify if you want to use band pass, default to None for high/low
# - dt: the time-interval in your data set
# - itmin: the min time index for given data, it's default set 1 (it=1 ==> t=0)
# - itmax: the max time index for given data
# - molecule: the molecule name in the cubefile fname: eg, "co" in co.density.0000000001.cube
# - ftype: the file type in the cubefile fname: eg, "density" in co.density.0000000001.cube
# - fil_type: the type of the butterworth: "low" for low-pass, "high" for high-pass, "band" for band-pass
# - d1types: the file type of the mat files
# - d2types: the data type of the mat files
# - spins: the spin type of the mat files
# - output: it will automatically overwrites the original mats with the filtered one
# You can search xxx for the part you can customize.

import sig_proc as sp
import file_proc as fp
import numpy as np
from scipy import signal 

ev = 27.2114
ecut = 20  #xxx you can change your cutoff energy here (eV)
ecut2 = None #xxx need to specify when using band pass: [ecut:ecut2]
dt = 0.06 #xxx the time-interval in your data set
itmin = 1  #xxx the min time index for given data, it's default set 1 (it=1 ==> t=0)
itmax = 1001  #xxx the max time index for given data
molecule = '' #xxx eg, "co" in co.density.0000000001.cube
ftype = '' #xxx eg, "density" in co.density.0000000001.cube
fil_type = '' #xxx "low" for low-pass, "high" for high-pass, "band" for band-pass

d1types = ["pmat","dpmat"]  #xxx the file type of the mat files
d2types = ["re","im"]  #xxx the data type of the mat files
spins = ["alpha","beta"]  #xxx the spin type of the mat files

cutoff = ecut/ev
cutoff2 = ecut2/ev if ecut2 else None
fs = int(1/dt) * 2 * np.pi 


for d1type in d1types:
    for d2type in d2types:
        for spin in spins:
            mmap_fname = "memmap"+d1type+d2type+spin+".dat"
            matfname = fp.get_matfname(molecule,1, d1type, d2type, spin) #getting the dimentions
            header, nao, data = fp.read_mat(matfname) #getting the dimentions
            mmap = np.memmap(mmap_fname,dtype='float32', mode='w+', shape=(itmax, (int(nao)*int(nao))))

            #read in all the time steps
            for it in range(itmin,itmax+1):
                matfname = fp.get_matfname(molecule,it, d1type, d2type, spin)
                header, nao, data = fp.read_mat(matfname)
                print("Reading file", matfname,"...")
                mmap[it, :] = data
                mmap.flush()


            for iy in range(mmap.shape[1]):
                y = mmap[:, iy]
                fil_y = sp.apply_butter_filter(y, fil_type, fs, cutoff, sec_cut=cutoff2)
                print("Filtering the #{} element".format(iy))
                mmap[:, iy] = fil_y

            for it in range(itmin, itmax+1):
                matfname = fp.get_matfname(molecule,it, d1type, d2type, spin)
                fp.write_mat(header, nao, mmap[it-1], matfname, cutoff)
                print("Writing in file", matfname,"...")

