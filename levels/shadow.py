from game_template import game_template
from useful_objects import levels_left, moves_left, on_board, border, floor
from helper import iterate_over_2D, lists_match, sort_objects_by_positions, diagonals, position_in_bounds


class objects:
    def __init__(self, game, input={}):
        self.id = "objects"
        self.colors = {
            "wall": "black",
            "swapper": "gray",
            "exit": "blue",
            "transition": "black",
        }
        self.layers = []
        for i in input.get("layers") or []:
            layer = {
                "walls": [],
                "swappers": [],
                "exits": [],
            }
            
            for x, y, item in iterate_over_2D(i):
                if item == "x":
                    layer["walls"].append([x, y])
                elif item == "o":
                    layer["swappers"].append([x, y])
                elif item == "e":
                    layer["exits"].append([x, y])
                
            self.layers.append(layer)
            
        game.current_layer = 0

    def render(self, game):
        for position in self.layers[game.current_layer]["walls"]:
            game.set(position, "wall")
        for position in self.layers[game.current_layer]["swappers"]:
            game.set(position, "swapper")
        for position in self.layers[game.current_layer]["exits"]:
            game.set(position, "exit")

    def reach_exit(self, game, position):
        # remove this position from the exit list
        self.layers[game.current_layer]["exits"].remove(position)

        game.win = True
        for layer in self.layers:
            if layer["exits"] != []:
                game.win = False
                break

    def get_object(self, game, position):
        for object_type in self.layers[game.current_layer]:
            for _position in self.layers[game.current_layer][object_type]:
                if position == _position:
                    if object_type == "exits":
                        return "exit"
                    elif object_type == "swappers":
                        return "swapper"
                    elif object_type == "walls":
                        return "wall"
        return "floor"

    def next_layer(self, game):

        if not game.find_object("characters").some_characters_stepping_on_swapper(game):
            return

        diags = diagonals(game.board_size)

        # for positions in diags:
        #     for position in positions:
        #         if self.get_object(game, position) != "swapper": 
        #             game.set(position, "transition")
                
            #game.next_frame()

        next_layer = game.current_layer + 1
        next_layer %= len(self.layers)

        _characters = game.find_object("characters")

        for character in _characters.all_characters_on_layer(game):
            if character["stepping_on"] == "swapper":
                character["on_layer"] = next_layer
        
        game.current_layer = next_layer

        for positions in diags:
            for position in positions:
                game.set(position, self.get_object(game, position))
        
        # when a character swaps layers, set what it's stepping on to be what it is standing on now
        for character in _characters.all_characters_on_layer(game):
            should_step_on = game.get(character["position"])
            game.set(character["position"], "character")
            character["stepping_on"] = should_step_on



class characters:
    def __init__(self, game, input={}):
        self.id = "characters"
        self.colors = {
            "character": "soft blue"
        }
        self.characters = input.get("characters") or []
        for character in self.characters:
            if "stepping_on" not in character:
                character["stepping_on"] = "floor"
            if "on_layer" not in character:
                character["on_layer"] = 0
    
    def render(self, game):
        for character in self.characters:
            if character["on_layer"] != game.current_layer:
                continue
            position = character["position"]
            game.set(position, "character")

    def player_at(self, game, position):
        for character in self.characters:
            if character["on_layer"] != game.current_layer:
                continue
            if character["position"] == position:
                return True
        return False

    def move(self, game, dx, dy):

        positions = [character["position"] for character in self.characters]
        for character in sort_objects_by_positions(self.characters, positions, dx, dy):

            if character["stepping_on"] == "wall":
                game.set(character["position"], "wall")
                game.lose = True
                return
                
            # do not move character if they are not on the current layer
            if character["on_layer"] != game.current_layer:
                continue

            new_position = [character["position"][0] + dx, character["position"][1] + dy]

            if not position_in_bounds(game, new_position):
                continue
            
            was_stepping_on = character["stepping_on"]

            if game.get(new_position) == "wall":
                continue
            elif game.get(new_position) == "swapper":
                character["stepping_on"] = "swapper"
            elif game.get(new_position) == "floor":
                character["stepping_on"] = "floor"
            elif game.get(new_position) == "exit":
                _objects = game.find_object("objects")
                _objects.reach_exit(game, new_position)

            game.set(character["position"], was_stepping_on)
            game.set(new_position, "character")
            character["position"] = new_position

    def some_characters_stepping_on_swapper(self, game):
        for character in self.characters:
            if character["on_layer"] != game.current_layer:
                continue
            if character["stepping_on"] == "swapper":
                return True
        return False

    def all_characters_on_layer(self, game):
        _characters = []
        for character in self.characters:
            if character["on_layer"] != game.current_layer:
                continue
            _characters.append(character)
        return _characters


class shadow_game(game_template):
    def __init__(self, game):
        self.game_name = "shadow"
        game.size = [64, 64]
        
        game.list_of_objects = {
            "moves_left": moves_left,
            "levels_left": levels_left,
            "border": border,
            "floor": floor,
            "characters": characters,
            "objects": objects,
        }

    def press_button(self, game, button):

        if button.name == "space":
            game.find_object("objects").next_layer(game)
        else:
            game.find_object("characters").move(game, button.dx, button.dy)

        if game.is_modified():
            game.find_object("moves_left").use_move(game)
            game.find_object("levels_left").update_level(game)
