from .Unit import Unit


class Image(Unit):
    def __hash__(self):
        return super().__hash__() + hash(self.image_url)

    def click(self):
        pass

    def drag(self, toUnit):
        pass

    def getDisplayDict(self) -> dict:
        d = super().getDisplayDict()
        d['image_url'] = self.image_url
        return d

    def __init__(self, image_url: str, name: str = "", w: int = -1, h: int = -1, initPayload: dict = {}):
        super().__init__(name, w, h, initPayload)
        self.image_url = image_url
