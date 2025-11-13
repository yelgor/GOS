# process_file.py
import numpy as np
from dsp import compute_fft, compute_bands, vad, compute_tdoa
from localization import estimate_direction

if __name__ == "__main__":
    signals = np.load("generated_frame.npy")      # (256, 8)

    spec = compute_fft(signals)
    low, mid, high = compute_bands(spec)

    if not vad(low, mid, high):
        print("NO SPEECH")
        exit()

    delays = compute_tdoa(signals)
    res = estimate_direction(delays)

    if res is None:
        print("NO DIRECTION")
    else:
        az, el = res
        print("AZIMUTH :", round(az,2))
        print("ELEV    :", round(el,2))
