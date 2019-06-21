from abc import abstractmethod

from .Unit import Unit


class UnitListTemplate(Unit, list):
    def genSub(self, BaseClass: type, baseArgs: tuple, w, h, name):
        """
        Generates child object of type BaseClass
        :param BaseClass: class of childs
        :param baseArgs: arguments for BaseClass constructor
        :param w: child's width
        :param h: child's height
        :param name: child's name
        :return: child
        """
        res = BaseClass(*baseArgs)
        res.w = w
        res.h = h
        res.name = name
        return res

    def __init__(
        self,
        length: int,
        BaseClass: type,
        baseArgs: tuple = (),
        name: str = "",
        w=600,
        h=600,
        init_payload: dict = {},
    ):
        """
        Constructor for UnitListTemplate
        :param length: length of list
        :param BaseClass: class of list element
        :param baseArgs: arguments for elements
        :param name: list name
        :param w: list width
        :param h: list height
        :param init_payload: initial list payload
        """
        super().__init__(name, w, h, init_payload)
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
        """
        Abstract method that gets index for element in list by coordinates on game canvas
        :param x: x coordinate
        :param y: y coordinate
        """
        pass

    def clickCoordinates(self, x, y):
        """
        Process click on coordinates. Gets child unit, that was clicked and calls its click() method,
        or clickCoordinates() method if unit-list. :param x: :param y: :return:
        """
        if not (self.x <= x <= self.x + self.w and self.y <= y <= self.y + self.h):
            return None
        i = self.getIndexByCoordinates(x, y)
        unit = self.__getitem__(i)
        if isinstance(unit, Unit) and isinstance(unit, list):
            unit.clickCoordinates(x, y)
        else:
            unit.click()

    def getDisplayDict(self):
        raise NotImplementedError

    def click(self) -> None:
        raise NotImplementedError

    def drag(self, toUnit) -> bool:
        raise NotImplementedError
