import numpy as np


class SyntheticWorld:
    """Deterministic synthetic geospatial fingerprint field for experiments."""

    def __init__(self, size=100.0, seed=42):
        self.size = float(size)
        self.rng = np.random.default_rng(seed)

    def fingerprint(self, position):
        x, y = position
        return np.array([
            np.sin(x / 11.0) + 0.7 * np.cos(y / 17.0) + 0.25 * np.sin((x + y) / 7.0),
            0.4 * np.cos(x / 23.0) + 0.6 * np.sin(y / 19.0),
            0.5 * np.sin(x / 8.0) * np.cos(y / 13.0),
            np.sin((2.0 * x - y) / 15.0),
            np.cos((x + y) / 10.0),
        ])

    def noisy_fingerprint(self, position, noise=0.08):
        return self.fingerprint(position) + self.rng.normal(0.0, noise, 5)
