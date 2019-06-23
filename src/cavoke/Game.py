from __future__ import annotations

from abc import abstractmethod
from math import floor
from typing import Callable, Tuple, List

from .GameInfo import GameInfo
from .GameStatus import GameStatus
from .Unit import Unit
from .UnitInfo import UnitInfo
from .exceptions import *


class Game(object):
    def __init__(
        self,
        game_name: str,
        creator: str,
        w: int = 680,
        h: int = 480,
        init_payload=None,
    ):
        """
        Constructor for Game class
        :param game_name: Game name
        :param creator: Creator name/username
        :param w: Canvas width
        :param h: Canvas height
        :param init_payload: initial payload of the game
        """
        if init_payload is None:
            init_payload = {}

        self.__game_name = game_name
        self.__creator = creator
        self.__payload = init_payload

        self.__w = w
        self.__h = h

        self.__units = {}
        self.__ids_register = {}
        self.__prevHashUnitsDict = {}
        self.__childToDirectChild = {}

    def __repr__(self):
        return (
            '<"' + self.game_name + '" game built using cavoke by ' + self.creator + ">"
        )

    # TODO add timer for game

    def addUnit(self, unit: Unit, x: int = 0, y: int = 0) -> str:
        """
        Adds unit to game's memory
        :param unit: unit to be added
        :param x: x coordinate
        :param y: y coordinate
        :return: unit's new id
        """
        if len(self.__units) >= 2 ** 16:
            raise GameUnitsCountExceededWarning

        unitId = self.__appointId(unit, x, y)
        # +1 to make __units store different prev_hash, so when getDisplayDict() is called, the unit repr will be
        # generated
        self.__units[unit.id] = UnitInfo(unit, unit.fullHash() + 1)
        return unitId

    def addUnits(
        self, *units: Unit, x: int = 0, y: int = 0, horizontally: bool = True
    ) -> list[str]:
        """
        Adds units to game's memory horizontally or vertically
        :param units: units to be added
        :param x: x start coordinate
        :param y: y start coordinate
        :param horizontally:
        :return: list of units' new ids
        """
        res = []
        for e in units:
            res.append(self.addUnit(e, x, y))
            if horizontally:
                x += e.w
            else:
                y += e.h
        return res

    def addUnitList(
        self, unit_list: List[Unit], x: int = 0, y: int = 0, horizontally: bool = True
    ) -> List[str]:
        """
        Adds units to game's memory horizontally or vertically
        :rtype: List[str]
        :param unit_list: list of units to be added
        :param x: x start coordinate
        :param y: y start coordinate
        :param horizontally:
        :return: list of units' new ids
        """
        return self.addUnits(*unit_list, x=x, y=y, horizontally=horizontally)

    def getDisplayList(self) -> List[Unit]:
        """
        Gets the list of units to be displayed on canvas
        :rtype: List[Unit]
        :return: list of Units
        """
        res = self.__prevHashUnitsDict
        for k, e in self.__units.items():
            if not isinstance(e, UnitInfo):
                raise GameUnitsArrayTypeWarning
            if e.prev_hash == e.unit.fullHash():
                continue
            unit: Unit = e.unit
            self.__units[unit.id].prev_hash = unit.fullHash()
            self.__add_and_parse_unit(res, unit)
        return [y for x, y in res.items()]

    def getResponse(self) -> dict:
        """
        Produces the response for client-side
        :rtype: dict
        :return: response as dict according to ../../schemas/schema.json
        """
        return {
            "status": "OK",
            "response": {
                "game": {
                    "name": self.game_name,
                    "author": self.creator,
                    "gameId": "47e7ce50763101ef364ea7a5dc6b1c57f99797037fab7d62437ca1674b3fe35a",  # FIXME
                    "status": self.checkGameStatus().name,
                    "display": {
                        "canvas": {
                            "w": self.w,
                            "h": self.h,
                            "contents": self.getDisplayList(),
                        }  # ,  FIXME
                        # "alert_box": {
                        #   "text": "123123"
                        # },
                        # "text_input": {
                        #   "message_to_player": "Guess the password!"
                        # }
                    },
                }
            },
        }

    def clickUnitId(self, unitId: str):
        """
        Click on unit by unit's id
        [!!!] Used by server
        :param unitId: unit's id
        :return: gets response for client-side
        """
        unit = self.findUnitById(unitId)
        direct_child = self.__childToDirectChild[unit]
        if is_unit_list(direct_child):
            direct_child.click(unit)
        else:
            direct_child.click()
        return self.getResponse()

    def clickCoordinates(self, x: int, y: int):
        """
        Click unit by coordinates
        :param x: x coordinate
        :param y: y coordinate
        :return: response for client-sied
        """
        for e, c in self.__ids_register.items():
            for i in range(c)[::-1]:
                unit = self.__units[e + "_" + str(i)]
                if unit.x <= x <= unit.x + self.w and unit.y <= y <= unit.y + self.h:
                    if is_unit_list(unit):
                        unit.clickCoordinates(x, y)
                    else:
                        unit.click()
        return self.getResponse()

    def clickPos(self, pos: tuple):
        """
        Click unit by position
        :param pos: position (tuple of two ints: x and y coordinates)
        :return: response for client-side
        """
        if len(pos) != 2:
            raise ValueError("pos must contain two numbers: x and y coordinates")
        return self.clickCoordinates(pos[0], pos[1])

    @abstractmethod
    def checkGameStatus(self) -> GameStatus:
        """
        Abstract method for checking the game status
        :return: GameStatus
        """
        return GameStatus.UNKNOWN

    def findUnitByLambda(self, f: Callable[[Unit], bool]) -> Unit:
        """
        Finds unit by filter-lambda :param f: filter-lambda function. Type: Callable[[Unit], bool]. Accepts Unit as
        argument and returns boolean: true if found, false if not :return: first unit, that satisfies filter-lambda
        function, or if none raises UnitNotFoundError
        """
        # BFS
        searchQueue = self.getAllUnits()
        while searchQueue:
            unit: Unit = searchQueue.pop(0)
            if f(unit):
                return unit
            if is_unit_list(unit):
                searchQueue += list(unit)
        raise UnitNotFoundError

    def findUnitByName(self, name: str) -> Unit:
        """
        Finds unit by name
        :param name: name
        :return: Unit
        :sa Game.findUnitByLambda() FIXME doxygen
        """
        return self.findUnitByLambda(lambda unit: unit.name == name)

    def findUnitById(self, unitId: str):
        """
        Finds unit by id
        :param unitId: unit's id
        :return: Unit
        :sa Game.findUnitByLambda() FIXME doxygen
        """
        return self.findUnitByLambda(lambda unit: unit.id == unitId)

    def getAllUnits(self) -> List[Unit]:
        """
        Gets all units in game's memory. :warning Unit-lists not expanded! FIXME doxygen
        :rtype: List[Unit]
        :return: returns list of units
        """
        return [y.unit for x, y in self.__units.items()]

    def __add_and_parse_unit(self, d: dict, unit: Unit, depth=0):
        """

        :param d:
        :param unit:
        :param depth:
        """
        if depth > 2 ** 16:
            raise GameAddUnitDepthExceededWarning
        # if unit is unit-list, then give every unit separately
        if is_unit_list(unit):
            for e in unit:
                if not isinstance(e, Unit):
                    raise GameUnitsArrayTypeWarning
                # recursion is safe as depth is increasing
                self.__add_and_parse_unit(d, e, depth + 1)
        else:
            d[unit.id] = unit.getDisplayDict()

    def __appointId(
        self, unit: Unit, x: int = None, y: int = None, depth=0, parent=None
    ) -> str:
        """
        Appoints id for unit (even unit-list) and registers game for every unit and sub-unit
        :param unit: Unit for registering
        :param x: x coordinate for unit
        :param y: y coordinate for unit
        :param depth: recursion depth (must be <= 256 or else - exception)
        :return: returns units unitId as str
        """
        if not parent:
            parent = [self]
        # check recursion depth
        if depth > 2 ** 8:
            raise GameAddUnitDepthExceededWarning

        # appoint an id
        className = type(unit).__name__
        if className in self.__ids_register:
            idx = self.__ids_register[className]
            self.__ids_register[className] += 1
            unitId = className + "_" + str(idx)
        else:
            self.__ids_register[className] = 1
            unitId = className + "_0"

        # register the unit
        gameInfo = GameInfo(repr(self), unitId)
        if x is None and y is None:
            x, y = unit.x, unit.y

        unit._addToCanvas(gameInfo, parent, x, y)

        # if unit is unit-list, then process every unit separately
        if is_unit_list(unit):
            k = len(unit)
            for i in range(k):
                e = unit[i]
                if not isinstance(e, Unit):
                    raise GameUnitsArrayTypeWarning
                # recursion is safe as depth is increasing
                if unit.isHorizontal:
                    self.__appointId(
                        e,
                        x + floor(unit.w * i / k),
                        y,
                        depth + 1,
                        parent.copy() + [unit],
                    )
                else:
                    self.__appointId(
                        e,
                        x,
                        y + floor(unit.h * i / k),
                        depth + 1,
                        parent.copy() + [unit],
                    )
        return unitId

    def _addChild(self, child: Unit, direct_child: Unit) -> None:
        self.__childToDirectChild[child] = direct_child

    @property
    def game_name(self):
        return self.__game_name

    @property
    def creator(self):
        return self.__creator

    @property
    def payload(self):
        return self.__payload

    @property
    def w(self):
        return self.__w

    @property
    def h(self):
        return self.__h

    @property
    def units(self):
        return self.__units


def is_unit_list(unit) -> bool:
    """
    Checks if unit is unit-list
    :param unit: test subject
    :return: returns boolean if is unit-list
    """
    return isinstance(unit, Unit) and isinstance(unit, list)
