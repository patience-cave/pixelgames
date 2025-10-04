

def _get(bits, at): return (bits >> at) % 2 # == 1
def _paint(bits, at): 
    bits |= 1 << at
    return bits
def _erase(bits, at, valid=False):
    if valid or _get(bits, at):
        bits -= 1 << at
    return bits
# set can only be 0 or 1
def _set(bits, at, to):
    if _get(bits, at):
        if not to:
            return _erase(bits, at, True)
    else:
        if to:
            return _paint(bits, at)
    return bits

def _valid_position(size, position):
    dimensions = len(size)
    if not dimensions: return False
    for i, value in enumerate(position):
        if i > 0 and i >= dimensions: return False
        if value < 0: return False
        if value >= size[i]: return False
    return True

# assuming the position is valid
def _position_to_at(size, position):
    s = position[0]
    m = 1
    for i, pos in enumerate(position[1:]):
        m *= size[i]
        s += m * pos
    return s

class bitgrid:
    def __init__(self, dimension, rep=0):
        self.size = dimension
        self.bits = rep

    def paint(self, at):
        self.bits = _paint(self.bits, at)

    def erase(self, at):
        self.bits = _erase(self.bits, at)

    def get(self, at):
        return _get(self.bits, at)

    # returns true if modified
    def set(self, at, to):
        oldbits = self.bits
        self.bits = _set(self.bits, at, to)
        return self.bits != oldbits

    def __str__(self): return f"{self.bits}"
    def __repr__(self): return f"bitgrid({self.bits})"

class grid:
    def __init__(self, dimension, symbols):
        """
        dimension : the dimension of the grid (i.e. 8x8)
        symbols : the number of different states a pixel can be
        """

        self.size = dimension

        self.bitgrids = []
        self.symbols = symbols

        while symbols:
            symbols >>= 1
            self.bitgrids.append(bitgrid(dimension))

    def location_exists(self, position):
        return _valid_position(self.size, position)

    # assuming position exists
    def get(self, position):
        at = _position_to_at(self.size, position)
        symbol = 0
        
        for i, bitgrid in enumerate(self.bitgrids):
            symbol += bitgrid.get(at) << i
        
        assert(symbol < self.symbols)

        return symbol

    # return True means modifications were made
    def set(self, position, to):
        if to >= self.symbols: return False
        if not self.location_exists(position): return False

        at = _position_to_at(self.size, position)

        bits = []
        for i in range(len(self.bitgrids)):
            bits.append(to % 2)
            to >>= 1

        modified = False
        for bit, bitgrid in zip(bits, self.bitgrids):
            o = bitgrid.set(at, bit)
            modified = o or modified

        return modified

    def __str__(self):
        return f"{[i.bits for i in self.bitgrids]}"



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


