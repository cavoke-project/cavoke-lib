from math import floor

from .UnitSequenceTemplate import UnitSequenceTemplate


class Column(UnitSequenceTemplate):
    @property
    def isHorizontal(self) -> bool:
        return False

    @property
    def units(self) -> list:
        return self.__units

    def getIndexByCoordinates(self, x, y) -> int:
        return floor((y - self.y) / self.h * self.length)

    def __init__(self, items_y: int, BaseClass: type, baseArgs: tuple = (),
                 name: str = "", w=600, h=600, initPayload: dict = {}):
        super().__init__(items_y, BaseClass, baseArgs, name, w, h, initPayload)
        self.items_y = items_y
        self.__units = [self.genSub(BaseClass, baseArgs, w, h // items_y, name + '_' + str(i))
                        for i in range(items_y)]
