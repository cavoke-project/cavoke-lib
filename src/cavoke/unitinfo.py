from dataclasses import dataclass

from .unit import Unit


@dataclass
class UnitInfo:
    unit: Unit
    prev_hash: int
