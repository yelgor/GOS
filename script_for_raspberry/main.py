# main.py

import numpy as np
import serial

from simulate_stm32 import simulate_signals
from dsp import compute_fft, compute_bands, vad, compute_tdoa
from localization import estimate_direction


# ========================================================
#  НАЛАШТУВАННЯ UART
# ========================================================

UART_PORT = "/dev/ttyAMA0"   # або "/dev/ttyS0", підстав свій
UART_BAUD = 115200


def main():

    # ====================================================
    # 1. SIMULATE STM32 → RAW MICROPHONE FRAME
    # ====================================================
    TRUE_AZ = 70.0
    TRUE_EL = 15.0

    signals = simulate_signals(TRUE_AZ, TRUE_EL)

    # ====================================================
    # 2. FULL DSP PIPELINE
    # ====================================================
    spec = compute_fft(signals)
    low, mid, high = compute_bands(spec)

    if not vad(low, mid, high):
        az, el = -1, -1   # немає мови → повертаємо -1
    else:
        delays = compute_tdoa(signals)
        result = estimate_direction(delays)

        if result is None:
            az, el = -1, -1
        else:
            az, el = result


    # ====================================================
    # 3. SERIAL OUTPUT (AZ, EL)
    # ====================================================
    msg = f"AZ={az:.2f} EL={el:.2f}\n"

    with serial.Serial(UART_PORT, UART_BAUD, timeout=1) as ser:
        ser.write(msg.encode("utf-8"))

    # Друкуємо на екран теж
    print("SENT:", msg)


if __name__ == "__main__":
    main()
