import numpy as np
import file_proc as fp
import matplotlib.pyplot as plt

ev = 27.2114
x1, y1 = fp.read_1d_file("../dipole/bromo-cm/4fs/low/butter.dat")
x2, y2 = fp.read_1d_file("../dipole/bromo-cm/4fs/band/butter.dat")
x3, y3 = fp.read_1d_file("../dipole/bromo-cm/4fs/high/butter.dat")

plt.plot(x1*ev, y1, label="low-pass")
plt.plot(x2*ev, y2, label="band-pass", ls="--")
plt.plot(x3*ev, y3, label="high-pass")

plt.legend()
plt.xlim((0,35))
plt.xlabel("Energy [ev]")
plt.show()
