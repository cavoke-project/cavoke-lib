from __future__ import annotations

from abc import abstractmethod
from typing import Callable

from .GameInfo import GameInfo
from .exceptions import *


class Unit(object):
    def __init__(self, name: str = "", w=50, h=50, initPayload: dict = {}):
        self.name = name
        self.id = None
        self.__gameInfo = None

        self.pos = (0, 0)
        self.x = 0
        self.y = 0

        self.w = w
        self.h = h
        self.payload = initPayload

    def __repr__(self):
        if self.__gameInfo is None:
            return (
                "<name="
                + (self.name if self.name else "[no name given]")
                + "; class="
                + str(self.__class__)
                + "; no game linked>"
            )
        else:
            return (
                "<id="
                + self.id
                + "; name="
                + self.name
                + "; class="
                + str(self.__class__)
                + "; game="
                + self.__gameInfo.game_repr
                + "; pos="
                + repr(self.pos)
                + ">"
            )

    @abstractmethod
    def __hash__(self):
        return hash(
            hash(self.name)
            + hash(self.id)
            + hash(self.x)
            + hash(self.y)
            + hash(self.w)
            + hash(self.h)
        )

    @abstractmethod
    def getDisplayDict(self):
        return {
            "name": self.name,
            "type": self._unit_type,
            "id": self.id,
            "position": {"x": self.x, "y": self.y},
            "size": {"w": self.w, "h": self.h},
        }

    def setOnClick(self, onClick: Callable[[], None]):
        self.click = onClick
        self.clickable = True

    @abstractmethod
    def click(self) -> None:
        pass

    def setOnDrag(self, onDrag: Callable[[Unit], None]):
        self.drag = onDrag
        self.draggable = True

    @abstractmethod
    def drag(self, toUnit) -> bool:
        pass

    def setCoordinates(self, x, y):
        if self.__gameInfo is None:
            raise NoGameWarning
        self.x = x
        self.y = y
        self.pos = (x, y)

    def setPosition(self, pos: tuple):
        if len(pos) != 2:
            raise ValueError("pos must contain two numbers: x and y coordinates")
        self.setCoordinates(pos[0], pos[1])

    def moveBy(self, dx, dy):
        self.setCoordinates(self.x + dx, self.y + dy)

    def _addToCanvas(self, gameInfo: GameInfo, x=0, y=0):
        if self.__gameInfo is None:
            self.__gameInfo = gameInfo
            self.setCoordinates(x, y)
            self.id = gameInfo.new_unit_id
        else:
            raise UnitGameOverrideWarning(self, gameInfo)

    @property
    @abstractmethod
    def _unit_type(self) -> str:
        pass
