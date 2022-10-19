#OA this script read in the input file and apply the filter to the data
# be mindful that the butterworth filter will make the tail of your data bad, so run longer that what you need
# eg: run 130au if you need the data in 100au (it will depend the data you have)
# via mengqi
import sig_proc as sp
import file_proc as fp
import numpy as np
from scipy import signal 

ev = 27.2114
ecut = 4 #ev #xxx you can change your cutoff energy here
ecut2 = 0
cutoff = ecut/ev
cutoff2 = None
dt = 0.2 #change here
fs = int(1/dt) * 2 * np.pi 

file_path = "../dipole/bromo-cm/4fs/"  #xxx you can change the input file path here (fw_d, lpf, lpf_ftd, lpf_fwd will be in the same folder)
fname_in = file_path + "4fs-ft_d.dat"  #xxx you can change the input file name here 
# get the original FFT data  #xxx this is not neccessary except for the read in
x, y = fp.read_1d_file(fname_in) 
fft_ya = sp.fft1d(y)
freqs, dk = sp.calc_freqs(x, dt)
fp.write_1d_file(freqs, np.abs(fft_ya), file_path + "fw_d.dat") 

# test the low-pass-filter
w, h = sp.show_filter("low",  fs, cutoff, sec_cut=cutoff2)
fp.write_1d_file(w, np.abs(h), file_path + "butter.dat")  #xxx this prints what the filter looks like in freq

yb = sp.apply_butter_filter(y, "low", fs, cutoff, sec_cut=cutoff2)
fft_yb = sp.fft1d(yb)
fp.write_1d_file(freqs, np.abs(fft_yb), file_path + "butter_fwd.dat")
fp.write_1d_file(x, yb, file_path + "butter_ftd.dat")
