import random
from .core.genome import ArchitectureGenome

OPTIONS = {
    "carrier": ["magnetic", "acoustic", "rf", "hybrid", "optical"],
    "secondary_carrier": ["none", "magnetic", "acoustic", "rf"],
    "localization": ["particle_filter", "bayesian", "kalman"],
    "fingerprint": ["magnetic+terrain", "magnetic+gravity", "terrain+rf", "multi_field"],
    "routing": ["astar", "dijkstra", "information_astar"],
    "sensor_policy": ["adaptive", "all", "minimal"],
    "coding": ["none", "error_correction", "spread_spectrum"],
    "homing": ["gradient", "particle_homing", "potential_field"],
    "map_resolution": ["coarse", "adaptive", "fine"],
}


def random_genome(rng=random):
    return ArchitectureGenome(**{key: rng.choice(values) for key, values in OPTIONS.items()})


def mutate(genome, rng=random):
    data = genome.to_dict()
    key = rng.choice(list(OPTIONS))
    data[key] = rng.choice(OPTIONS[key])
    return ArchitectureGenome(**data)


def crossover(a, b, rng=random):
    da, db = a.to_dict(), b.to_dict()
    data = {key: (da[key] if rng.random() < 0.5 else db[key]) for key in da}
    return ArchitectureGenome(**data)
