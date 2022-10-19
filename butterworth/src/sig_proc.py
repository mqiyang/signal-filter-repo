# https://stackoverflow.com/questions/25191620/creating-lowpass-filter-in-scipy-understanding-methods-and-units#
# https://en.wikipedia.org/wiki/Butterworth_filter
from scipy.signal import butter, filtfilt, freqz
import numpy as np

def butter_low_pass(order, cutoff, fs):
    """
    This function applies the filter to the data set
    Parameters:
    order -- the order of the butterworth filter
    norm_cutoff -- the cutoff energy normed with fs/nyq
    """    
    return butter(order, cutoff, btype='low', analog=False, output='ba', fs=fs)


def butter_band_pass(order, lowcut, highcut, fs):
    print([lowcut, highcut])
    return butter(order, [lowcut, highcut], btype='band', analog=False, output='ba', fs=fs)


def butter_high_pass(order, cutoff, fs):
    """
    This function applies the filter to the data set
    Parameters:
    order -- the order of the butterworth filter
    norm_cutoff -- the cutoff energy normed with fs/nyq
    """    
    return butter(order, cutoff, btype='high', analog=False, output='ba', fs=fs)


def apply_butter_filter(data, ftype, fs, cut, sec_cut=None, order=5):
    """
    This function applies the filter to the data set
    Parameters:
    data -- the data to be filtered
    ftype -- the type of the filter, here only implement low-pass and band-pass
    cut -- the lowcut or highcut energy in rad/s, set to None in defaut
    sec_cut -- the high cutoff energy in rad/s when band energy is specified
    fs -- the sampling frequency
    order -- the order of the butterworth filter
    Note: there is no need to normalize the cutoff with nyq since it will handle it automatically with given fs
    Note: the band pass filter cannot process small energy range, lowcut - highcut should be large enough (in my test case the diff is 3)
    """
    if (ftype == "band"):
        if (not sec_cut):
            raise Exception("lowcut needs to be specified for band pass for applying the filter")
        else:
            b, a = butter_band_pass(order, cut, sec_cut, fs)
    elif(ftype == "low"):        
        if (sec_cut):
            raise Exception("cannot specify lowcut for low band pass")
        else:
            b, a = butter_low_pass(order, cut, fs)
            print("Applied low pass")
    elif(ftype == "high"):        
        if (sec_cut):
            raise Exception("cannot specify highcut for low band pass")
        else:
            b, a = butter_high_pass(order, cut, fs)
            print("Applied high pass")
    else:
        raise Exception("Valid filter type for applying: low, high, band")
    y = filtfilt(b, a, data)
    return y


def show_filter(ftype, fs, cut, sec_cut=None, order=5):
    if (ftype == "band"):
        if (not sec_cut):
            raise Exception("lowcut needs to be specified for band pass for showing the filter")
        else:
            b, a = butter_band_pass(order, cut, sec_cut, fs)
    elif(ftype == "high"):        
        b, a = butter_high_pass(order, cut, fs)
        
    elif(ftype == "low"):        
        b, a = butter_low_pass(order, cut, fs)
    else:
        raise Exception("Valid filter type for showing: low, high, band")
    return freqz(b, a, fs=fs, worN=2000)
    
    
def damp_func(x, y, tau):
    y = y * np.exp(-(x/tau))


def fft1d(y):
    return np.fft.fftshift(np.fft.fft(y))


def calc_freqs(x, dt):
    freqs = np.fft.fftshift(np.fft.fftfreq(len(x), d=dt)) * 2 * np.pi  # engineer freqs to angular freqs
    dk = freqs[1] - freqs[0]
    return freqs, dk


# ev = 27.2114
# x, y = read_1d_file("ft_d.dat")
# tau = 0
# ecut = 20

# dt = x[1] - x[0]
# tmax = x[-1]
# fs = int(1 / dt)
# nyq = 0.5 * fs
# cutoff = ecut / ev  #/ (2*np.pi)

# # get the original FFT data
# fft_ya = np.fft.fftshift(np.fft.fft(y))
# freqs = np.fft.fftshift(np.fft.fftfreq(len(x), d=dt)) * 2 * np.pi 
# write_1d_file(freqs, np.abs(fft_ya), "fw_d.dat")

# yb = butter_low_pass_filter(y, nyq, cutoff, fs)
# write_1d_file(x, yb, "filtered_ftd.dat")
# fft_yb = np.fft.fftshift(np.fft.fft(yb))
# write_1d_file(freqs, np.abs(fft_yb), "filtered_fwd.dat")
