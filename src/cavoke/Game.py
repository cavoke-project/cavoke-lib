from typing import Callable
from abc import abstractmethod

from .Canvas import Canvas
from .Unit import Unit


class Game(Canvas):
    def __init__(self, game_name, creator, w=680, h=480, initPayload = {}, custom_canvas=None,
                 winCondition: Callable = lambda *args: None):
        self.game_name = game_name
        self.creator = creator
        self.welcome = None
        self.canvas = custom_canvas
        self.__winCondition = winCondition
        if custom_canvas is None:
            super().__init__(repr(self), w, h, initPayload)
            custom_canvas =
        self.canvas = custom_canvas



    def __repr__(self):
        return '<"' + self.game_name + '" game built using cavoke by ' + self.creator + '>'

    # TODO add timer

    def addObject(self, unit: Unit, x=0, y=0):
        self.canvas.addUnit(unit, x, y)

    def setWinCondition(self, winCondition: Callable):
        self.__winCondition = winCondition

    # TODO enum?
    @abstractmethod
    def checkIfWon(self) -> int:
        return self.__winCondition(self.canvas)
