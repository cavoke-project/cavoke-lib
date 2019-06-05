from cavoke.TextGame import TextGame

game = TextGame(game_name="Dummy Game",
                author='waleko')
canvas = Canvas(w=680, h=480)
canvas.addObject(Image(src='example.org/favicon.ico'), name="one", x=10, y=10, clickable=True)
canvas.addObject(Image(src='example.org/favicon.ico'), position='centre')  # auto-name
canvas.addObject(Text(text='123', font='Times New Roman', size=17), position='centre')

game.setCanvas(canvas)

canvas1 = Canvas()
grid = Grid(x=3, y=3, size="full")  # auto-name, grid is iterable, default base is image
grid.setOnClick(lambda obj: {
    if obj.
})
canvas1.addObject(grid)
# Image, Text, Grid are inherited from Unit, which contains clickable methods and so on

