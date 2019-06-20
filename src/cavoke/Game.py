from typing import Callable
from abc import abstractmethod

from .exceptions import *
from .Unit import Unit
from .GameInfo import GameInfo
from .UnitInfo import UnitInfo
from .Grid import Grid
from .Row import Row


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

    # TODO add timer
    def addUnit(self, unit: Unit, x=0, y=0, _depth=0) -> str:
        if len(self.__units) >= 2 ** 16:
            raise GameUnitsCountExceededWarning
        if _depth > 2 ** 16:
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

        # FIXME remove
        # # if is list (Row, Grid), then process every element separately
        # if isinstance(unit, Unit) and isinstance(unit, list):
        #     self.addUnits(*unit, x=x, y=y, horizontally=unit.isHorizontal, _depth=_depth)
        #     return unitId

        # register the unit
        gameInfo = GameInfo(repr(self), unitId)
        unit._addToCanvas(gameInfo, x, y)
        self.__units[unit.id] = UnitInfo(unit, hash(unit) + 1)
        return unitId

    def addUnits(self, *units: Unit, x=0, y=0, horizontally=True, _depth=0) -> list:
        res = []
        for e in units:
            res.append(self.addUnit(e, x, y, _depth + 1))
            if horizontally:
                x += e.w
            else:
                y += e.h
        return res

    def getDisplayList(self) -> list:
        res = self.__prevHashUnitsDict
        for k, e in self.__units.items():
            if not isinstance(e, UnitInfo):
                raise GameUnitsMemoryWarning
            if e.prev_hash == hash(e.unit):
                continue
            unit: Unit = e.unit
            self.__units[unit.id].prev_hash = hash(unit)
            res[unit.id] = unit.getDisplayDict()
        return [y for x, y in res.items()]

    def clickUnit(self, unit):
        unit.click()

    def clickCoordinates(self, x, y):
        for e, c in self.__ids_register.items():
            for i in range(c)[::-1]:
                unit = self.__units[e + '_' + str(i)]
                if unit.x <= x <= unit.x + self.w and unit.y <= y <= unit.y + self.h:
                    return self.clickUnit(unit)

    def clickPos(self, pos: tuple):
        if len(pos) != 2:
            raise ValueError("pos must contain two numbers: x and y coordinates")
        self.clickCoordinates(pos[0], pos[1])

    def setWinCondition(self, winCondition: Callable):
        self.__winCondition = winCondition

    # TODO enum instead of int?
    @abstractmethod
    def checkIfWon(self) -> int:
        ans = self.__winCondition(self)
        if not isinstance(ans, int):
            raise GameCreatorFunctionIncorrectReturnTypeError(ans, 'int')
        return ans

    def findUnitByName(self, name: str):
        for k, e in self.__units.items():
            if not isinstance(e, UnitInfo):
                raise GameUnitsMemoryWarning
            if e.unit.name == name and name != "":
                return e.unit
        raise UnitNotFoundError

    def findUnitById(self, unitId: str):
        try:
            unit = self.__units[unitId]
        except KeyError:
            raise UnitNotFoundError
        return unit
    
    def allUnits(self):
        return [y for x, y in self.__units.items()]