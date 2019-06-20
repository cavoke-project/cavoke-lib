from abc import abstractmethod

from .Unit import Unit


class Column(Unit, list):
    def __genSub(self, BaseClass: type, w, h, name, *baseArgs):
        res = BaseClass(*baseArgs)
        res.w = w
        res.h = h
        res.name = name
        return res

    def __init__(self, items_y: int, BaseClass: type,
                 name: str = "", w=600, h=600, initPayload: dict = {},
                 *baseArgs):
        super().__init__(name, w, h, initPayload)
        self.items_y = items_y
        self.__units = [self.__genSub(BaseClass, w, h // items_y, name + '_' + str(i),
                                      *baseArgs) for i in range(items_y)]
        self.__BaseClass = BaseClass
        self.isHorizontal = False

    def __getitem__(self, item):
        return self.__units.__getitem__(item)

    def __iter__(self):
        for i in range(self.items_y):
            yield self.__units[i]

    def getDisplayDict(self) -> list:
        return self.__units

    def click(self):
        pass

    def drag(self, toUnit):
        pass
