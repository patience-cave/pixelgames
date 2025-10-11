from hmac import new
from game_template import game_template
from useful_objects import levels_left, moves_left, on_board, border, floor
from helper import iterate_over_2D, lists_match, sort_objects_by_positions, diagonals, position_in_bounds, convert_tile_to_board, frontier_positions, safest_next_move


class chaser:
    def __init__(self, game, input={}):
        self.id = "chaser"
        self.colors = {
            "chaser": "purple",
        }
        self.position = input.get("position") or []
    
    def render(self, game):
        game.set(self.position, "chaser")
    
    def move(self, game, dx, dy):
        new_position = [self.position[0] + dx, self.position[1] + dy]
        
        if not position_in_bounds(game, new_position):
            return
        
        new_tile = game.get(new_position)

        if new_tile == "runner":
            game.find_object("runners").eat_runner(game, new_position)
            game.set(self.position, "floor")
            game.set(new_position, "chaser")
        elif new_tile == "floor":
            game.set(self.position, "floor")
            game.set(new_position, "chaser")
            self.position = new_position
        elif new_tile == "box":
            if game.find_object("walls").push_box(game, new_position, dx, dy):
                game.set(self.position, "floor")
                game.set(new_position, "chaser")
                self.position = new_position
            else:
                return
        else:
            return
        
    # def distance_from_runner(self, game, position, naive=False):
    #     if naive:
    #         return abs(self.position[0] - position[0]) + abs(self.position[1] - position[1])
    #     else:
    #         new_position = min_steps_to_chaser(game, (position[0], position[1]), (self.position[0], self.position[1]))
    #         return new_position



class runners:

    def __init__(self, game, input={}):
        self.id = "runners"
        self.colors = {
            "runner": "soft blue",
        }
        self.runners = input.get("runners") or []
    
    def render(self, game):
        for runner in self.runners:
            game.set(runner["position"], "runner")

    def run_away(self, game):

        print(self.runners)

        for runner in self.runners:

            stress = False
            floor_positions = []
            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                new_position = [runner["position"][0] + dx, runner["position"][1] + dy]
                if game.get(new_position) == "chaser":
                    stress = True
                elif game.get(new_position) == "floor":
                    floor_positions.append(new_position)
            
            if stress and len(floor_positions) == 1:
                print("STRESS")
                new_position = floor_positions[0]
            elif stress and not floor_positions:
                continue
            else:
                new_position = safest_next_move(game, (runner["position"][0], runner["position"][1]))

            game.set(runner["position"], "floor")
            game.set(new_position, "runner")
            runner["position"] = new_position

        # for runner in self.runners:
        #     runner_position = runner["position"]
        #     record_distance = game.find_object("chaser").distance_from_runner(game, runner_position)
        #     record_position = runner_position
            
        #     for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        #         new_position = [runner_position[0] + dx, runner_position[1] + dy]

        #         if game.get(new_position) != "floor":
        #             continue

        #         distance = game.find_object("chaser").distance_from_runner(game, new_position)
        #         if distance > record_distance:
        #             record_distance = distance
        #             record_position = new_position
            
        #     game.set(runner_position, "floor")
        #     game.set(record_position, "runner")
        #     runner["position"] = record_position
    
    def eat_runner(self, game, position):
        # remove the runner at the current position
        self.runners = [runner for runner in self.runners if not lists_match(runner["position"], position)]


class walls:
    def __init__(self, game, input={}):
        self.id = "walls"
        self.colors = {
            "wall": "black",
            "box": "brown",
        }
        self.board = input.get("board") or []
    
    def render(self, game):
        for x, y, item in iterate_over_2D(self.board):
            if item == "x":
                game.set([x, y], "wall")
            elif item == "o":
                game.set([x, y], "box")
    
    def push_box(self, game, position, dx, dy):
        new_position = [position[0] + dx, position[1] + dy]
        if game.get(new_position) == "floor":
            game.set(position, "floor")
            game.set(new_position, "box")
            return True
        return False


class chase_game(game_template):
    def __init__(self, game):
        self.game_name = "chase"
        game.size = [64, 64]
        
        game.list_of_objects = {
            "moves_left": moves_left,
            "levels_left": levels_left,
            "border": border,
            "floor": floor,
            "walls": walls,
            "chaser": chaser,
            "runners": runners
        }
    
    def press_button(self, game, button):

        game.find_object("chaser").move(game, button.dx, button.dy)

        game.next_frame()
        
        game.find_object("runners").run_away(game)

        if game.find_object("runners").runners == []:
            game.win = True
        
        if game.is_modified():
            game.find_object("moves_left").use_move(game)
            game.find_object("levels_left").update_level(game)


