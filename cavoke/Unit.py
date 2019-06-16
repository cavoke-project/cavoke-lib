from typing import Callable
from .exceptions import *
from .Canvas import Canvas


class Unit(object):
    def __init__(self, onClick: Callable = None, onDrag: Callable = None, initPayload: dict = {}):
        self.__canvas = None
        self.pos = (0, 0)
        self.x = 0
        self.y = 0
        self.setOnClick(onClick)
        self.setOnDrag(onDrag)
        self.payload = initPayload

    def __repr__(self):
        if self.__canvas is None:
            return '<' + str(self.__class__) + " class without a linked canvas. payload=" + repr(self.payload) + '>'
        else:
            return '<' + str(self.__class__) + " class linked to " + repr(Canvas) + " canvas at pos=" +\
                   repr(self.pos) + ". payload=" + repr(self.payload) + '>'
    # FIXME evals don't work
    # def setFunction(self, method: str, methodBoolean: str, f: Callable):
    #     cmd = lambda pre, post: eval(pre + (' ' if pre else '') + 'self.' + method + (' ' if post else '') + post)
    #     if f is None:
    #         eval('self.' + method + ' = lambda *args: None')
    #         eval('self.' + methodBoolean + ' = False')
    #     else:
    #         eval('self.' + method + ' = f')
    #         eval('self.' + methodBoolean + ' = True')

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
        if self.__canvas is None:
            raise NoCanvasWarning
        self.x = x
        self.y = y
        self.pos = (x, y)

    def moveToPos(self, pos: tuple):
        self.moveTo(pos[0], pos[1])

    def moveBy(self, dx, dy):
        self.moveTo(self.x + dx, self.y + dy)

    def _addToCanvas(self, canvas: Canvas, x, y):
        if canvas is None:
            self.__canvas = canvas
            self.moveTo(x, y)
        else:
            raise UnitCanvasOverride(self, canvas)
