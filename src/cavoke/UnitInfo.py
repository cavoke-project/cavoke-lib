from dataclasses import dataclass
from .Unit import Unit


@dataclass
class UnitInfo:
    unit: Unit
    prev_hash: int
