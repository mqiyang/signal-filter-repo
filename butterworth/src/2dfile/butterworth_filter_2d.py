# this script read in the input file and apply the filter to the data
# be mindful that the butterworth filter will make the tail of your data bad, so run longer that what you need
# eg: run 130au if you need the data in 100au (it will depend the data you have)
# via Mengqi Yang
# ------------------------------
# You need to specify:
# - ecut: your cutoff energy in eV
# - ecut2: need to specify if you want to use band pass
# - dt: the time-interval in your data set
# - fname_in: the path of your input file
# - fil_type: the type of the butterworth: "low" for low-pass, "high" for high-pass, "band" for band-pass
# - output: it will automatically generates the filtered signal in time domain and it's FTed data, the FTed data of original signal,
#           and the freq response of the butter. you can turn some of them off by commenting the corresponding blocks.
# You can search xxx for the part you can customize.
import sig_proc as sp
import file_proc as fp
import numpy as np
from scipy import signal 


ev = 27.2114
ecut = 4 #xxx you can change your cutoff energy here (eV)
ecut2 = None #xxx need to specify when using band pass: [ecut:ecut2]
dt = 0.2 #xxx time-interval between each data
fname_in = ""  #xxx you can change the input file name here 
fil_type = "low"  #xxx you can change it to different filter type: "high", "band"

cutoff = ecut/ev
cutoff2 = ecut2/ev if ecut2 else None
fs = int(1/dt) * 2 * np.pi 
x, y = fp.read_1d_file(fname_in) 

#xxx get the original FT data, you can comment this block to turn if off
fft_ya = sp.fft1d(y)
freqs, dk = sp.calc_freqs(x, dt)
fp.write_1d_file(freqs, np.abs(fft_ya), "fw_d.dat") 

#xxx get the freq response of the butter filter, you can comment this block to turn if off
w, h = sp.show_filter(fil_type,  fs, cutoff, sec_cut=cutoff2)
fp.write_1d_file(w, np.abs(h), "butter.dat") 

# get the filtered data in time domain
yb = sp.apply_butter_filter(y, fil_type, fs, cutoff, sec_cut=cutoff2)
fp.write_1d_file(x, yb, "butter_ftd.dat")

#xxx get the FT filtered data, you can comment this block to turn if off
fft_yb = sp.fft1d(yb)
freqs, dk = sp.calc_freqs(x, dt)
fp.write_1d_file(freqs, np.abs(fft_yb), "butter_fwd.dat")
