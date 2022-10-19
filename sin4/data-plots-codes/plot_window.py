import numpy as np
import file_proc as fp
import matplotlib.pyplot as plt

fs = 41.341374575751
x, y = fp.read_1d_file("window/bromo-cm/window_1000.dat")

fig, ax = plt.subplots()
ax.plot(x/fs, y, label="$w(t_c=4.83fs)$")
ind = np.where(x==199.8)
plt.vlines(x = 199.8/fs, ymin=0, ymax = y[ind],
           colors = 'black', ls="--",
           label = '$t_c=4.83fs$')

x, y = fp.read_1d_file("window/bromo-cm/window_0.dat")
ax.plot(x/fs, y, label="$w(t_c=0fs)$")
# plt.vlines(x = 199.8/fs, ymin=0, ymax = y[0],
#            colors = 'black', ls="--",
#            label = '$t_c=0fs$')
ax.set_ylim(0, 0.027)
ax.set_xlim(0, 7)
ax.set_xlabel("Time [fs]")
plt.legend()
plt.show()
