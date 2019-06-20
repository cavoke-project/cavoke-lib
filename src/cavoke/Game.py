from __future__ import annotations

from typing import Callable
from abc import abstractmethod
from math import floor

from .exceptions import *
from .Unit import Unit
from .GameInfo import GameInfo
from .UnitInfo import UnitInfo
from .GameStatus import GameStatus


def is_unit_list(unit) -> bool:
    return isinstance(unit, Unit) and isinstance(unit, list)


class Game(object):
    def __init__(self, game_name: str, creator: str, w: int = 680, h: int = 480, initPayload: dict = {}):
        self.game_name = game_name
        self.creator = creator
        self.payload = initPayload

        self.w = w
        self.h = h

        self.__units = {}
        self.__ids_register = {}
        self.__prevHashUnitsDict = {}

        self.__winCondition = lambda *args: None

    def __repr__(self):
        return '<"' + self.game_name + '" game built using cavoke by ' + self.creator + '>'

    def __appointId(self, unit: Unit, x=None, y=None, depth=0):
        if depth > 2 ** 16:
            raise GameAddUnitDepthExceededWarning

        # appoint an id
        className = type(unit).__name__
        if className in self.__ids_register:
            idx = self.__ids_register[className]
            self.__ids_register[className] += 1
            unitId = className + '_' + str(idx)
        else:
            self.__ids_register[className] = 1
            unitId = className + '_0'

        # register the unit
        gameInfo = GameInfo(repr(self), unitId)
        if x is None and y is None:
            x, y = unit.x, unit.y
        unit._addToCanvas(gameInfo, x, y)

        # if unit is unit-list, then give every unit separately
        if is_unit_list(unit):
            k = len(unit)
            for i in range(k):
                e = unit[i]
                if not isinstance(e, Unit):
                    raise GameUnitsArrayTypeWarning
                if unit.isHorizontal:
                    self.__appointId(e, x + floor(unit.w * i / k), y, depth + 1)
                else:
                    self.__appointId(e, x, y + floor(unit.h * i / k), depth + 1)
        return unitId

    # TODO add timer
    def addUnit(self, unit: Unit, x=0, y=0) -> str:
        if len(self.__units) >= 2 ** 16:
            raise GameUnitsCountExceededWarning

        unitId = self.__appointId(unit, x, y)
        self.__units[unit.id] = UnitInfo(unit, hash(unit) + 1)
        return unitId

    def addUnits(self, *units: Unit, x=0, y=0, horizontally=True) -> list:
        res = []
        for e in units:
            res.append(self.addUnit(e, x, y))
            if horizontally:
                x += e.w
            else:
                y += e.h
        return res

    def getDisplayList(self) -> list:
        res = self.__prevHashUnitsDict
        for k, e in self.__units.items():
            if not isinstance(e, UnitInfo):
                raise GameUnitsArrayTypeWarning
            if e.prev_hash == hash(e.unit):
                continue
            unit: Unit = e.unit
            self.__units[unit.id].prev_hash = hash(unit)
            self.__add_and_parse_unit(res, unit)
        return [y for x, y in res.items()]

    def clickUnitId(self, unitId):
        unit = self.findUnitById(unitId)
        unit.click()
        return self.getDisplayList()

    def clickCoordinates(self, x: int, y: int):
        for e, c in self.__ids_register.items():
            for i in range(c)[::-1]:
                unit = self.__units[e + '_' + str(i)]
                if unit.x <= x <= unit.x + self.w and unit.y <= y <= unit.y + self.h:
                    if is_unit_list(unit):
                        unit.clickCoordinates(x, y)
                    else:
                        unit.click()

    def clickPos(self, pos: tuple):
        if len(pos) != 2:
            raise ValueError("pos must contain two numbers: x and y coordinates")
        self.clickCoordinates(pos[0], pos[1])

    def setWinCondition(self, winCondition: Callable[[Game], GameStatus]):
        self.__winCondition = winCondition

    # TODO enum instead of int?
    @abstractmethod
    def checkIfWon(self) -> int:
        ans = self.__winCondition(self)
        if not isinstance(ans, int):
            raise GameCreatorFunctionIncorrectReturnTypeError(ans, 'int')
        return ans

    def findUnitByLambda(self, f: Callable[[Unit], bool]):
        searchQueue = [y for x, y in self.__units.items()]
        while searchQueue:
            unit: Unit = searchQueue.pop(0).unit
            if f(unit):
                return unit
            if is_unit_list(unit):
                searchQueue += list(unit)
        raise UnitNotFoundError

    def findUnitByName(self, name: str):
        return self.findUnitByLambda(lambda unit: unit.name == name)

    def findUnitById(self, unitId: str):
        return self.findUnitByLambda(lambda unit: unit.id == unitId)
    
    def getAllUnits(self):
        return [y for x, y in self.__units.items()]

    def __add_and_parse_unit(self, d: dict, unit: Unit, depth=0):
        if depth > 2 ** 16:
            raise GameAddUnitDepthExceededWarning
        # if unit is unit-list, then give every unit separately
        if is_unit_list(unit):
            for e in unit:
                if not isinstance(e, Unit):
                    raise GameUnitsArrayTypeWarning
                self.__add_and_parse_unit(d, e, depth + 1)
        else:
            d[unit.id] = unit.getDisplayDict()
