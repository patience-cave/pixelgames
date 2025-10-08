from helper import iterate_over_2D, lists_match
from useful_objects import moves_left, levels_left
from game_template import game_template

class color_pads:
    def __init__(self, game, input={}):
        self.id = "color_pads"
        self.colors = {
            "pad-yellow": "yellow",
            "pad-cyan": "cyan",
            "pad-soft blue": "soft blue",
        }
        self.color_pads = input.get("color_pads") or []
    
    def render(self, game):
        for pad in self.color_pads:
            for position in pad["positions"]:
                color = pad["color"]
                game.set(position, f"pad-{color}")

class patrols:
    def __init__(self, game, input={}):
        self.id = "patrols"
        self.colors = {
            "patrol body": "orange",
            "patrol eye": "dark red"
        }
        self.patrols = input.get("patrols") or []

    def render(self, game):

        for patrol in self.patrols:
            position = patrol["position"]
            if "dx" not in patrol: patrol["dx"] = 0
            if "dy" not in patrol: patrol["dy"] = 0
            dx = patrol["dx"]
            dy = patrol["dy"]
            for i in [(0,0), (0,-1), (0,1), (1,-1), (-1,1), (-1,0), (-1,-1), (1,0), (1,1)]:
                game.set((position[0]+i[0], position[1]+i[1]), "patrol body")
            
            game.set([position[0]+dx, position[1]+dy], "patrol eye")
    
    def move(self, game):
        for patrol in self.patrols:
            position = patrol["position"]
            dx = patrol["dx"]
            dy = patrol["dy"]
            
            if dx == 0 and dy == 0:
                continue

            if self.check_collision(game, patrol):
                self.flip(game, patrol)
            else:

                if dx != 0:
                    for i in [-1, 0, 1]:
                        game.set((position[0]-dx, position[1]+i), "floor")
                if dy != 0:
                    for i in [-1, 0, 1]:
                        game.set((position[0]+i, position[1]-dy), "floor")

                patrol["position"] = (position[0]+dx, position[1]+dy)
                self.render(game)

                if self.check_collision(game, patrol, safe=True):
                    self.flip(game, patrol)


    def check_collision(self, game, patrol, safe=False):
        position, dx, dy = patrol["position"], patrol["dx"], patrol["dy"]

        edge_positions = set()
        if dx != 0:
            for i in [-1, 0, 1]:
                edge_positions.add((position[0]+dx+dx, position[1]+i+dy))
        if dy != 0:
            for i in [-1, 0, 1]:
                edge_positions.add((position[0]+i+dx, position[1]+dy+dy))
        if dx != 0 and dy != 0:
            edge_positions.add((position[0]+dx+dx, position[1]+dy+dy))

        for position in edge_positions:

            if "invisible wall" in patrol:
                for invisible_wall in patrol["invisible wall"]:
                    if lists_match(position, invisible_wall):
                        return True
            
            if game.get(position) not in ["floor"]:
                if game.get(position).startswith("player"):
                    if not safe:
                        game.lose = True
                else:
                    return True
        return False
    
    def flip(self, game, patrol):
        position, dx, dy = patrol["position"], patrol["dx"], patrol["dy"]
        game.set([position[0]+dx, position[1]+dy], "patrol body")
        dx, dy = -dx, -dy
        patrol["dx"] = dx
        patrol["dy"] = dy
        game.set([position[0]+dx, position[1]+dy], "patrol eye")



class border:
    def __init__(self, game, input={}):
        self.id = "border"
        self.colors = {
            "corner": "dark gray",
            "active border": "green",
            "inactive border": "light gray"
        }
        self.initial_direction = input.get("initial_direction") or "up"

        self.left = -1
        self.right = game.board_size[0]
        self.bottom = -1
        self.top = game.board_size[1]

    def render(self, game):
        game.set((self.left, self.bottom), "corner")
        game.set((self.left, self.top), "corner")
        game.set((self.right, self.bottom), "corner")
        game.set((self.right, self.top), "corner")

        dir = self.initial_direction
        self.direction(game, "")
        self.direction(game, dir)

    def direction(self, game, dir):
        
        if dir == self.initial_direction:
            return
        
        self.initial_direction = dir

        for i in range(self.left+1,self.right):
            game.set((i,self.bottom), "inactive border")
            game.set((i,self.top), "inactive border")

            if dir == "up":
                game.set((i,self.top), "active border")
            elif dir == "down":
                game.set((i,self.bottom), "active border")

        for i in range(self.bottom+1,self.top):
            game.set((self.left,i), "inactive border")
            game.set((self.right,i), "inactive border")

            if dir == "right":
                game.set((self.right,i), "active border")
            elif dir == "left":
                game.set((self.left,i), "active border")

            


class floor:
    def __init__(self, game):
        self.id = "floor"
        self.colors = {
            "floor": "purple"
        }

    def render(self, game):
        game.set_rect("floor", (0,0), game.board_size)

    
