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
        return floor((x - self.x) / self.w * self.length)

    def __init__(self, items_y: int, BaseClass: type,
                 name: str = "", w=600, h=600, initPayload: dict = {},
                 *baseArgs):
        super().__init__(items_y, BaseClass, name, w, h, initPayload, *baseArgs)
        self.items_y = items_y
        self.__units = [self.genSub(BaseClass, w, h // items_y, name + '_' + str(i), *baseArgs)
                        for i in range(items_y)]
