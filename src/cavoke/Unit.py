from typing import Callable
from .exceptions import *
from .CanvasInfo import CanvasInfo
from abc import abstractmethod


class Unit(object):
    def __init__(self, name: str = "", w=50, h=50,
                 onClick: Callable = None, onDrag: Callable = None,
                 initPayload: dict = {}):
        self.name = name
        self.id = None
        self.__canvasInfo = None

        self.pos = (0, 0)
        self.x = 0
        self.y = 0

        self.w = w
        self.h = h
        self.visible = True

        self.setOnClick(onClick)
        self.setOnDrag(onDrag)
        self.payload = initPayload

    def __repr__(self):
        if self.__canvasInfo is None:
            return '<' + str(self.__class__) + " class without a linked canvas. payload=" + repr(self.payload) + '>'
        else:
            return '<' + str(self.__class__) + " class linked to " + self.__canvasInfo.canvas_repr + " canvas at pos=" +\
                   repr(self.pos) + ". payload=" + repr(self.payload) + '>'

    def __hash__(self):
        return hash(hash(self.name) +
                    hash(self.id) +
                    hash(self.x) +
                    hash(self.y))

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
    def toDisplayDict(self):
        return

    # TODO refactor with Unit.setFunction()
    def setOnClick(self, onClick: Callable):
        if onClick is None:
            self.__onClick = lambda *args: None
            self.clickable = False
        else:
            self.__onClick = onClick
            self.clickable = True

    def click(self):
        if self.clickable:
            self.__onClick()

    def setOnDrag(self, onDrag: Callable):
        if onDrag is None:
            self.__onDrag = lambda *args: None
            self.draggable = False
        else:
            self.__onDrag = onDrag
            self.draggable = True

    def drag(self, toUnit):
        if self.draggable:
            self.__onDrag(toUnit)

    def moveTo(self, x, y):
        if self.__canvasInfo is None:
            raise NoCanvasWarning
        self.x = x
        self.y = y
        self.pos = (x, y)

    def moveToPos(self, pos: tuple):
        if len(pos) != 2:
            raise ValueError("pos must contain two numbers: x and y coordinates")
        self.moveTo(pos[0], pos[1])

    def moveBy(self, dx, dy):
        self.moveTo(self.x + dx, self.y + dy)

    def _addToCanvas(self, canvasInfo: CanvasInfo, x=0, y=0):
        if self.__canvasInfo is None:
            self.__canvasInfo = canvasInfo
            self.moveTo(x, y)
            self.id = canvasInfo.new_unit_id
        else:
            raise UnitCanvasOverride(self, canvasInfo)
