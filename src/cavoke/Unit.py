from __future__ import annotations

from abc import abstractmethod
from typing import Callable

from .GameInfo import GameInfo
from .exceptions import *


class Unit(object):
    @property
    @abstractmethod
    def _unit_type(self) -> str:
        """
        Unit type property. :warning It's not just type(Unit), but the object type of unit. It's used for
        Unit.getDisplayDict() and is declared only in direct Unit inherents (e.g. Image, Text). FIXME typo
        Do not change it, unless you know what you're doing!
        """
        pass

    def __init__(self, name: str = "", w: int = 50, h: int = 50, init_payload=None):
        """
        Constructor for Unit
        :param name: unit name
        :param w: unit width
        :param h: unit height
        :param init_payload: initial unit payload
        """
        if init_payload is None:
            init_payload = {}
        self.__name = name
        self.__id = None
        self.__gameInfo = None

        self.__x = 0
        self.__y = 0
        self.__w = w
        self.__h = h

        self.payload = init_payload

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

    @property
    @abstractmethod
    def draggable(self) -> bool:
        """
        Boolean if player can drag the unit around
        :return: returns boolean
        """
        return False

    @abstractmethod
    def getDisplayDict(self):
        """
        Gets display info for unit for Game.getDisplayList()
        :return: dict of values
        """
        return {
            "name": self.name,
            "type": self._unit_type,
            "id": self.id,
            "position": {"x": self.x, "y": self.y},
            "size": {"w": self.w, "h": self.h},
            "draggable": self.draggable,
        }

    def setOnClick(self, onClick: Callable[[], None]) -> None:
        """
        Sets click function
        :param onClick: function
        """
        self.click = onClick

    @abstractmethod
    def click(self) -> None:
        """
        Abstract click function. Called when clicked on unit.
        """
        pass

    def setOnDrag(self, onDrag: Callable[[Unit], None]) -> None:
        """
        Sets drag function
        :param onDrag: function
        """
        self.drag = onDrag

    @abstractmethod
    def drag(self, toUnit: Unit) -> bool:
        """
        Abstract drag function. Called when clicked on unit.
        :param toUnit: unit which self is dragged to.
        :return: :important boolean: true if dragged successfully, false if not dragged  FIXME doxygen
        """
        pass

    def setCoordinates(self, x: int, y: int):
        """
        Sets new position of unit
        :param x: x coordinate
        :param y: y coordinate
        """
        if self.__gameInfo is None:
            raise NoGameWarning
        self.__x = x
        self.__y = y

    def setPosition(self, pos: tuple):
        """
        Sets new position of unit
        :param pos: tuple of coordinates: (x, y)
        """
        if len(pos) != 2:
            raise ValueError("pos must contain two numbers: x and y coordinates")
        self.setCoordinates(pos[0], pos[1])

    def moveBy(self, dx: int, dy: int):
        """
        Moves unit by desired values
        :param dx: shift in x coordinate
        :param dy: shift in y coordinate
        """
        self.setCoordinates(self.x + dx, self.y + dy)

    def _addToCanvas(self, gameInfo: GameInfo, x=0, y=0):
        """
        Function called when unit is added to canvas.
        :warning Do not call the function, unless you know what you're doing!  FIXME
        :param gameInfo: GameInfo
        :param x: x coordinate
        :param y: y coordinate
        """
        if self.__gameInfo is None:
            self.__gameInfo = gameInfo
            self.setCoordinates(x, y)
            self.__id = gameInfo.new_unit_id
        else:
            raise UnitGameOverrideWarning(self, gameInfo)

    @property
    def name(self):
        return self.__name

    @property
    def id(self):
        return self.__id

    @property
    def pos(self):
        return self.x, self.y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def w(self):
        return self.__w

    @property
    def h(self):
        return self.__h
