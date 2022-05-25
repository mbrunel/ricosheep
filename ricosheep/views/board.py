from multiprocessing.connection import wait
from flinter import View
from game import Game, Board, Dot
from colors import *
import os

def path(file):
    return os.path.dirname(os.path.abspath(__file__)) + "/../../assets/images/" + file + ".png"

def board(args):
    '''define the board'''
    board = View(12, 12)
    board.text_box(0, 0, width=12, height=1, border=BGCOLOR, color=BGCOLOR, tags=["status"])

    if len(args) == 1:
        game, = args
        solution = game.solve()
        if not solution:
            board.change("status", "You lost!")
            solution_depth = game.board.width
        else:
            solution_depth = len(solution)
    else:
        width, height, nbSheeps, solution_depth = args
        game = Game(Board(width=width, height=height), nbSheeps=nbSheeps)
        if not game.generate_solution(solution_depth):
            board.browse("board", width, height, nbSheeps, solution_depth)

    def change(action):
        for sheep in game.sheeps:
            tag = str(sheep.y * game.board.width + sheep.x)
            if game.board[sheep].is_grass():
                board.change(tag, image=path("grass"))
            else:
                board.delete(tag)
        action()
        for sheep in game.sheeps:
            tag = str(sheep.y * game.board.width + sheep.x)
            if game.board[sheep].is_grass():
                board.change(tag, image=path("sheep_grass"))
            else:
                board.box(sheep.x, sheep.y, grid="game", image=path("sheep"), tags=[tag])
        if game.isWon():
            board.change("status", text="You won!")
            board.change("new_game", text="Next level", on_click=lambda: board.browse("board", game.board.width + 1, game.board.height + 1, game.board.width - 1, solution_depth))
            return
        
        if (game.board.height + game.board.width) // 2 <= 9:
            tmp = game.clone()
            tmp.moves = tmp.states = []
            solution = tmp.solve()
            if not solution:
                board.change("status", text="You lost!")
                board.change("undo", text="retry", on_click=lambda: change(lambda: game.rewind(0)))
            elif len(solution) <= 3:
                board.change("status", text="Almost there!")
            else:
                board.change("status", text="Keep going!")

    board.box(0, 0, width=12, height=12, color=BGCOLOR, border=BGCOLOR, no_pad=True)
    board.grid("game", 1, 2, 10, 8, game.board.width, game.board.height)
    for y in range(game.board.height):
        for x in range(game.board.width):
            pos = Dot(x, y)
            board.box(x, y, grid="game", no_pad=True)
            image = ""
            if game.board[pos].is_bush():
                image = "bush"
            elif game.board[pos].is_grass():
                if pos in game.sheeps:
                    image = "sheep_grass"
                else:
                    image = "grass"
            elif pos in game.sheeps:
                    image = "sheep"
            if image:
                board.box(x, y, grid="game", no_pad=True, image=path(image), tags=[str(y * game.board.width + x)])
    
    board.add_event(lambda: change(lambda: game.move("right")), "Touche", "Right")
    board.add_event(lambda: change(lambda: game.move("left")), "Touche", "Left")
    board.add_event(lambda: change(lambda: game.move("up")), "Touche", "Up")
    board.add_event(lambda: change(lambda: game.move("down")), "Touche", "Down")
    board.button(1, 11, width=2, text="menu", on_click=lambda: board.browse("menu"))
    board.button(5, 11, width=2, text="reroll", on_click=lambda: board.browse("board", game.board.width, game.board.height, len(game.sheeps), solution_depth), tags=["new_game"])
    board.button(9, 11, width=2, text="undo", on_click=lambda: change(lambda: game.rewind(-1)), tags=["undo"])
    board.add_event(lambda: board.browse("exit"), "Quitte")
    return board