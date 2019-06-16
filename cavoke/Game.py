from typing import Callable
from .Canvas import Canvas


class Game(object):
    def __init__(self, game_name, creator, canvas=None):
        self.game_name = game_name
        self.creator = creator
        self.welcome = None
        if canvas is None:
            canvas = Canvas(self)
        self.canvas = canvas

    def __repr__(self):
        return '<"' + self.game_name + '" game built on cavoke by ' + self.creator + '>'

    # def addObject(self, unit: Unit):
    #
    # def setWinCondition(self, winCondition: Callable):
