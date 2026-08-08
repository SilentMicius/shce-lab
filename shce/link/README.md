# Room-scale link experiment

Milestone R1 is deliberately simple: transmit a short digital payload from a PC speaker and recover it with a separate receiver microphone in another room.

The baseline uses 2-FSK in the audible band, CRC32 framing and a known preamble. The purpose is to establish a reproducible physical channel and measure:

- packet success rate
- bit error rate
- received SNR
- latency
- range through walls/doors
- sensitivity to orientation and reflections

Only after this baseline is measurable should alternative carriers or the SHCE geospatial fingerprint layer be introduced. Keep playback volume low and do not test high-intensity ultrasound.
