from .Column import Column
from .Row import Row


class Grid(Column, list):
    def __init__(
        self,
        items_x: int,
        items_y: int,
        BaseClass: type,
        baseArgs: tuple = (),
        name: str = "",
        w=600,
        h=600,
        initPayload: dict = {},
    ):
        super().__init__(
            items_y,
            Row,
            (items_x, BaseClass, baseArgs, name, w, h // items_y),
            name,
            w,
            h,
            initPayload,
        )
