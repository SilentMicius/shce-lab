import json
import sqlite3
from pathlib import Path


class Registry:
    """Persistent local registry of candidate architectures and experiments."""

    def __init__(self, path: str = "results/shce.sqlite"):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path)
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS architectures (
                id TEXT PRIMARY KEY,
                genome TEXT NOT NULL,
                score REAL,
                metrics TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )"""
        )
        self.db.commit()

    def save(self, genome, score: float, metrics: dict) -> None:
        self.db.execute(
            "INSERT OR REPLACE INTO architectures(id, genome, score, metrics) VALUES (?,?,?,?)",
            (genome.id, genome.canonical(), score, json.dumps(metrics)),
        )
        self.db.commit()
