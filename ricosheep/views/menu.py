from flinter import View

def menu(args):
    menu = View(12, 12)
    menu.add_event(lambda: menu.browse("exit"), "Quitte")
    return menu