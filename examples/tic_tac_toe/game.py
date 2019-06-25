from src.cavoke import *
from enum import Enum, auto

from random import shuffle


class TileStatus(Enum):
    BLANK = auto()
    PLAYERMARKED = auto()
    ENEMYMARKED = auto()


class Tile(Image):
    def click(self) -> None:
        pass

    @property
    def draggable(self) -> bool:
        return False

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


class MyGrid(Grid):
    def nextMove(self):
        d = list(range(9))
        shuffle(d)
        for c in d:
            e = self[c // 3][c % 3]
            if e.status != TileStatus.BLANK:
                continue
            e.status = TileStatus.ENEMYMARKED
            e.setImageUrl(e.getImageUrl())
            break

    def click(self, unit: Tile = None) -> None:
        if unit.status != TileStatus.BLANK:
            return
        unit.status = TileStatus.PLAYERMARKED
        unit.setImageUrl(unit.getImageUrl())
        self.nextMove()

    @property
    def draggable(self) -> bool:
        return False

    def __init__(self):
        super().__init__(3, 3, Tile, (), "grid")
        self.nextMove()


class MyGame(Game):
    def __init__(self):
        super().__init__('tic-tac-toe', 'waleko')
        self.gridId = self.addUnit(MyGrid())
        self.grid = self.findUnitById(self.gridId)

    def isWinner(self, le):
        bo = lambda c: self.grid[c // 3][c % 3].status
        return ((bo(6) == le and bo(7) == le and bo(8) == le) or  # across the top
                (bo(3) == le and bo(4) == le and bo(5) == le) or  # across the middle
                (bo(1) == le and bo(2) == le and bo(0) == le) or  # across the bottom
                (bo(6) == le and bo(3) == le and bo(0) == le) or  # down the left side
                (bo(7) == le and bo(4) == le and bo(1) == le) or  # down the middle
                (bo(8) == le and bo(5) == le and bo(2) == le) or  # down the right side
                (bo(6) == le and bo(4) == le and bo(2) == le) or  # diagonal
                (bo(8) == le and bo(4) == le and bo(0) == le))  # diagonal

    def checkGameStatus(self) -> GameStatus:
        if self.isWinner(TileStatus.PLAYERMARKED):
            return GameStatus.WON
        elif self.isWinner(TileStatus.ENEMYMARKED):
            return GameStatus.LOST
        for i in range(3):
            for q in range(3):
                e: Tile = self.grid[i][q]
                if e.status == TileStatus.BLANK:
                    return GameStatus.PLAYING
        return GameStatus.DRAW
