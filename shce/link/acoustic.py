"""Minimal room-scale acoustic data link.

This module intentionally starts with a conventional, measurable baseline:
2-FSK over an audio carrier with a preamble and CRC. It is a test instrument
for the SHCE research loop, not a claim of a new physical communication law.
"""
from __future__ import annotations

import struct
import zlib

import numpy as np

MAGIC = b"SHCE1"
HEADER = struct.Struct(">5sIH")


def _bits(data: bytes) -> np.ndarray:
    return np.unpackbits(np.frombuffer(data, dtype=np.uint8))


def _bytes(bits: np.ndarray) -> bytes:
    usable = (len(bits) // 8) * 8
    return np.packbits(bits[:usable]).tobytes()


def frame(payload: bytes) -> bytes:
    checksum = zlib.crc32(payload) & 0xFFFFFFFF
    return HEADER.pack(MAGIC, checksum, len(payload)) + payload


def tone(freq: float, seconds: float, sample_rate: int, amplitude: float = 0.18) -> np.ndarray:
    n = max(1, int(seconds * sample_rate))
    t = np.arange(n, dtype=np.float32) / sample_rate
    return (amplitude * np.sin(2 * np.pi * freq * t)).astype(np.float32)


def encode(payload: bytes, sample_rate: int = 48000, f0: float = 4200.0,
           f1: float = 6200.0, symbol_seconds: float = 0.012,
           amplitude: float = 0.18) -> np.ndarray:
    """Return mono PCM samples for a low-volume 2-FSK room test."""
    preamble = np.tile(np.array([0, 1], dtype=np.uint8), 32)
    bits = np.concatenate([preamble, _bits(frame(payload))])
    symbols = [tone(f1 if bit else f0, symbol_seconds, sample_rate, amplitude)
               for bit in bits]
    guard = np.zeros(int(0.15 * sample_rate), dtype=np.float32)
    return np.concatenate([guard, *symbols, guard])
