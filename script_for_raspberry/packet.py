# packet.py
import struct
from dataclasses import dataclass
from typing import List

# Формат структури UART пакета (little-endian, без вирівнювання)
PACKET_STRUCT_FMT = "<BBH 8H 8H 8h B 4b 4b 4H"
PACKET_SIZE = struct.calcsize(PACKET_STRUCT_FMT)

@dataclass
class Packet:
    frame_id: int
    rms: List[int]
    peak: List[int]
    mean: List[int]
    vad: int
    drms: List[int]
    delay: List[int]
    low: int
    mid: int
    high: int
    checksum: int

def parse_packet(data: bytes) -> Packet | None:
    """Розбір UART-пакету у Python об'єкт."""
    if len(data) != PACKET_SIZE:
        return None

    unpacked = struct.unpack(PACKET_STRUCT_FMT, data)

    h1, h2 = unpacked[0], unpacked[1]
    if h1 != ord('G') or h2 != ord('S'):
        return None  # неправильний заголовок

    frame_id = unpacked[2]
    rms  = list(unpacked[3:11])
    peak = list(unpacked[11:19])
    mean = list(unpacked[19:27])
    vad  = unpacked[27]
    drms = list(unpacked[28:32])
    delay = list(unpacked[32:36])
    low, mid, high, checksum = unpacked[36:40]

    # TODO: додати перевірку checksum, коли визначимо формулу
    return Packet(
        frame_id, rms, peak, mean, vad, drms, delay,
        low, mid, high, checksum
    )