class State(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self

    def __deepcopy__(self, memo):
        copied = State(copy.deepcopy(dict(self), memo))
        return copied

def remove_empty_elements(l):
    return [x for x in l if x != []]


import copy

"""
symbols need colors lol
every color change needs to be saved as an action
"""
class grid_stateful:

    def __init__(self):

        #self.grid = grid(dimension, symbols)
        self.moves = []
        self.animations = [] # if an animation plays post action, wait for it to be complete
        
        # the game will look to this to re-paint pixels
        # if this list is > 1, it will turn into an animation
        self.intended_actions = [[]]
        self.states = [] # automatically, the current state is {} an empty dict

        self.begin_method = None
        self.press_tile_method = None
        self.press_button_method = None
        self.initialize_method = None
        self.colors = None
        self.grid = None

        self.methods = State()
        self.methods.set = self.set
        self.methods.get = self.get
        self.methods.size = [8,8]
        self.methods.colors = ["black", "white"]
        self.methods.next_frame = self.new_frame
        self.methods.moves = 0

    def initialize(self):

        if self.initialize_method != None:
            self.initialize_method(self.methods)
        
        self.size = self.methods.size
        self.colors = self.methods.colors

        if self.grid == None:
            symbols = len(self.colors)
            self.grid = grid(self.size, symbols)
        else:
            for x in range(self.size[0]):
                for y in range(self.size[1]):
                    self.set([x,y],0)

    def _state_to_color(self, state):
        return _color_to_rgb[self.colors[state]]

    def new_frame(self):
        self.intended_actions.append([])

    def set(self, position, to):
        
        previous_state = self.grid.get(position)

        if self.grid.set(position, to):

            new_state = self.grid.get(position)

            # if the previous color state equals the new color state cancel the action
            if previous_state == new_state:
                return

            self.intended_actions[-1].append({
                "type": "change_color",
                "position": position,
                "from_color": previous_state,
                "to_color": new_state
            })

    def get(self, position):
        if self.grid.location_exists(position):
            return self.grid.get(position)
        return -1

    # returns the current action plus and animation buffer
    # returns the full animation [[action], [action], [action], ...]
    def resolve_action(self, a, isundo=False):

        if a == None:
            return []

        if a["type"] == "change_color":

            # swap colors if undoing, don't forget to force change the color state
            if isundo:
                self.grid.set(a["position"], a["from_color"])
                a["from_color"], a["to_color"] = a["to_color"], a["from_color"]

            return [[{
                "result": "change_color",
                "position": a["position"],
                "to_color": self._state_to_color(a["to_color"])
            }]]

        elif a["type"] == "animation":

            # play the animation backwards if you are undoing
            if isundo:
               a["list"] = a["list"][::-1]

            o = []
            for i in a['list']:
                p = self.resolve_action(i, isundo)
                o += p
            return o

            # # the first frame of the animation should happen
            # first_animation = a["list"][0]
            # resolve_first_animation = self.resolve_action(first_animation, isundo)

            # animations_buffer = [self.resolve_action(i, isundo) for i in a['list'][1:]]

            # animations, buffer = 

            # self.animations += [self.resolve_action(i, isundo) for i in a['list'][1:]]

            # return resolve_first_animation

        elif a["type"] == "many":

            # it probably makes sense to play all changes backwards too if undoing
            if isundo:
                a["list"] = a["list"][::-1]

            o = [[]]
            for i in a['list']:
                p = self.resolve_action(i, isundo)
                if len(p) == 1:
                    o[-1] += p[0]
                else:
                    o += p
                    o += [[]]
            o = remove_empty_elements(o)

            return o

        elif a["type"] == "undo":
            assert(not isundo)
            return self.resolve_action(a["action"], True)

    def has_intended_actions(self):

        self.intended_actions = remove_empty_elements(self.intended_actions)

        for i in self.intended_actions:
            if i: return True

        self.intended_actions = [[]]
        return False

    def resolve_intended_actions(self, ia):

        if not self.has_intended_actions(): return
        # if the final animation has not been populated, remove it
        while len(ia) and (not ia[-1]): ia.pop(-1)
        assert(ia)

        # if there is only one action to animate
        if len(ia) == 1:

            _intended_action = ia[0]

            if len(_intended_action) == 1:
                return _intended_action[0]
            else:
                return {
                    "type": "many",
                    "list": _intended_action
                }

        # longer animation
        else:
            return {
                "type": "animation",
                "list": [self.resolve_intended_actions([i]) for i in ia]
            }


    def update(self):

        # assert(len(self.moves) == len(self.states))

        # if an animation is currently happening, keep resolving it each update
        if self.animations:
            # print('animating...')
            animation = []

            current_animation = self.animations[0]
            self.animations = self.animations[1:]

            return current_animation

        # if there is no action, kill the function early
        if not self.intended_actions[0]:
            return []

        # print('updating...')

        action = self.resolve_intended_actions(self.intended_actions)
        self.intended_actions = [[]]

        # if the action is not an undo, preserve it in the action history
        if not action["type"] == "undo":
            self.moves.append(action)

        # if it returns more than one action
        # pop the other actions into the animation

        actions = self.resolve_action(action)

        first_action = actions.pop(0)
        self.animations = actions

        return first_action# self.resolve_action(action)

    def press_tile(self, position):
        if self.animations: return []

        if self.press_tile_method != None:
            current_state = copy.deepcopy(self.states[-1])
            self.press_tile_method(self.methods, current_state, position[0], position[1])

            # do not save the new state if no changes happened on screen
            if self.has_intended_actions():
                self.methods.moves += 1
                self.states.append(current_state)


    def press_button(self, button):
        if self.animations: return []

        if button == "reset":
            self.reset()
            return
        elif button == "undo":
            self.undo()
            return

        button_state = State()
        button_state.dx = 0
        button_state.dy = 0
        button_state.up = button == 'up'
        button_state.down = button == 'down'
        button_state.right = button == 'right'
        button_state.left = button == 'left'

        if button_state.up or button_state.down:
            button_state.dy = 1 if button_state.up else -1
        else:
            button_state.dx = 1 if button_state.right else -1

        if self.press_button_method != None:
            current_state = copy.deepcopy(self.states[-1])
            self.press_button_method(self.methods, current_state, button_state)
            #self.press_button_method(button_state, current_state, self.set, self.get)
            # do not save the new state if no changes happened on screen
            if self.has_intended_actions():
                self.methods.moves += 1
                self.states.append(current_state)

    def begin(self):
        if self.moves == []:
            if self.begin_method != None:
                current_state = State()
                self.begin_method(self.methods, current_state)
                self.states.append(current_state)


    def undo(self):
        if self.intended_actions[0]: return
        if self.animations: return
        if len(self.moves) <= 1: return

        a = self.moves[-1]

        self.intended_actions[-1].append({
            "type": "undo",
            "action": a
        })

        self.states.pop()
        self.moves.pop()

    def reset(self):

        if self.intended_actions[0]: return
        if self.animations: return
        if len(self.moves) <= 1: return

        self.intended_actions[-1].append({
            "type": "undo",
            "action": {
                "type": "animation",
                "list": self.moves[1:]
            }
        })

        self.states = [self.states[0]]
        self.moves = [self.moves[0]]

        # self.states = []
        # self.moves = []
        #self.animations = []
        #self.intended_actions = [[]]

        #self.initialize()
        #self.begin()
        pass

    def make_color_grid(self):
        return [[
                self._state_to_color(self.grid.get([x, y]))
            for y in range(self.grid.size[0])] for x in range(self.grid.size[1])]

    def input(self, code):

        if type(code) is str:
            event = code
        else:
            event = code['event']

        if event == "press_tile":
            self.press_tile(code['position'])

        elif event == "press_button":
            self.press_button(code['button'])

        elif event == "begin":
            self.begin()

        elif event == "undo":
            self.undo()

        elif event == "reset":
            self.reset()

        elif event == "init":
            self.initialize()

        elif event == "color_grid":
            return self.make_color_grid()

        elif event == "update":
            return self.update()

        elif event == "new_frame":
            self.new_frame()
