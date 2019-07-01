from math import floor
from typing import List

from .unitlisttemplate import UnitListTemplate
from .unit import Unit


class Column(UnitListTemplate):
    @property
    def isHorizontal(self) -> bool:
        return False

    @property
    def units(self) -> List[Unit]:
        return self.__units

    def getIndexByCoordinates(self, x, y) -> int:
        return floor((y - self.y) / self.h * self.length)

    def __init__(
        self,
        items_y: int,
        BaseClass: type,
        baseArgs: tuple = (),
        name: str = "",
        w=600,
        h=600,
        init_payload: dict = {},
    ):
        super().__init__(items_y, BaseClass, baseArgs, name, w, h, init_payload)
        self.items_y = items_y
        self.__units = [
            self.genSub(BaseClass, baseArgs, w, h // items_y, name + "_" + str(i))
            for i in range(items_y)
        ]
