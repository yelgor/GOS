# simulate_stm32.py
import numpy as np
from config import FS, FRAME_SAMPLES, C_SOUND
from geometry import build_mic_positions

MIC_POS = build_mic_positions()

def simulate_signals(az_deg, el_deg, freq=1000):
    az = np.radians(az_deg)
    el = np.radians(el_deg)
    s = np.array([np.cos(el)*np.cos(az),
                  np.cos(el)*np.sin(az),
                  np.sin(el)])

    delays = (MIC_POS @ s) / C_SOUND
    t = np.arange(FRAME_SAMPLES)/FS

    sig = []
    for d in delays:
        sig.append(0.8*np.sin(2*np.pi*freq*(t - d)))

    return np.array(sig).T.astype(np.float32)

if __name__ == "__main__":
    TRUE_AZ = 70
    TRUE_EL = 15

    signals = simulate_signals(TRUE_AZ, TRUE_EL)
    np.save("generated_frame.npy", signals)

    print("Generated frame saved to generated_frame.npy")
