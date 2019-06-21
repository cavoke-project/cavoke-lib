from src.cavoke import *
from enum import Enum, auto


class TileStatus(Enum):
    BLANK = auto()
    PLAYERMARKED = auto()
    ENEMYMARKED = auto()


class Tile(Image):
    @property
    def draggable(self) -> bool:
        return False

    def click(self) -> None:
        if not self.status == TileStatus.BLANK:
            self.status = TileStatus.PLAYERMARKED
            self.setImageUrl(self.getImageUrl())


    def drag(self, toUnit: Unit) -> bool:
        pass

    def getImageUrl(self):
        baseUrl = "https://alexkovrigin.me/data/cavoke/examples/1/"
        if self.status == TileStatus.BLANK:
            addUrl = "blank.png"
        elif self.status == TileStatus.PLAYERMARKED:
            addUrl = "cross.png"
        else:
            addUrl = "circle.png"
        return baseUrl + addUrl

    def __init__(self):
        self.status = TileStatus.BLANK
        super().__init__(self.getImageUrl())
