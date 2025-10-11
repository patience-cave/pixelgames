from game_template import game_template
from useful_objects import levels_left, moves_left, on_board, border, floor
from helper import iterate_over_2D, lists_match, sort_objects_by_positions, diagonals, position_in_bounds, convert_tile_to_board, frontier_positions


class theory:
    def __init__(self, game, input={}):
        self.id = "theory"
        self.colors = {
            "red-blob": (200, 0, 0),
            "red-end": (200, 0, 0),
            "orange-blob": (200, 50, 0),
            "orange-end": (200, 60, 0),
            "yellow-blob": (200, 200, 0),    
            "yellow-end": (200, 200, 0),    
            "green-blob": (0, 150, 0),
            "green-end": (0, 150, 0),
            "blue-blob": (50, 50, 250),
            "blue-end": (50, 50, 250),
            "purple-blob": (120, 55, 160),
            "purple-end": (120, 55, 160),
            "brown-blob": "brown",
            "brown-end": "light brown",
            "black-block": "black",
        }
        self.positions = {}
        codes = {
            "r": "red-blob", "R": "red-end",
            "o": "orange-blob", "O": "orange-end",
            "y": "yellow-blob", "Y": "yellow-end",
            "g": "green-blob", "G": "green-end",
            "b": "blue-blob", "B": "blue-end",
            "p": "purple-blob", "P": "purple-end",
            "n": "brown-blob", "N": "brown-end",
            "x": "black-block",
            ".": "floor"
        }
        for x, y, item in iterate_over_2D(input["board"]):
            self.positions[(x, y)] = codes[item]

    def render(self, game):
        for position, color in self.positions.items():
            if color.endswith("-end"):
                game.set(position, color)
                for i in range(game.resolution[0]):
                    fixed_pos_x = position[0] * game.resolution[0]
                    fixed_pos_x2 = position[0] * game.resolution[0] + game.resolution[0] - 1
                    fixed_pos_y = position[1] * game.resolution[1]
                    fixed_pos_y2 = position[1] * game.resolution[1] + game.resolution[1] - 1
                    game.set([fixed_pos_x, fixed_pos_y + i], "floor", _resolution=False)
                    game.set([fixed_pos_x2, fixed_pos_y + i], "floor", _resolution=False)
                    game.set([fixed_pos_x + i, fixed_pos_y], "floor", _resolution=False)
                    game.set([fixed_pos_x + i, fixed_pos_y2], "floor", _resolution=False)
            else:
                game.set(position, color)
    
    def get_tile(self, game, position):
        _position = (position[0], position[1])
        return self.positions.get(_position, "floor")

    def blob(self, game, position):
        expanded_positions = set()
        unexpanded_positions = set()
        unexpanded_positions.add((position[0], position[1]))
        tile = self.get_tile(game, position)

        while unexpanded_positions:
            _position = unexpanded_positions.pop()
            expanded_positions.add(_position)
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                
                new_position = (_position[0] + dx, _position[1] + dy)
                
                if not position_in_bounds(game, new_position):
                    continue
                if new_position in expanded_positions:
                    continue

                new_tile = self.get_tile(game, new_position)
                if new_tile != tile:
                    continue
                    
                unexpanded_positions.add(new_position)

        return expanded_positions

    def expand_blob(self, game, position):
        tile = self.get_tile(game, position)
        frontier = frontier_positions(self.blob(game, position))

        for position in frontier:
            if not position_in_bounds(game, position):
                continue
            new_tile = self.get_tile(game, position)

            if new_tile == "floor":
                game.set(position, tile)
                self.positions[position] = tile
            elif new_tile == "black-block":
                continue
            elif new_tile.endswith("-end"):
                # do the colors match
                if tile.split("-")[0] == new_tile.split("-")[0]:
                    game.set(position, tile)
                    self.positions[position] = tile
            else:
                mix_codes = {
                    "red-yellow": "orange",
                    "yellow-red": "orange",
                    "red-blue": "purple",
                    "blue-red": "purple",
                    "yellow-blue": "green",
                    "blue-yellow": "green",
                    "red-orange": "orange",
                    "orange-red": "red",
                    "orange-yellow": "yellow",
                    "yellow-orange": "orange",
                    "yellow-green": "green",
                    "green-yellow": "yellow",
                    "green-blue": "blue",
                    "blue-green": "green",
                    "blue-purple": "purple",
                    "purple-blue": "blue",
                    "red-purple": "purple",
                    "purple-red": "red"
                }
                mixture = tile.split("-")[0] + "-" + new_tile.split("-")[0]
                if mixture in mix_codes:
                    blob_name = mix_codes[mixture] + "-blob"
                    game.set(position, blob_name)
                    self.positions[position] = blob_name
                else:
                    game.set(position, "brown-blob")
                    self.positions[position] = "brown-blob"



    def tapped(self, game, position):
        if not position_in_bounds(game, position):
            return
        tile = self.get_tile(game, position)

        if tile.endswith("-blob"):
            self.expand_blob(game, position)
        
        



class colortheory_game(game_template):
    def __init__(self, game):
        self.game_name = "colortheory"
        game.size = [64, 64]
        
        game.list_of_objects = {
            "moves_left": moves_left,
            "levels_left": levels_left,
            "border": border,
            "floor": floor,
            "theory": theory
        }

    def press_tile(self, game, tile):

        converted_tile = convert_tile_to_board(game, tile)

        game.find_object("theory").tapped(game, converted_tile)

        if game.is_modified():
            game.find_object("moves_left").use_move(game)
            game.find_object("levels_left").update_level(game)

