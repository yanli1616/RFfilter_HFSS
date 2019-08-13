from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
def plot(n,Wn,rp=0,rs=0,ftype='Butterworth',type='lowpass'):
    if ftype=='Butterworth':
        freq_response_b, freq_response_a = signal.butter(n, Wn, type, True, 'ba')
    elif ftype=='Chebyshev':
        freq_response_b, freq_response_a=signal.cheby1(n, rp, Wn, type, True, 'ba')
    elif ftype=='Elliptic':
        freq_response_b, freq_response_a=signal.ellip(n, rp, rs, Wn, type, True, 'ba')
    elif ftype=='Bessel':
        freq_response_b, freq_response_a=signal.bessel(n, Wn, type, True, 'ba')
    w, h = signal.freqs(freq_response_b, freq_response_a)
    plt.semilogx(w, 20 * np.log10(abs(h)))
    plt.title('filter frequency response')
    plt.xlim((2*np.pi*1e8,2*np.pi*1e10))
    plt.ylim((-200,0))
    plt.xlabel('Frequency [radians / second]')
    plt.ylabel('Amplitude [dB]')
    plt.margins(0, 0.1)
    plt.grid(which='both', axis='both')

    plt.show()
