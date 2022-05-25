from flinter import Router
from views import menu, board, settings

routes = {
    "menu": menu,
    "board": board,
    "settings": settings,
    "exit": None
}

app = Router(**routes)

if __name__ == "__main__":
    app.run(menu)
