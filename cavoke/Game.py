from typing import Callable

from .Canvas import Canvas
from .Unit import Unit


class Game(object):
    def __init__(self, game_name, creator, canvas=None):
        self.game_name = game_name
        self.creator = creator
        self.welcome = None
        if canvas is None:
            canvas = Canvas(repr(self))
        self.canvas = canvas

    def __repr__(self):
        return '<"' + self.game_name + '" game built using cavoke by ' + self.creator + '>'

    # TODO add timer

    def addObject(self, unit: Unit, x=0, y=0):
        self.canvas.addUnit(unit, x, y)

    # def setWinCondition(self, winCondition: Callable):