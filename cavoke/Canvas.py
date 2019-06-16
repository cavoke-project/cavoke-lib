from typing import Callable

class Canvas(object):
    def __init__(self, game, w=680, h=480):
        self.__game = game
        self.w = w
        self.h = h
        self.objects = []

    def __repr__(self):
        return "<Canvas linked to " + repr(self.__game) + " game with w=" + str(self.w) + "&h=" + str(self.h) + ">"

    def addObject(self):