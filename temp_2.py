from src.cavoke import *


class Tile(Image):
    def click(self) -> None:
        self.setImageUrl("cross.png")
        self.status = 1

    def drag(self, toUnit) -> bool:
        pass

    def __init__(self):
        super().__init__("blank.png")
        self.status = 0


class MyGrid(Grid):
    def __init__(self):
        super().__init__(3, 3, Tile, (), "grid", initPayload={"marked": 0})


class MyGame(Game):
    def __init__(self):
        super().__init__("Dummy", "waleko")
        self.addUnit(MyGrid())

    def checkGameStatus(self) -> GameStatus:
        grid = self.findUnitByName("grid")
        if grid[0][0].status == 1:
            return GameStatus.WON
        elif grid[0][0].status == 2:
            return GameStatus.LOST
        else:
            return GameStatus.PLAYING
