from src.cavoke import *


game = Game(game_name="Tick-tack-toe pre-pre-demo", creator="waleko")


grid = Grid(x=3, y=3, size="full")  # auto-name, grid is iterable, default base is image
grid.setOnClick(lambda obj: {123})
game.addObject(grid)
# Image, Text, Grid are inherited from Unit, which contains clickable methods and so on
def tileOnClick(tile: Image):
    if tile.extra["status"] == "Unchecked":
        tile.extra["status"] = "Player_checked"
        tile.src = "/cross.png"


grid.setOnClick(tileOnClick)


def winCondition(_game: Game) -> bool:
    _grid = _game.getElementByName("grid1")
    return _grid[0][0].extra["status"] == "Player_checked"


game.setWinCondition(winCondition)

# canvas = Canvas(w=680, h=480)
# canvas.addObject(Image(src='example.org/favicon.ico'), name="one", x=10, y=10, clickable=True)
# canvas.addObject(Image(src='example.org/favicon.ico'), position='centre')  # auto-name
# canvas.addObject(Text(text='123', font='Times New Roman', size=17), position='centre')
#
# game.setCanvas(canvas)
