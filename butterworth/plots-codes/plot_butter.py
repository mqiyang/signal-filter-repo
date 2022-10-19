import numpy as np
import file_proc as fp
import matplotlib.pyplot as plt

fs = 41.341374575751
x1, y1 = fp.read_1d_file("../dipole/bromo-cm/ft_d.dat")

fig, axs = plt.subplots(2,1)
axs[0].plot(x1/fs, y1, label="unfiltered dipole")

x2, y2 = fp.read_1d_file("../dipole/bromo-cm/butter_ftd.dat")
axs[0].plot(x2/fs, y2, label="filtered dipole")

x3, y3 = fp.read_1d_file("../dipole/bromo-cm/4fs/butter_ftd.dat")
axs[1].plot(x1/fs, y1, label="unfiltered dipole")
axs[1].plot(x3/fs, y3, label="filtered dipole (4 fs)")
axs[1].plot(x2/fs, y2, label="filtered dipole (12 fs)")
axs[0].set_xlim(0,12)
axs[0].legend()
axs[1].set_xlim(0,4)
axs[1].set_xlabel("Time [fs]")
axs[1].legend()

plt.show()
