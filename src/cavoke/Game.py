from typing import Callable
from abc import abstractmethod

from .exceptions import *
from .Unit import Unit
from .GameInfo import GameInfo
from .UnitInfo import UnitInfo


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

    def addUnit(self, unit: Unit, x=0, y=0) -> str:
        if len(self.__units) >= 2 ** 16:
            raise GameUnitsCountExceededWarning
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
        unit._addToCanvas(gameInfo, x, y)
        self.__units[unit.id] = UnitInfo(unit, hash(unit) + 1)
        return unitId

    def toDisplayList(self) -> list:
        res = self.__prevHashUnitsDict
        for e in self.__units:
            if not isinstance(e, UnitInfo):
                raise GameUnitsMemoryWarning
            if e.prev_hash == hash(e.unit):
                continue
            unit: Unit = e.unit
            self.__units[unit.id].prev_hash = hash(unit)
            res[unit.id] = unit.toDisplayDict()
        return [y for x, y in res.items()]

    # def clickCoordinates(self, ):

    def clickPos(self, pos: tuple):
        if len(pos) != 2:
            raise ValueError("pos must contain two numbers: x and y coordinates")

    def setWinCondition(self, winCondition: Callable):
        self.__winCondition = winCondition

    # TODO enum instead of int?
    @abstractmethod
    def checkIfWon(self) -> int:
        ans = self.__winCondition(self)
        if ans is not int:
            raise CreatorFunctionIncorrectReturnTypeError(ans, 'int')
        return ans

    def findUnitByName(self, name: str):
        for k, e in self.__units.items():
            if not isinstance(e, UnitInfo):
                raise GameUnitsMemoryWarning
            if e.unit.name == name:
                return e.unit
        raise UnitNotFoundError

    def findUnitById(self, unitId: str):
        for k, e in self.__units.items():
            if not isinstance(e, UnitInfo):
                raise GameUnitsMemoryWarning
            if e.unit.id == unitId:
                return e.unit
        raise UnitNotFoundError
