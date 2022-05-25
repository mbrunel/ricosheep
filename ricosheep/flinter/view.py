"""
Authors: Matthias Brunel
"""
import fltk

BLACK = "#000000"
WHITE = "#ffffff"

class Event:
    def __init__(self, tag, value, callback):
        self.tag = tag
        self.value = value
        self.callback = callback

    def handle_event(self, e, tag):
        if tag == self.tag:
            if self.tag == "Touche":
                key = fltk.touche(e)
                if not self.value:
                    self.callback(key)
                elif self.value == key:
                    self.callback()
            else:
                self.callback()


class Grid:
    def __init__(self, box, rows, columns):
        ax, ay, bx, by = box
        self.ax = ax
        self.ay = ay
        self.bx = bx
        self.by = by
        self.rows = rows
        self.columns = columns
        self.case_width = (bx - ax) / rows
        self.case_heigth = (by - ay) / columns

    def grid_to_pixel(self, row, column, x_pad, y_pad):
        x = self.ax + row / self.rows * (self.bx - self.ax) + x_pad * self.case_width
        y = (
            self.ay
            + column / self.columns * (self.by - self.ay)
            + y_pad * self.case_heigth
        )
        return x, y

    def compute_box(self, row, column, width, height, l_pad, r_pad, b_pad, t_pad):
        ax, ay = self.grid_to_pixel(row, column, l_pad, t_pad)
        bx, by = self.grid_to_pixel(row + width, column + height, -r_pad, -b_pad)
        return ax, ay, bx, by


