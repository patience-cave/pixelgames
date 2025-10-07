from mimetypes import init
from bitpacking import grid
from state import State

"""
symbols need colors lol
every color change needs to be saved as an action
"""
class grid_stateful:

    def __init__(self):

        self.current_state = None

        self.size = None
        self.actual_size = None
        self.resolution = None
        
        self._colors = None
        self._color_map = None

        # --------------------------------
        # Game States, Actions, and Animations
        # --------------------------------

        # history of previous states
        self.states: list[State] = []

        # if this list is not empty, an animation is playing
        # wait for it to be empty before new events are processed
        self.animations = []
        
        # the game will look to this to re-paint pixels
        # if this list is > 1, it will turn into an animation
        self.intended_actions = [[]]
        
        # --------------------------------
        # Event Functions
        # The event functions get processed in level.py
        # --------------------------------

        # call when the game is initialized
        # this is where you set the grid size and colors
        self.initialize_method = None

        # call when the game begins
        # this is where you set the initial state of the grid
        self.begin_method = None

        # call when a tile is pressed
        self.press_tile_method = None

        # call when a button is pressed
        self.press_button_method = None


    # The Initialize Event
    def initialize(self):

        # cleanse the game variables
        self.animations = []
        self.states = [State()]

        initial_state = self.states[0]

        initial_state.set = self.set
        initial_state.get = self.special_get
        initial_state.size = [8,8]
        initial_state.resolution = [1, 1]
        initial_state.actual_size = [8,8]

        # initial_state.objects = []
        self._colors = {
            "empty": State({"index": 0, "name": "black", "rgb": (0,0,0)}),
            "win": State({"index": 1, "name": "green", "rgb": (0,255,0)}),
            "lose": State({"index": 2, "name": "red", "rgb": (255,0,0)})
        }
        self._color_map = ["empty", "win", "lose"]

        initial_state.add_colors = self.add_colors
        initial_state.set_background = self.set_background
        initial_state.contains = self.contains
        initial_state.contains_either = self.contains_either

        initial_state.next_frame = self.next_frame
        initial_state.move = 0
        initial_state.win = False
        initial_state.lose = False
        initial_state.level = 1
        initial_state.attempt = 1
        initial_state.max_moves = float('inf')
        initial_state.max_attempts = float('inf')
        initial_state.max_levels = 8
        initial_state.event = {"type": "init"}
        initial_state.intended_actions = [[]]

        # these methods are not deepcopied because they are bound to the original object
        initial_state._no_deepcopy_keys = ["set", "get", "next_frame", "add_colors", "set_background", "contains"]


        assert(self.current_state == None)
        self.current_state = initial_state

        # if no initialize method is set, the default values will remain
        if self.initialize_method != None:
            self.initialize_method(initial_state)

            # correct the actual size given the resolution
            if type(initial_state.resolution) == int:
                initial_state.resolution = [initial_state.resolution] * len(initial_state.size)
            assert(len(initial_state.size) == len(initial_state.resolution))
            initial_state.actual_size = [i * j for i,j in zip(initial_state.size, initial_state.resolution)]

        # ensure size and colors are public variables
        self.size = initial_state.size
        self.resolution = initial_state.resolution
        self.actual_size = initial_state.actual_size

        # self._colors = initial_state._colors
        # self._color_map = initial_state._color_map

        symbols = len(self._color_map)
        initial_state.grid = grid(self.actual_size, symbols)



    def iterate_grid(self):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                yield [x,y]
    

    def current_grid(self):
        return self.current_state.grid

    def previous_state(self):
        return self.states[-1]

    def previous_grid(self):
        return self.states[-1].grid


# --------------------------------
# Importing the various methods
# --------------------------------

try:
    from grid_methods.begin import begin
    from grid_methods.add_object import add_object, get_object
    from grid_methods.colors import _state_to_color, make_color_grid, add_colors, set_background
    from grid_methods.events import input
    from grid_methods.get import get, contains, special_get, contains_either
    from grid_methods.lose import lose
    from grid_methods.press_button import press_button
    from grid_methods.press_tile import press_tile
    from grid_methods.reset import reset
    from grid_methods.actions import resolve_action, has_intended_actions, resolve_intended_actions, next_frame
    from grid_methods.set import set
    from grid_methods.undo import undo
    from grid_methods.update import update
    from grid_methods.win import win
except:
    from begin import begin
    from add_object import add_object, get_object
    from colors import _state_to_color, make_color_grid, add_colors, set_background
    from events import input
    from get import get, contains, special_get, contains_either
    from lose import lose
    from press_button import press_button
    from press_tile import press_tile
    from reset import reset
    from actions import resolve_action, has_intended_actions, resolve_intended_actions, next_frame
    from set import set
    from undo import undo
    from update import update
    from win import win


grid_stateful.begin = begin

grid_stateful.add_object = add_object
grid_stateful.get_object = get_object

grid_stateful._state_to_color = _state_to_color
grid_stateful.make_color_grid = make_color_grid
grid_stateful.add_colors = add_colors
grid_stateful.set_background = set_background

grid_stateful.input = input

grid_stateful.get = get
grid_stateful.contains = contains
grid_stateful.special_get = special_get
grid_stateful.contains_either = contains_either

grid_stateful.lose = lose

grid_stateful.press_button = press_button

grid_stateful.press_tile = press_tile

grid_stateful.reset = reset

grid_stateful.resolve_action = resolve_action
grid_stateful.has_intended_actions = has_intended_actions
grid_stateful.resolve_intended_actions = resolve_intended_actions
grid_stateful.next_frame = next_frame

grid_stateful.set = set

grid_stateful.undo = undo

grid_stateful.update = update

grid_stateful.win = win
