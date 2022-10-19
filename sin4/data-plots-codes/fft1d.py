import numpy as np
import file_proc as fp

x, y = fp.read_1d_file("window/bromo-cm/window_1000.dat")
# x = np.linspace(-10, 10, 201)
# y = np.sin(x*np.pi/41.341)**4
# for ix, iy in zip(x,y):
#     print("{0:.8f}\t{1:.8f}".format(ix, iy))
dx = x[1] - x[0]
k = np.fft.fftshift(np.fft.fftfreq(len(x), d=dx))*np.pi*2
fft_y = np.fft.fftshift(np.fft.fft(y))
for ix, iy in zip(k,fft_y):
    print("{0:.8f}\t{1:.8f}\t{2:.8f}\t{3:.8f}".format(ix, np.real(iy), np.imag(iy), np.abs(iy)))

