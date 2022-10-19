"""
A python version of a low-pass-filter using sin^4 window function.
Original version: Matlab @ Francios
@ Mengqi
# Create the window for each timestep and apply to the data
# 1) set this timestep as the center of 1fs window
# 2) find left(tStart) and right boundary (tEnd) of this window with +/-0.5fs ==> tChosen
# 3) calculate this window function
#   - rescaled by (right boundary - left boundary)
#   - shifted with left boundart
#   - normalized by the sum
# 4) do the dot production and sum (convolution step)
# Note: when t is smaller than 0.5fs or larger than t[-1]-0.5fs the window witdh is smaller than 1fs

"""

import numpy as np
import file_proc as fp

def choseValues(tCenter, t, width):
    """
    find left(tStart) and right boundary (tEnd) of this window with +/-0.5fs ==> tChosen and the vals in that range
    """
    tval = tCenter
    tStart = tval - width*0.5
    tEnd = tval + width*0.5
    itChosen = np.where((t >= tStart) & (t <= tEnd))
    tChosen = t[itChosen]
    return itChosen, tChosen


def calcWindow(tChosen, itCenter, lwrite_window=False):
    """
    calculate this window function
    - rescaled by (right boundary - left boundary)
    - shifted with left boundart
    - normalized by the sum
    """
    window = np.sin(np.pi*(tChosen-tChosen[0])/(tChosen[-1]-tChosen[0]))**4 # window function of 1fs
    window /= window.sum()

    if lwrite_window:
        fout2 = "window_" + str(itCenter) + ".dat"
        with open(fout2, 'w') as f2:
            for x, y in zip(tChosen, window):
                f2.write("{0:.8E}\t{1:.8E}\n".format(x, y))

    return window

def print_tChosen(tCenter, tChosen):
    print("tChosen[0], tChosen[-1]: ", tChosen[0],  tChosen[-1])
    print("tChosen[1]-tChosen[0]: ", tChosen[-1]-tChosen[0])


####################
## Main
####################
"""
It reads in the volumetric cube files and store it in the memmap data structure, and then apply filter to the data and generate the filtered cube with specified output names
You need to modify:
- the size of your data set: nt
- the time interval between your data: dt
- the window width (1/(cutoff/2pi)): width
- the list of input cube filenames: finlist
- the list of output cube filenames: outlist
- set the third argument of calcWindow as true if you want to print out the window, it will generate window_*.dat in current directory
search for xxx for the locations

"""
nt = 999  #xxx size of your data set
dt = 0.2  #time interval between your data
t = np.array([it*dt for it in range(nt)])

width = 1*41.341374575751  #window width

finlist = [ './'+str(i+1).zfill(10)+'.cube' for i in range(nt) ]  #xxx list of input cube file names. eg. co.density.0000000001.cube
outlist = [ './'+str(i+1).zfill(10)+'.cube' for i in range(nt) ] #xxx list of output cube file names. eg. fil.co.density.0000000001.cube

mmap_fname = "memmap.dat"
nx, ny, nz, data, meta = fp.read_cube(finlist[0])     # get the size for the memmap
mmap = np.memmap(mmap_fname,dtype='float32', mode='w+', shape=(nt, (nx*ny*nz)))

for it in range(nt): # read in the cube data from all time steps
    print("Reading in " + str(it+1) + "it...")
    fname = finlist[it]
    nx, ny, nz, data, meta = fp.read_cube(fname)
    mmap[it, :] = data

for it, tval in enumerate(t):
    print("Processing data from " + str(it+1) + "it...")

    itChosen, tChosen = choseValues(tval, t, width)
    window = calcWindow(tChosen, it, False)  #xxx set to True if you want to save the window data

    valsChosen = mmap[itChosen]
    transWindow = np.reshape(window, (len(window), 1))
    convVal = np.sum(valsChosen * transWindow, axis=0) # sum over time

    print("Writing data to " + str(it+1) + "it...")
    fp.write_cube(np.reshape(convVal, (nx,ny,nz)), meta, outlist[it])