class walls:
    def __init__(self, game, input={}):
        self.id = "walls"
        self.colors = {
            "wall": "dark gray",
            "wall-white": "white",
            "wall-cyan": "cyan",
            "wall-pink": "pink",
            "wall-yellow": "yellow",
            "wall-soft blue": "soft blue",
        }
        positions = input.get("positions") or []
        
        self.walls = {}
        for i in self.colors:
            self.walls[i] = []

        for x,y,i in iterate_over_2D(positions):
            if i == "x": self.walls["wall"].append((x, y))
            if i == "o": self.walls["wall-white"].append((x, y))
            if i == "c": self.walls["wall-cyan"].append((x, y))
            if i == "p": self.walls["wall-pink"].append((x, y))
            if i == "y": self.walls["wall-yellow"].append((x, y))
            if i == "b": self.walls["wall-soft blue"].append((x, y))

    def render(self, game):

        for i in self.walls:
            for position in self.walls[i]:
                game.set(position, i)



class players:
    def __init__(self, game, input={}):
        self.id = "players"
        self.colors = {
            "player-red": "red",
            "player-yellow": "yellow",
            "player-cyan": "cyan",
            "player-pink": "pink",
            "player-soft blue": "soft blue",
        }
        self.player_data = input.get("player_data") or []
        self.end_data = input.get("end_data") or []

    def render(self, game):
        for i in self.player_data:
            pos = i["position"]
            id = i["player"]
            game.set(pos, f"player-{id}")

    def move(self, game, dx, dy):

        original_positions = { i["player"]: i["position"] for i in self.player_data }
        looped_players = []

        while True:

            still_moving = False

            # Sort the players by their position and their direction to move
            if dx == 1:
                sorted_players = sorted(self.player_data, key=lambda x: x["position"][0])
            elif dx == -1:
                sorted_players = sorted(self.player_data, key=lambda x: x["position"][0], reverse=True)
            elif dy == 1:
                sorted_players = sorted(self.player_data, key=lambda x: x["position"][1])
            elif dy == -1:
                sorted_players = sorted(self.player_data, key=lambda x: x["position"][1], reverse=True)

            for player in sorted_players:

                if "tile_covered" not in player:
                    player["tile_covered"] = "floor"
                previously_covered = player["tile_covered"]

                id = player["player"]

                previous_position = player["position"]
                new_position = [previous_position[0] + dx, previous_position[1] + dy]

                # Looped Grid Logic
                if new_position[0] < 0: new_position[0] = game.board_size[0] - 1
                if new_position[1] < 0: new_position[1] = game.board_size[1] - 1
                if new_position[0] >= game.board_size[0]: new_position[0] = 0
                if new_position[1] >= game.board_size[1]: new_position[1] = 0

                # If the player loops and returns to their prior position, end their motion
                if id in looped_players:
                    continue
                if new_position == original_positions[id]:
                    looped_players.append(id)
                
                # If the player hits any of these, end their motion
                if game.get(new_position).startswith("wall"):
                    continue
                if game.get(new_position).startswith("patrol"):
                    game.lose = True
                    continue
                if game.get(new_position).startswith("player"):
                    continue
                
                if game.get(new_position).startswith("pad"):
                    old_color = player["player"]
                    player["tile_covered"] = game.get(new_position)
                    player["player"] = game.get(new_position).split("-")[1]
                    id = player["player"]
                    
                    if id != old_color:
                        original_positions[id] = original_positions[old_color]
                        del original_positions[old_color]


                if game.get(new_position).startswith("floor"):
                    player["tile_covered"] = "floor"

                game.set(previous_position, previously_covered)
                for i in self.player_data:
                    if i["player"] == id:
                        i["position"] = new_position
                game.set(new_position, f"player-{id}")
                still_moving = True

            if not still_moving:
                break
            else:
                game.next_frame()
    
        # check if all players have reached the end
        game_win = True

        for end in self.end_data:

            if "end_color" in end:
                end_color = end["end_color"]
                if not game.get(end["end"]).startswith(f"player-{end_color}"):
                    game_win = False
                    break
            else:
                if not game.get(end["end"]).startswith("player"):
                    game_win = False
                    break

        if game_win:
            game.win = True



class as66_game(game_template):

    def __init__(self, game):
        self.game_name = "as66"
        game.size = [64, 64]

        game.list_of_objects = {
                "moves_left": moves_left,
                "levels_left": levels_left,
                "border": border,
                "floor": floor,
                "patrols": patrols,
                "players": players,
                "color_pads": color_pads,
                "walls": walls
            }

    def press_button(self, game, button):

        if button.previous_button == button.name and game.move != 0:
            return
        
        if button.name not in ["up", "down", "left", "right"]:
            return

        for patrol in game.find_all("patrols"):
            patrol.move(game)
        
        game.find_object("border").direction(game, button.name)
        game.find_object("players").move(game, button.dx, button.dy)

        if game.is_modified():
            game.find_object("moves_left").use_move(game)
            game.find_object("levels_left").update_level(game)
