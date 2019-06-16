from dataclasses import dataclass
from .Unit import Unit


@dataclass
class UnitCanvasInfo:
    unit: Unit
    prev_hash: int

