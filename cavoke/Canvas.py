from .Unit import Unit
from .exceptions import *
from .CanvasInfo import CanvasInfo
from .UnitCanvasInfo import UnitCanvasInfo


class Canvas(object):
    def __init__(self, game_repr: str, w=680, h=480):
        self.__game_repr = game_repr
        self.w = w
        self.h = h
        self.__units = {}
        self.__ids_register = {}
        self.prevDict = {}

    def __repr__(self):
        return "<Canvas linked to " + repr(self.__game_repr) + " game with w=" + str(self.w) + "&h=" + str(self.h) + ">"

    def addUnit(self, unit: Unit, x=0, y=0):
        if len(self.__units) >= 2 ** 16:
            raise CanvasUnitsCountExceeded
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
        canvasInfo = CanvasInfo(repr(self), unitId)
        unit._addToCanvas(canvasInfo, x, y)
        self.__units[unit.id](UnitCanvasInfo(unit, hash(unit) + 1))

    def findUnitByName(self, name: str):
        for e in self.__units:
            if e is not UnitCanvasInfo:
                raise ValueError("junk in canvas.__units")
            if e.unit.name == name:
                return e

    def findUnitById(self, unitId: str):
        for e in self.__units:
            if e is not UnitCanvasInfo:
                raise ValueError("junk in canvas.__units")
            if e.unit.id == unitId:
                return e

    def toDisplayList(self) -> list:
        res = self.prevDict
        for e in self.__units:
            if e is not UnitCanvasInfo:
                raise ValueError("junk in canvas.__units")
            if e.prev_hash == hash(e.unit):
                continue
            unit: Unit = e.unit
            self.__units[unit.id].prev_hash = hash(unit)
            res[unit.id] = unit.toDisplayDict()
        return [y for x, y in res.items()]