class View:
    init = False
    width = 0
    height = 0

    class Box:
        d_pad = 0

        def __init__(self, grid, row, column, **kwargs):
            width = kwargs.get("width", 1)
            height = kwargs.get("height", 1)
            l_pad = kwargs.get("l_pad", View.Box.d_pad)
            r_pad = kwargs.get("r_pad", View.Box.d_pad)
            t_pad = kwargs.get("t_pad", View.Box.d_pad)
            b_pad = kwargs.get("b_pad", View.Box.d_pad)
            no_pad = kwargs.get("no_pad", False)
            if no_pad:
                l_pad = r_pad = t_pad = b_pad = 0
            self.border = kwargs.get("border", BLACK)
            self.color = kwargs.get("color", WHITE)
            self.border_width = kwargs.get("border_width", 1)
            self.img = kwargs.get("image", "")
            self.id = self.img_id = 0
            self.tags = kwargs.get("tags", [])
            self.ax, self.ay, self.bx, self.by = grid.compute_box(
                row, column, width, height, l_pad, r_pad, t_pad, b_pad
            )
            self.width = self.bx - self.ax
            self.height = self.by - self.ay
            self.midx = self.ax + self.width / 2
            self.midy = self.ay + self.height / 2

        def display(self):
            if not self.img:
                self.id = fltk.rectangle(
                    self.ax,
                    self.ay,
                    self.bx,
                    self.by,
                    self.border,
                    self.color,
                    self.border_width,
                )
            self.display_image()

        def erase(self):
            self.erase_image()
            if self.id:
                fltk.efface(self.id)
                self.id = 0

        def display_image(self):
            if self.img:
                self.img_id = fltk.image(
                    self.midx,
                    self.midy,
                    self.img,
                    int(self.width),
                    int(self.height),
                    ancrage="center",
                )

        def erase_image(self):
            if self.img_id:
                fltk.efface(self.img_id)
                self.img_id = 0

        def change(self, **kwargs):
            oldcolor = self.color
            oldborder = self.border
            self.tags += kwargs.get("tags", [])
            rmtag = kwargs.get("rmtag")
            if self.tags.count(rmtag):
                self.tags.remove(rmtag)
            self.color = kwargs.get("color", self.color)
            self.border = kwargs.get("border", self.border)
            oldimg = self.img
            self.img = kwargs.get("image", self.img)
            if oldcolor != self.color or oldborder != self.border or oldimg != self.img:
                self.erase()
                self.display()

    class TextBox(Box):
        d_text_size = 0

        def __init__(self, grid, row, column, **kwargs):
            super().__init__(grid, row, column, **kwargs)
            self.midx = (self.bx + self.ax) / 2
            self.midy = (self.by + self.ay) / 2
            self.text = str(kwargs.get("text", ""))
            self.text_color = kwargs.get("text_color", BLACK)
            self.text_size = kwargs.get("text_size", View.TextBox.d_text_size)
            self.o_text_size = self.text_size
            self.text_font = kwargs.get("text_font", "mono")
            self.fit(self.text)
            self.text_id = 0

        def fit(self, text):
            if text:
                fit = False
                while not fit:
                    h_text, v_text = fltk.taille_texte(
                        text, self.text_font, self.text_size
                    )
                    if h_text < int(self.width) and v_text < int(self.height):
                        fit = True
                    else:
                        self.text_size -= 1

        def _display_text(self, text):
            if text:
                self.text_id = fltk.texte(
                    self.midx,
                    self.midy,
                    text,
                    self.text_color,
                    "center",
                    self.text_font,
                    self.text_size,
                )

        def display_text(self):
            self._display_text(self.text)

        def erase_text(self):
            if self.text_id:
                fltk.efface(self.text_id)
                self.text_id = 0

        def display(self):
            super().display()
            self.display_text()

        def erase(self):
            self.erase_text()
            super().erase()

        def refresh(self):
            self.erase_text()
            self.fit(self.text)
            self.display_text()

        def change(self, **kwargs):
            super().change(**kwargs)
            oldtext = self.text
            self.text = str(kwargs.get("text", self.text))
            if len(oldtext) > len(self.text):
                self.text_size = self.o_text_size
            self.text_color = kwargs.get("text_color", self.text_color)
            self.text_size = kwargs.get("text_size", self.text_size)
            self.text_font = kwargs.get("text_font", self.text_font)
            self.refresh()

    class Button(TextBox):
        def __init__(self, grid, row, column, **kwargs):
            super().__init__(grid, row, column, **kwargs)
            self.on_click = kwargs.get("on_click", lambda: None)
            self.hovered = False
            self.swap_img = kwargs.get("hoverImage", self.img)

        def is_hovered(self):
            x, y = fltk.abscisse_souris(), fltk.ordonnee_souris()
            return self.ax < x < self.bx and self.ay < y < self.by

        def change(self, **kwargs):
            super().change(**kwargs)
            new_on_click = kwargs.get("on_click", None)
            if new_on_click:
                self.on_click = new_on_click

        def fade(self, contrast):
            def add_inbound(n, add):
                return min(255, max(0, int(n + add)))

            if self.img:
                swap = self.swap_img
                self.swap_img = self.img
                self.change(image=swap)
            else:
                c = int(self.color[1:], 16)
                b = add_inbound(c & 255, contrast)
                g = add_inbound((c >> 8) & 255, contrast)
                r = add_inbound((c >> 16) & 255, contrast)
                self.change(color="#%02x%02x%02x" % (r, g, b))

        def update(self):
            if self.hovered != self.is_hovered():
                self.hovered = not self.hovered
                self.fade(((not self.hovered) - self.hovered) * 30)
                if self.hovered:
                    if isinstance(self, View.TextField):
                        fltk.set_cursor("xterm")
                    else:
                        fltk.set_cursor("hand2")
                else:
                    fltk.set_cursor("")

    class TextField(Button):
        def __init__(self, grid, row, column, **kwargs):
            super().__init__(grid, row, column, **kwargs)
            self.active = False
            self.on_enter = kwargs.get("on_enter", lambda text: None)
            self.p_cursor = 0

        def change(self, **kwargs):
            super().change(**kwargs)
            new_on_enter = kwargs.get("on_click", None)
            if new_on_enter:
                self.on_click = new_on_enter

        def display_text(self):
            text = self.text
            cursor = "│" if self.active else ""
            pos = len(text) - self.p_cursor
            text = text[:pos] + cursor + text[pos:]
            self.fit(text)
            return self._display_text(text)

    def __init__(self, rows, column, width=1280, height=720, d_pad=0.1, d_text_size=24):
        if not View.init:
            self.__init_fltk(width, height)
        self.grids = {"root": Grid((0, 0, View.width, View.height), rows, column)}
        self.statics = []
        self.dynamics = []
        self.bound_events = []
        self.active_field = None
        self.new_view = ""
        self.add_event(self.__click_handler, "ClicGauche")
        self.add_event(self.__write_handler, "Touche")
        View.Box.d_pad = d_pad
        View.TextBox.d_text_size = d_text_size

    def __init_fltk(self, width, height):
        fltk.cree_fenetre(width, height)
        View.width = width
        View.height = height
        View.init = True

    def close(self):
        fltk.ferme_fenetre()
        View.init = False

    def resize(self, width, height):
        self.close()
        self.__init_fltk(width, height)

    def box(self, row, column, **kwargs):
        self.statics.append(
            View.Box(self.grids[kwargs.pop("grid", "root")], row, column, **kwargs)
        )
        self.statics[-1].display()

    def text_box(self, row, column, **kwargs):
        self.statics.append(
            View.TextBox(self.grids[kwargs.pop("grid", "root")], row, column, **kwargs)
        )
        self.statics[-1].display()

    def button(self, row, column, **kwargs):
        self.dynamics.append(
            View.Button(self.grids[kwargs.pop("grid", "root")], row, column, **kwargs)
        )
        self.dynamics[-1].display()

    def text_field(self, row, column, **kwargs):
        def activate(self, field):
            self.active_field = field
            field.active = True
            field.refresh()
            fltk.set_cursor("")

        field = View.TextField(
            self.grids[kwargs.pop("grid", "root")], row, column, **kwargs
        )
        field.on_click = lambda: activate(self, field)
        self.dynamics.append(field)
        if kwargs.get("active"):
            field.on_click()
        field.display()

    def grid(self, name, row, column, width, height, nb_rows, nb_columns):
        self.grids[name] = Grid(
            self.grids["root"].compute_box(row, column, width, height, 0, 0, 0, 0),
            nb_rows,
            nb_columns,
        )

    def __click_handler(self):
        if self.active_field:
            self.active_field.on_enter(self.active_field.text)
            self.active_field.active = False
            self.active_field.refresh()
            self.active_field = None
        for button in self.dynamics:
            if button.is_hovered():
                button.on_click()

    def __write_handler(self, key):
        if not self.active_field:
            return
        widget = self.active_field
        if key == "Return":
            widget.on_enter(widget.text)
            return
        text = widget.text
        pos = len(text) - widget.p_cursor

        full_name_table = {
            "ampersand": "&",
            "eacute": "é",
            "quotedbl": '"',
            "apostrophe": "'",
            "parenleft": "(",
            "minus": "-",
            "egrave": "è",
            "underscore": "_",
            "ccedilla": "ç",
            "agrave": "à",
            "asciitilde": "~",
            "numbersign": "#",
            "braceleft": "{",
            "bracketleft": "[",
            "bar": "|",
            "grave": "`",
            "backslash": "\\",
            "asciicircum": "^",
            "at": "@",
            "bracketright": "]",
            "braceright": "}",
            "parenright": ")",
            "equal": "=",
            "degree": "°",
            "plus": "+",
            "asterisk": "*",
            "mu": "µ",
            "dollar": "$",
            "sterling": "£",
            "percent": "%",
            "ugrave": "ù",
            "quotedbl": '"',
            "asciicircum": "^",
            "section": "§",
            "exclam": "!",
            "slash": "/",
            "colon": ":",
            "period": ".",
            "semicolon": ";",
            "question": "?",
            "comma": ",",
            "space": " ",
        }

        if key in full_name_table:
            text = text[:pos] + full_name_table[key] + text[pos:]
        elif len(key) == 1:
            text = text[:pos] + key + text[pos:]
        elif key == "BackSpace" and pos >= 0:
            text = text[: pos - 1] + text[pos:]
        elif key == "Delete" and pos < len(text):
            text = text[:pos] + text[pos + 1 :]
            widget.p_cursor -= 1
        elif key == "Left" and widget.p_cursor < len(text):
            widget.p_cursor += 1
        elif key == "Right" and widget.p_cursor > 0:
            widget.p_cursor -= 1
        elif key == "Home":
            widget.p_cursor = len(text)
        elif key == "End":
            widget.p_cursor = 0

        widget.change(text=text)

    def add_event(add_event, callback, type, value=0):
        add_event.bound_events.append(Event(type, value, callback))

    def change(self, tag, **kwargs):
        def search(list, tag, **kwargs):
            for e in list:
                for etag in e.tags:
                    if etag == tag:
                        e.change(**kwargs)

        search(self.statics, tag, **kwargs)
        search(self.dynamics, tag, **kwargs)

    def delete(self, tag):
        def search(list, tag):
            for e in reversed(list):
                for etag in e.tags:
                    if etag == tag:
                        e.erase()
                        list.remove(e)

        search(self.statics, tag)
        search(self.dynamics, tag)
        if self.active_field and not self.active_field.textId:
            self.active_field = None

    def browse(self, new_view, *args):
        self.new_view = new_view
        self.args = args

    def update(self):
        for widget in self.dynamics:
            widget.update()

    def handle_events(self):
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev)
        for bound_event in self.bound_events:
            bound_event.handle_event(ev, tev)

    # def display(self):
    #     for widget in self.statics:
    #         widget.display()
    #     for widget in self.dynamics:
    #         widget.display()
