from __future__ import annotations


from typing import Callable
from .exceptions import *
from .GameInfo import GameInfo
from abc import abstractmethod


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
            return '<name=' + (self.name if self.name else "[no name given]") + '; class=' + str(
                self.__class__) + ";no game linked>"
        else:
            return '<id=' + self.id + '; name=' + self.name + '; class=' + str(self.__class__) + \
                   ";game=" + self.__gameInfo.game_repr + "; pos=" + repr(self.pos) + '>'

    @abstractmethod
    def __hash__(self):
        return hash(hash(self.name) +
                    hash(self.id) +
                    hash(self.x) +
                    hash(self.y) +
                    hash(self.w) +
                    hash(self.h))

    # FIXME evals don't work
    # def setFunction(self, method: str, methodBoolean: str, f: Callable):
    #     cmd = lambda pre, post: eval(pre + (' ' if pre else '') + 'self.' + method + (' ' if post else '') + post)
    #     if f is None:
    #         eval('self.' + method + ' = lambda *args: None')
    #         eval('self.' + methodBoolean + ' = False')
    #     else:
    #         eval('self.' + method + ' = f')
    #         eval('self.' + methodBoolean + ' = True')

    @abstractmethod
    def getDisplayDict(self):
        return {
            "name": self.name,
            "id": self.id,
            "position": {
                "x": self.x,
                "y": self.y
            },
            "size": {
                "w": self.w,
                "h": self.h
            }
        }

    # TODO refactor with Unit.setFunction()
    def setOnClick(self, onClick: Callable[[], None]):
        if onClick is None:
            self.__onClick = lambda *args: None
            self.clickable = False
        else:
            self.__onClick = onClick
            self.clickable = True

    @abstractmethod
    def click(self):
        if self.clickable:
            self.__onClick()

    def setOnDrag(self, onDrag: Callable[[Unit], None]):
        if onDrag is None:
            self.__onDrag = lambda *args: None
            self.draggable = False
        else:
            self.__onDrag = onDrag
            self.draggable = True

    @abstractmethod
    def drag(self, toUnit):
        if self.draggable:
            self.__onDrag(toUnit)

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
