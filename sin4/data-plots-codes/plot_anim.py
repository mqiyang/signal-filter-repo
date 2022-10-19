import numpy as np
import file_proc as fp
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import ImageMagickWriter

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
## Input
####################

t, vals = fp.read_1d_file("dipole/bromo-cm/ft_d.dat")
width = 1*41.341374575751  #fs to au

# give it and calculate the its value, chosen values and window.
it = 950
tval = t[it]
val = vals[it]

itChosen, tChosen = choseValues(tval, t, width)
window = calcWindow(tChosen, it, False)
valsChosen = vals[itChosen]
prod = valsChosen * window
convVal = np.sum(prod)


# do the static parts
fig, axs = plt.subplots(2,1)
axs0_0 = axs[0]
axs1_0 = axs[1]
axs0_0.set_ylim(0, 0.015)
axs1_0.set_ylim(0, 4.5)
# plot window plot
axs0_0.plot(tChosen, window, label = "w(t)", color="orange")
axs0_0.legend()
# plot signal 
axs1_0.plot(tChosen, valsChosen, label = "f(t)", color="#069AF3")
axs1_0.plot(tval, val, "o",  color="#FBDD7E")


# # create dynamical axes:
axs0_1 = axs0_0.twinx()
axs0_1.set_ylim(0, 0.015)
axs0_1.set_axis_off()
ani0_1, = axs0_1.plot([], [], "o", color = "#ADD8E6") #window point

axs1_1 = axs1_0.twinx()
axs1_1.set_ylim(0, 4.5)
axs1_1.set_axis_off()
ani1_1, = axs1_1.plot([], [], "o", color="#ADD8E6") #f(t) dot

axs1_2 = axs1_0.twinx()
ani1_2, = axs1_2.plot([], [], "o", color="#C79FEF")
axs1_2.set_ylim(-0.01, 0.07)
axs1_2.set_axis_off()  #f(x)*w(x) point

axs1_3 = axs1_0.twinx()
ani1_3, = axs1_3.plot([], [], label="f(x)*w(x)", color="#C79FEF") #f(x)*w(x) line
axs1_3.set_ylim(-0.01, 0.07)


def convAnimation(i):
    ani0_1.set_data(tChosen[i], window[i])
    ani1_1.set_data(tChosen[i], valsChosen[i])
    ani1_2.set_data(tChosen[i], prod[i])
    ani1_3.set_data(tChosen[0:i], prod[0:i])
    plt.fill_between(tChosen[0:i], prod[0:i],color="#E6E6FA", alpha=0.5 )
    if(i==len(tChosen)-1):
        axs[1].plot(tval, convVal, "o", color="#FC5A50")
        axs[1].annotate("filtered data", (tval+1.5, convVal-0.2), color="#FC5A50")
        plt.pause(10)
anim = animation.FuncAnimation(fig, convAnimation, frames=len(tChosen), interval=10, repeat_delay=50000, repeat=True)
anim.pause()
axs1_0.legend(loc="upper left")
axs1_3.legend(loc="upper right")
anim.save('conv-prod-animation.gif', writer=ImageMagickWriter(fps=10, extra_args=['-loop', '0']))
# plt.show()
