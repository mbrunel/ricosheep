"""
Authors: Matthias Brunel
"""
from flinter import View
from colors import *


def settings(args):
    settings = View(10, 10)
    width = View.width
    height = View.height

    def resize():
        nonlocal width, height
        settings.resize(width, height)
        settings.browse("settings")

    def set_width(nb):
        nonlocal width
        try:
            new_width = int(nb)
            assert new_width >= 20
            width = new_width
        except:
            pass

    def set_height(nb):
        nonlocal height
        try:
            new_height = int(nb)
            assert new_height >= 20
            height = new_height
        except:
            pass

    settings.box(0, 0, width=10, height=10, no_pad=True, color=BGCOLOR)
    settings.text_box(3, 0, width=4, text="Settings", color=BGCOLOR, border=BGCOLOR)
    settings.text_box(0, 2, width=2, text="Width:", color=BGCOLOR, border=BGCOLOR)
    settings.text_field(2, 2, width=2, text=str(width), on_enter=set_width)
    settings.text_box(0, 3, width=2, text="Height:", color=BGCOLOR, border=BGCOLOR)
    settings.text_field(2, 3, width=2, text=str(height), on_enter=set_height)
    settings.button(4, 9, color=GREY, text="Apply", on_click=resize)
    settings.button(
        8,
        9,
        width=2,
        color=GREY,
        text="Back",
        on_click=lambda: settings.browse("menu"),
    )
    settings.add_event(lambda: settings.browse("exit"), "Quitte")
    return settings