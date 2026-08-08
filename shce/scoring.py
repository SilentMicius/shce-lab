def score_trials(trials):
    """Return a transparent multi-objective score and raw metrics."""
    count = len(trials)
    success = sum(t["success"] for t in trials) / count
    error = sum(t["position_error"] for t in trials) / count
    energy = sum(t["energy"] for t in trials) / count

    localization = max(0.0, 1.0 - min(error / 100.0, 1.0))
    energy_efficiency = 1.0 / (1.0 + energy / 100.0)
    robustness = success
    score = (
        0.40 * localization
        + 0.35 * robustness
        + 0.25 * energy_efficiency
    )

    return score, {
        "localization": localization,
        "robustness": robustness,
        "energy_efficiency": energy_efficiency,
        "mean_error": error,
        "mean_energy": energy,
        "success_rate": success,
    }
