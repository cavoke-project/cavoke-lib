from math import floor

from .UnitSequenceTemplate import UnitSequenceTemplate


class Row(UnitSequenceTemplate):
    @property
    def isHorizontal(self) -> bool:
        return True

    @property
    def units(self) -> list:
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
        initPayload: dict = {},
    ):
        super().__init__(items_x, BaseClass, baseArgs, name, w, h, initPayload)
        self.items_y = items_x
        self.__units = [
            self.genSub(BaseClass, baseArgs, w // items_x, h, name + "_" + str(i))
            for i in range(items_x)
        ]
