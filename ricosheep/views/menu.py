from turtle import color, onclick
from flinter import View
from colors import *
from game import Parser, Game, Board
import os
from pathlib import Path

def menu(args):
    '''define the menu'''
    menu = View(12, 12)
    dim = 5
    filename = "name"

    def set_dim(nb):
        nonlocal dim
        dim = nb
    
    def set_filename(f):
        nonlocal filename
        filename = f + ".txt"

    def load_conquest():
        if 3 <= dim <= 40:
            menu.browse("board", dim, dim, dim - 1, dim)
        else:
            menu.change("size_error", text="size must be between 3 and 40")

    def load_from_file():
        files = list(Path(os.path.dirname(os.path.abspath(__file__)) + "/../../assets/maps/").rglob(filename))
        if files and filename:
            parser = Parser(files[0])
            try:
                board, sheeps = parser.load()
                menu.browse("board", Game(Board(board=board), sheeps))
            except:
                menu.change("map_error", text="invalid map")
        else:
            menu.change("map_error", text="map not found")

    menu.box(0, 0, width=12, height=12, color=BGCOLOR, no_pad=True)
    menu.box(0, 0, width=6, height=12, color=BGCOLOR, no_pad=True)
    menu.text_box(0, 1, width=6, text="Conquest Mode", color=BGCOLOR, border=BGCOLOR)
    menu.text_box(0, 3, width = 6, text="play on increasingly harder", color=BGCOLOR, border=BGCOLOR)
    menu.text_box(0, 4, width = 6, text="randomly generated maps", color=BGCOLOR, border = BGCOLOR)
    menu.text_box(1, 6, width=3, text="starting size : ", color=BGCOLOR, border=BGCOLOR)
    menu.text_field(4, 6, text=dim, on_enter=lambda n: set_dim(int(n)))
    menu.text_box(0, 8, width=6, text_color=RED, color=BGCOLOR, border=BGCOLOR, tags=["error", "size_error"])
    menu.button(2, 10, width=2, height=2, text="Go !", on_click=load_conquest)
    menu.text_box(6, 1, width=6, text="Custom", color=BGCOLOR, border=BGCOLOR)
    menu.text_box(6, 3, width = 6, text="Load a custom map from", color=BGCOLOR, border=BGCOLOR)
    menu.text_box(6, 4, width = 6, text="the assets folder", color=BGCOLOR, border = BGCOLOR)
    menu.text_field(7, 6, width=4, text="name", on_enter=lambda f: set_filename(f))
    menu.text_box(6, 8, width=6, text_color=RED, color=BGCOLOR, border=BGCOLOR, tags=["error", "map_error"])
    menu.button(8, 10, width=2, height=2, text="Go !", on_click=load_from_file)
    menu.button(11, 0, text="settings", on_click=lambda: menu.browse("settings"))
    menu.add_event(lambda: menu.browse("exit"), "Quitte")
    return menu