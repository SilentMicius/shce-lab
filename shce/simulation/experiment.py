import numpy as np


def run_trial(genome, world, start, target, rng, noise=0.08, max_steps=120):
    """Run one synthetic homing trial and return measurable outcomes."""
    position = np.array(start, dtype=float)
    target = np.array(target, dtype=float)
    target_fingerprint = world.fingerprint(target)

    for step in range(max_steps):
        candidates = []
        for angle in np.linspace(0, 2 * np.pi, 16, endpoint=False):
            candidate = np.clip(
                position + [np.cos(angle), np.sin(angle)], 0, world.size
            )
            error = np.linalg.norm(world.fingerprint(candidate) - target_fingerprint)
            candidates.append((error, candidate))

        _, best = min(candidates, key=lambda item: item[0])
        movement = best - position
        norm = np.linalg.norm(movement)
        if norm:
            movement /= norm

        drift = {
            "magnetic": 0.015,
            "acoustic": 0.035,
            "rf": 0.025,
            "hybrid": 0.012,
            "optical": 0.020,
        }.get(genome.carrier, 0.04)

        position = np.clip(
            position + movement + rng.normal(0.0, drift, 2), 0, world.size
        )
        if np.linalg.norm(position - target) < 2.0:
            return {
                "success": 1,
                "position_error": float(np.linalg.norm(position - target)),
                "steps": step + 1,
                "energy": float(step + 1),
            }

    return {
        "success": 0,
        "position_error": float(np.linalg.norm(position - target)),
        "steps": max_steps,
        "energy": float(max_steps),
    }
