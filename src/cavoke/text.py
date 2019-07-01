from .unit import Unit


class Text(Unit):
    def fullHash(self):
        return super().fullHash() + hash(self.text) + hash(self.size) + hash(self.font)

    def getDisplayDict(self):
        return {
            "name": self.name,
            "type": self._unit_type,
            "id": self.id,
            "position": {"x": self.x, "y": self.y},
            "text": self.text,
            "font": self.font,
            "size": self.size,
        }

    @property
    def _unit_type(self) -> str:
        return "text"

    def __init__(
        self,
        text: str,
        name: str = "",
        size: int = 11,
        font: str = "Arial",
        init_payload: dict = {},
    ):
        super().__init__(name, 50, 50, init_payload)
        self.__text = text
        self.__size = size
        self.__font = font

    @property
    def text(self):
        return self.__text

    @property
    def size(self):
        return self.__size

    @property
    def font(self):
        return self.__font

    def setText(self, text: str):
        self.__text = text

    def setFont(self, font: str):
        self.__font = font

    def setSize(self, size: int):
        self.__text = int(size)
