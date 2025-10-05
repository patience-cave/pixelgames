
_color_to_rgb = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "green": (0, 255, 0),
    "dark green": (0, 150, 0),
    "red": (255, 0, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "magenta": (255, 0, 255),
    "cyan": (0, 255, 255),
    "gray": (128, 128, 128)
}


def _state_to_color(self, state):
    return _color_to_rgb[self.colors[state]]


def make_color_grid(self):
    return [[
            self._state_to_color(self.get([x, y]))
        for y in range(self.size[0])] for x in range(self.size[1])]
