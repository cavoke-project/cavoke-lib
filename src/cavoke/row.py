from math import floor
from typing import List, Tuple

from .unitlisttemplate import UnitListTemplate
from .unit import Unit


class Row(UnitListTemplate):
    @property
    def isHorizontal(self) -> bool:
        return True

    @property
    def units(self) -> List[Unit]:
        return self.__units

    def getIndexByCoordinates(self, x, y) -> int:
        return floor((x - self.x) / self.w * self.length)

    def __init__(
        self,
        items_x: int,
        BaseClass: type,
        baseArgs: tuple = (),
        name: str = "",
        w=600,
        h=600,
        init_payload: dict = {},
    ):
        super().__init__(items_x, BaseClass, baseArgs, name, w, h, init_payload)
        self.items_y = items_x
        self.__units = [
            self.genSub(BaseClass, baseArgs, w // items_x, h, name + "_" + str(i))
            for i in range(items_x)
        ]
