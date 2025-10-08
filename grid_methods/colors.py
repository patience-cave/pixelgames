from state import State

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
    "gray": (128, 128, 128),
    "light gray": (210, 210, 210),
    "dark gray": (50, 50, 50),
    "purple": (160, 85, 200),
    "orange": (255, 165, 0),
    "dark red": (150, 0, 0),
    "pink": (255, 105, 180),
    "soft blue": (115, 144, 250),
}


def set_background(self, color):
    if color in _color_to_rgb:
        self._colors['empty'] = State({"index": 0, "name": color, "rgb": _color_to_rgb[color]})



def add_colors(self, colors):

    current_index = 0
    if self._color_map is not None:
        current_index = len(self._color_map)
    
    for color in colors:

        if color in self._colors:
            continue
            
        s = State()
        s.index = current_index
        current_index += 1
        s.name = color
        s.rgb = self._state_to_color(colors[color])
        self._colors[color] = s

        self._color_map.append(color)
    



def _state_to_color(self, state):
    if isinstance(state, str):
        if state in _color_to_rgb:
            return _color_to_rgb[state]
        else:
            return (255, 255, 255)
    elif isinstance(state, int):
        return self._colors[self._color_map[state]].rgb

    return state



def make_color_grid(self):
    return [[
            self._state_to_color(self.get([x, y]))
        for y in range(self.actual_size[0])] for x in range(self.actual_size[1])]
