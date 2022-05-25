"""
Authors: Matthias Brunel
"""
import fltk

class Router:
    def __init__(self, **routes):
        self.routes = routes

    def run(self, view_loader, *args):
        while view_loader:
            view = view_loader(args)
            while not view.new_view:
                view.update()
                view.handle_events()
                fltk.mise_a_jour()
            view_loader = self.routes[view.new_view]
            args = view.args
            fltk.efface_tout()
