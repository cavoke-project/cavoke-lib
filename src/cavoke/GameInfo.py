from dataclasses import dataclass


@dataclass
class GameInfo:
    canvas_repr: str
    new_unit_id: str