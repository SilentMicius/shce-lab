from dataclasses import dataclass, asdict
import hashlib
import json


@dataclass(frozen=True)
class ArchitectureGenome:
    """Machine-readable representation of one candidate architecture."""

    carrier: str
    secondary_carrier: str
    localization: str
    fingerprint: str
    routing: str
    sensor_policy: str
    coding: str
    homing: str
    map_resolution: str

    def canonical(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))

    @property
    def id(self) -> str:
        digest = hashlib.sha256(self.canonical().encode()).hexdigest()[:12].upper()
        return f"SHCE-{digest}"

    def to_dict(self) -> dict:
        return asdict(self)
