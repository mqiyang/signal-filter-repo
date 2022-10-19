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
It reads in the matfiles molecule.pmat_re_*.dat, molecule.pmat_im_*.dat, molecule.dpmat_re_*.dat, molecule.dpmat_im_*.dat and output corresponding fil.*.dat
You need to modify:
- the size of your data set: itmax
- the time interval between your data: dt
- the window width (1/(cutoff/2pi)): width
- you can remove any of the d1types to fit your needs: d1types
- the path of the original and filtered signal: path
- set the third argument of calcWindow as true if you want to print out the window, it will generate window_*.dat in current directory
search for xxx for the locations

"""
itmax = 1000  #xxx the size of your data set
dt = 0.2  #xxx time interval between your data
t = np.array([it*dt for it in range(itmax)])

width = 1*41.341374575751  #xxx fs to au

d1types = ["pmat","dpmat"]  #xxx density and dpdt, you can choose one for your needs
d2types = ["re","im"]
spins = ["alpha","beta"]
path = ""  #xxx input path (same as output)

for d1type in d1types:
    for d2type in d2types:
        for spin in spins:
            mmap_fname = "memmap"+d1type+d2type+spin+".dat"
            matfname1 = path+fp.get_matfname('bromo',1, d1type, d2type, spin) #getting the dimentions
            header, nao, data = fp.read_mat(matfname1) #getting the dimentions
            mmap = np.memmap(mmap_fname,dtype='float32', mode='w+', shape=(itmax, (int(nao)*int(nao))))
                             
            #read in all the time steps
            for it in range(itmax): 
                matfname1 = path+fp.get_matfname('bromo',it+1, d1type, d2type, spin)
                header, nao, data = fp.read_mat(matfname1)
                print("Reading in " + matfname1)
                mmap[it, :] = data
                mmap.flush()

            for it, tval in enumerate(t): #build the rolling window and apply to each time step
                itChosen, tChosen = choseValues(tval, t, width)
                window = calcWindow(tChosen, it, False)  #xxx set to True to print window

                mmap.flush()
                valsChosen = mmap[itChosen]                

                transWindow = np.reshape(window, (len(window), 1))
                convVal = np.sum(valsChosen * transWindow, axis=0) # sum over time  

                matfname2 = fp.get_matfname('bromo',it+1, d1type, d2type, spin)
                print("Writing data to " + matfname2)
                fp.write_mat(header, nao, convVal, matfname2, cutoff=width)

                    
