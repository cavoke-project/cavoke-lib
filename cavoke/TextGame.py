from typing import Callable
from GameServer import GameServer

class TextGame(object):
    def __init__(self, game_name, author):
        self.game_name = game_name
        self.author = author
        self.welcome = None

    def setWelcome(self, f):
        self.welcome = f

    def displayMessage(self, text):
        print(text + ' ' + self.game_name)

    def execWelcome(self):
        self.welcome()

    def setLambda(self, f: Callable):
        f(self)