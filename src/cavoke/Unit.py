from __future__ import annotations

from abc import abstractmethod
from typing import Callable, Tuple, List
from random import randrange

from .GameInfo import GameInfo
from .exceptions import *


class Unit(object):
    @property
    @abstractmethod
    def _unit_type(self) -> str:
        """
        Unit type property. :warning It's not just type(Unit), but the object type of unit. It's used for
        Unit.getDisplayDict() and is declared only in direct Unit inheritors (e.g. Image, Text).
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

        self.__unique = randrange(100000)

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

    def __hash__(self):
        # simple hash for checking if same Unit
        return hash(str(+hash(self.id) * 2 + hash(str(self.__unique)) * 3))

    @abstractmethod
    def fullHash(self):
        # complex hash for checking if unit had changed
        return hash(
            str(
                hash(self.name) * 3
                + hash(self.id) * 7
                + hash(str(self.x)) * 2
                + hash(str(self.y)) * 5
                + hash(str(self.w)) * 11
                + hash(str(self.h)) * 13
                + hash(str(self.__unique)) * 17
            )
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

    def setPosition(self, pos: Tuple[int, int]):
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

    def _addToCanvas(self, gameInfo: GameInfo, parents: list, x: int = 0, y: int = 0):
        """
        Function called when unit is added to canvas.
        :warning Do not call the function, unless you know what you're doing!  FIXME doxygen
        :param gameInfo: Info about parent game
        :param parents: Unit or game parents
        :param x: x coordinate
        :param y: y coordinate
        """
        # check if Unit is linked to another game
        if self.__gameInfo is not None:
            raise UnitGameOverrideWarning(self, gameInfo)
        # add self as parent for easier coding
        parents.append(self)

        # init Unit
        self.__gameInfo = gameInfo
        self.setCoordinates(x, y)
        self.__id = gameInfo.new_unit_id

        # add child to parents
        for i in range(len(parents) - 1):
            parents[i]._addChild(self, parents[i + 1])

    @property
    def name(self) -> str:
        return self.__name

    @property
    def id(self) -> str:
        return self.__id

    @property
    def pos(self) -> Tuple[int, int]:
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

    def setName(self, name: str):
        self.__name = name

    def setX(self, x: int):
        self.__x = x

    def setY(self, y: int):
        self.__y = y

    def setW(self, w: int):
        self.__w = w

    def setH(self, h: int):
        self.__h = h
