# dsp.py
import numpy as np
from config import *
from geometry import build_mic_positions

MIC_POS = build_mic_positions()

WINDOW = np.hanning(FRAME_SAMPLES)
FREQS = np.fft.rfftfreq(FRAME_SAMPLES, 1/FS)

LOW_IDX  = np.where((FREQS>=LOW_BAND[0]) & (FREQS<=LOW_BAND[1]))[0]
MID_IDX  = np.where((FREQS>=MID_BAND[0]) & (FREQS<=MID_BAND[1]))[0]
HIGH_IDX = np.where((FREQS>=HIGH_BAND[0])& (FREQS<=HIGH_BAND[1]))[0]

def compute_fft(signals):
    return np.fft.rfft(signals*WINDOW[:,None], axis=0)

def compute_bands(spec):
    mag2 = np.abs(spec)**2
    low  = mag2[LOW_IDX].sum(axis=0)
    mid  = mag2[MID_IDX].sum(axis=0)
    high = mag2[HIGH_IDX].sum(axis=0)
    return low, mid, high

def vad(low, mid, high):
    tot = (low+mid+high).sum()
    if tot < MIN_TOTAL_ENERGY: return False
    if mid.sum()/tot < MIN_MID_RATIO: return False
    return True

def gcc_phat(s1, s2):
    n = s1.size + s2.size
    S1 = np.fft.rfft(s1, n=n)
    S2 = np.fft.rfft(s2, n=n)
    R = S1 * np.conj(S2)
    R /= np.abs(R) + 1e-12
    cc = np.fft.irfft(R, n=n)

    maxs = n//2
    cc = np.concatenate((cc[-maxs:], cc[:maxs+1]))
    shifts = np.arange(-maxs, maxs+1)
    shift = shifts[np.argmax(cc)]
    return shift/FS

def compute_tdoa(signals):
    delays = []
    for i,j in DELAY_PAIRS:
        delays.append(gcc_phat(signals[:,i], signals[:,j])*FS)
    return np.array(delays)
