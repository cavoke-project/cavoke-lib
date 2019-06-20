from abc import abstractmethod

from .Unit import Unit


class Image(Unit):
    def getDisplayDict(self) -> dict:
        return {
            "name": self.name,
            "position": {
                "x": self.x,
                "y": self.y
            },
            "image_url": self.image_url,
            "clickable": self.clickable,
            "draggable": self.draggable
        }

    def __init__(self, image_url: str, name: str = "", w: int = None, h: int = None, initPayload: dict = {}):
        super().__init__(name, w, h, initPayload)
        self.image_url = image_url

    @abstractmethod
    def click(self):
        pass

    @abstractmethod
    def drag(self, toUnit):
        pass
