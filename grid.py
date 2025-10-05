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
        self.colors = None

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
        initial_state.get = self.get
        initial_state.size = [8,8]
        initial_state.colors = ["black", "white"]
        initial_state.next_frame = self.next_frame
        initial_state.move = 0
        initial_state.win = self.win
        initial_state.lose = self.lose
        initial_state.level = 1
        initial_state.attempt = 1
        initial_state.max_moves = float('inf')
        initial_state.max_attempts = float('inf')
        initial_state.max_levels = 8
        initial_state.event = {"type": "init"}
        initial_state.intended_actions = [[]]

        # these methods are not deepcopied because they are bound to the original object
        initial_state._no_deepcopy_keys = ["set", "get", "next_frame", "win", "lose"]


        # if no initialize method is set, the default values will remain
        if self.initialize_method != None:
            self.initialize_method(initial_state)
        
        # ensure size and colors are public variables
        self.size = initial_state.size
        self.colors = initial_state.colors

        assert(self.current_state == None)

        symbols = len(self.colors)
        initial_state.grid = grid(self.size, symbols)

        self.current_state = initial_state



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

from grid_methods.begin import begin
grid_stateful.begin = begin

from grid_methods.colors import _state_to_color, make_color_grid
grid_stateful._state_to_color = _state_to_color
grid_stateful.make_color_grid = make_color_grid

from grid_methods.events import input
grid_stateful.input = input

from grid_methods.get import get
grid_stateful.get = get

from grid_methods.lose import lose
grid_stateful.lose = lose

from grid_methods.press_button import press_button
grid_stateful.press_button = press_button

from grid_methods.press_tile import press_tile
grid_stateful.press_tile = press_tile

from grid_methods.reset import reset
grid_stateful.reset = reset

from grid_methods.actions import resolve_action, has_intended_actions, resolve_intended_actions, next_frame
grid_stateful.resolve_action = resolve_action
grid_stateful.has_intended_actions = has_intended_actions
grid_stateful.resolve_intended_actions = resolve_intended_actions
grid_stateful.next_frame = next_frame

from grid_methods.set import set
grid_stateful.set = set

from grid_methods.undo import undo
grid_stateful.undo = undo

from grid_methods.update import update
grid_stateful.update = update

from grid_methods.win import win
grid_stateful.win = win
