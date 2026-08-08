import argparse
import random

import numpy as np

from .core.registry import Registry
from .discovery import crossover, mutate, random_genome
from .scoring import score_trials
from .simulation.experiment import run_trial
from .simulation.world import SyntheticWorld


def main():
    parser = argparse.ArgumentParser(prog="shce")
    parser.add_argument("--population", type=int, default=40)
    parser.add_argument("--generations", type=int, default=5)
    parser.add_argument("--trials", type=int, default=20)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    py_rng = random.Random(args.seed)
    np_rng = np.random.default_rng(args.seed)
    world = SyntheticWorld(seed=args.seed)
    registry = Registry()
    population = [random_genome(py_rng) for _ in range(args.population)]

    for generation in range(args.generations):
        ranked = []
        for genome in population:
            trials = []
            for _ in range(args.trials):
                start = np_rng.uniform(0, world.size, 2)
                target = np_rng.uniform(0, world.size, 2)
                trials.append(run_trial(genome, world, start, target, np_rng))
            score, metrics = score_trials(trials)
            registry.save(genome, score, metrics)
            ranked.append((score, genome, metrics))

        ranked.sort(key=lambda item: item[0], reverse=True)
        print(f"Generation {generation + 1}/{args.generations}")
        for score, genome, metrics in ranked[:3]:
            print(
                f"  {genome.id} score={score:.4f} "
                f"success={metrics['success_rate']:.1%} "
                f"error={metrics['mean_error']:.2f}"
            )

        elite = ranked[: max(2, len(ranked) // 5)]
        population = [item[1] for item in elite]
        while len(population) < args.population:
            a = py_rng.choice(elite)[1]
            if py_rng.random() < 0.35:
                b = py_rng.choice(elite)[1]
                child = crossover(a, b, py_rng)
            else:
                child = a
            population.append(mutate(child, py_rng))


if __name__ == "__main__":
    main()
