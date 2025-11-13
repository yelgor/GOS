# geometry.py
import numpy as np
from config import MIC_RADIUS, Z_BOTTOM, Z_TOP, BOTTOM_ANGLES_DEG, TOP_ANGLES_DEG

BOTTOM_ANGLES = np.radians(BOTTOM_ANGLES_DEG)
TOP_ANGLES = np.radians(TOP_ANGLES_DEG)

def build_mic_positions():
    pos = []
    for a in BOTTOM_ANGLES:
        pos.append([MIC_RADIUS*np.cos(a), MIC_RADIUS*np.sin(a), Z_BOTTOM])
    for a in TOP_ANGLES:
        pos.append([MIC_RADIUS*np.cos(a), MIC_RADIUS*np.sin(a), Z_TOP])
    return np.array(pos, float)
