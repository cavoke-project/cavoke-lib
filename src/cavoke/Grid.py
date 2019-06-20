from abc import abstractmethod

from .Unit import Unit
from .Row import Row


class Grid(Row, list):
    def __init__(self, items_x: int, items_y: int, BaseClass: type,
                 name: str = "", w=600, h=600, initPayload: dict = {},
                 *baseArgs):
        super().__init__(items_y, Row, name, w, h // items_y, initPayload,
                         items_x, BaseClass, name, w // items_x, h // items_y, initPayload, *baseArgs)
        self.__units = [Row(items_x, BaseClass, name + '_' + str(i), w, h // items_y,
                            *baseArgs) for i in range(items_y)]
        self.__BaseClass = BaseClass
        self.isHorizontal = False

    def __getitem__(self, item):
        return self.__units.__getitem__(item)

    def getDisplayDict(self) -> dict:
        pass

    def click(self):
        pass

    def drag(self, toUnit):
        pass