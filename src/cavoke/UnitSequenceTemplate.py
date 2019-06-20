from abc import abstractmethod

from .Unit import Unit


class UnitSequenceTemplate(Unit, list):
    def genSub(self, BaseClass: type, baseArgs: tuple, w, h, name):
        res = BaseClass(*baseArgs)
        res.w = w
        res.h = h
        res.name = name
        return res

    def __init__(self, length: int, BaseClass: type, baseArgs = (),
                 name: str = "", w=600, h=600, initPayload: dict = {}):
        super().__init__(name, w, h, initPayload)
        self.length = length
        self.__BaseClass = BaseClass

    def __hash__(self):
        h = 0
        for e in self.units:
            h += hash(e)
        return h

    @property
    @abstractmethod
    def units(self) -> list:
        pass

    @property
    @abstractmethod
    def isHorizontal(self) -> bool:
        pass

    def __getitem__(self, item):
        return self.units.__getitem__(item)

    def __len__(self):
        return len(self.units)

    def __iter__(self):
        for i in range(self.length):
            yield self.units[i]

    @abstractmethod
    def getIndexByCoordinates(self, x, y) -> int:
        pass

    def clickCoordinates(self, x, y):
        if not (self.x <= x <= self.x + self.w and self.y <= y <= self.y + self.h):
            return None
        i = self.getIndexByCoordinates(x, y)
        unit = self.__getitem__(i)
        if isinstance(unit, Unit) and isinstance(unit, list):
            unit.clickCoordinates(x, y)
        else:
            unit.click()

    def getDisplayDict(self):
        pass

    def click(self) -> None:
        pass

    def drag(self, toUnit) -> bool:
        pass
