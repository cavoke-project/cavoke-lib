from .Row import Row
from .Column import Column


class Grid(Column, list):

    def __init__(self, items_x: int, items_y: int, BaseClass: type,
                 name: str = "", w=600, h=600, initPayload: dict = {},
                 *baseArgs):
        super().__init__(items_y, Row, name, w, h, initPayload,
                         items_x, BaseClass, name, w, h // items_y, initPayload, *baseArgs)

    def getDisplayDict(self) -> dict:
        pass

    def click(self):
        pass

    def drag(self, toUnit):
        pass