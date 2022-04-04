from flinter import Router
from views import menu

routes = {
    "menu": menu,
    "exit": None
}

app = Router(**routes)

if __name__ == "__main__":
    app.run(menu)
