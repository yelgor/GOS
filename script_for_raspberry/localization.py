# localization.py
import numpy as np
from config import FS, C_SOUND, DELAY_PAIRS
from geometry import build_mic_positions

MIC_POS = build_mic_positions()

def estimate_direction(delays):
    b = C_SOUND*(delays/FS)
    A = []
    for (i,j), dt in zip(DELAY_PAIRS, b):
        A.append(MIC_POS[j]-MIC_POS[i])
    A = np.vstack(A)

    s, *_ = np.linalg.lstsq(A, b, rcond=None)
    n = np.linalg.norm(s)
    if n < 1e-6: return None
    s /= n

    az = np.degrees(np.arctan2(s[1], s[0]))
    if az < 0: az += 360
    el = np.degrees(np.arcsin(np.clip(s[2], -1, 1)))

    return az, el
