from helper import chunk_list_avg_size, iterate_over_2D


class color_pads:
    def __init__(self, game, color_pads):
        self.id = "color_pads"
        self.colors = {
            "pad-yellow": "yellow",
            "pad-cyan": "cyan",
            "pad-soft blue": "soft blue",
        }
        self.color_pads = color_pads
    
    def render(self, game):
        for pad in self.color_pads:
            for position in pad["positions"]:
                color = pad["color"]
                game.set(position, f"pad-{color}")



class moves_left:
    def __init__(self, game):
        self.id = "moves_left"
        self.colors = {
            "unused move": "orange",
            "used move": "dark red"
        }
        game.protected_colors += ["used move", "unused move"]
        self.on_move = 0

    def render(self, game):

        # paint the border
        for i in range(game.actual_size[0]):
            game.set((0,i), "unused move", _resolution=False, _origin=False)
            game.set((game.actual_size[0]-1,i), "unused move", _resolution=False, _origin=False)
            game.set((i,game.actual_size[1]-1), "unused move", _resolution=False, _origin=False)

        # generate the list of positions
        positions_list = []
        for i in range(game.actual_size[0]//2):
            halfway = game.actual_size[0]//2
            top = game.actual_size[1] - 1
            positions_list.append([(halfway-i-1, top), (halfway+i, top)])
        self.positions = positions_list

        for i in range(game.actual_size[1]-1)[::-1]:
            positions_list.append([(0,i), (game.actual_size[0]-1,i)])
        
        # chunk the list
        chunk_size = len(positions_list) / game.max_moves
        self.positions = chunk_list_avg_size(positions_list, chunk_size)

    def use_move(self, game):
        if self.on_move >= len(self.positions):
            return
        
        positions = self.positions[self.on_move]
        for i in positions:
            game.set(i[0], "used move", _resolution=False, _origin=False)
            game.set(i[1], "used move", _resolution=False, _origin=False)

        self.on_move += 1



class patrols:
    def __init__(self, game, _patrols):
        self.id = "patrols"
        self.colors = {
            "patrol body": "orange",
            "patrol eye": "dark red"
        }
        self.patrols = _patrols

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
                print("gonna flippo")
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

                if self.check_collision(game, patrol):
                    print("needs to flip")
                    self.flip(game, patrol)


    def check_collision(self, game, patrol):
        position, dx, dy = patrol["position"], patrol["dx"], patrol["dy"]

        edge_positions = set()
        if dx != 0:
            for i in [-1, 0, 1]:
                edge_positions.add((position[0]+dx+dx, position[1]+i))
        if dy != 0:
            for i in [-1, 0, 1]:
                edge_positions.add((position[0]+i, position[1]+dy+dy))

        for position in edge_positions:
            if game.get(position) not in ["floor"]:
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
    def __init__(self, game, initial_direction='up'):
        self.id = "border"
        self.colors = {
            "corner": "dark gray",
            "active border": "green",
            "inactive border": "light gray"
        }
        self.initial_direction = initial_direction

        self.left = game.board_origin[0] - 1
        self.right = game.board_origin[0] + game.board_size[0]
        self.bottom = game.board_origin[1] - 1
        self.top = game.board_origin[1] + game.board_size[1]

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
        game.set_rect("floor", game.board_origin, game.board_size)


class walls:
    def __init__(self, game, positions):
        self.id = "walls"
        self.colors = {
            "wall": "dark gray",
            "wall-white": "white",
            "wall-cyan": "cyan",
            "wall-pink": "pink",
            "wall-yellow": "yellow",
            "wall-soft blue": "soft blue",
        }
        self.walls = {}
        for i in self.colors:
            self.walls[i] = []

        for x,y,i in iterate_over_2D(positions):
            y += game.board_origin[1]
            x += game.board_origin[0]
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
    def __init__(self, game, player_data):
        self.id = "players"
        self.colors = {
            "player-red": "red",
            "player-yellow": "yellow",
            "player-cyan": "cyan",
            "player-pink": "pink",
            "player-soft blue": "soft blue",
        }
        self.player_data = player_data

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
                if new_position[0] <= game.board_origin[0]: new_position[0] = game.board_origin[0] + game.board_size[0] - 1
                if new_position[1] <= game.board_origin[1]: new_position[1] = game.board_origin[1] + game.board_size[1] - 1
                if new_position[0] >= game.board_origin[0] + game.board_size[0]: new_position[0] = game.board_origin[0] + 1
                if new_position[1] >= game.board_origin[1] + game.board_size[1]: new_position[1] = game.board_origin[1] + 1

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
        for player in self.player_data:

            # did the player reach the end?
            for i in zip(player["position"], player["end"]):
                if i[0] != i[1]:
                    game_win = False
                    break

            # is the player the correct color?
            if "end_color" in player:
                if player["player"] != player["end_color"]:
                    game_win = False
                    break

        if game_win:
            game.win = True



class ever_maze:

    def __init__(self, game):
        game.size = [64, 64]
        game.resolution = [1,1]
        game.origin = (0,0)
        game.max_levels = 9
        game.level = 1
        game.set_background("gray")

    def initialize_objects(self, game):

        if game.level == 1:
            
            game.size = [16,16]
            game.resolution = [4,4]
            game.origin = (8,8)

            game.board_origin = (0,0)
            game.board_size = (12,12)

            game.max_moves = 15
            self.previous_button = "up"

            game.add_objects([
                moves_left(game),
                border(game, initial_direction=self.previous_button),
                floor(game),
                patrols(game, []),
                players(game, [
                    {
                        "player": "red",
                        "position": (8,9),
                        "end": (4,3)
                    }
                ]),
                color_pads(game, []),
                walls(game, [
                    "......xx..x.",
                    ".x.....xxx..",
                    "..xx..xx.x..",
                    "..xxx.......",
                    ".xxxxx......",
                    "..xx.....x..",
                    ".......xxx..",
                    ".......xxx..",
                    "...o.o..x.x.",
                    "...ooo......",
                    "............",
                    "............",
                ])
            ])
        elif game.level == 2:
            
            game.size = [16,16]
            game.resolution = [4,4]
            game.origin = (8,8)

            game.board_origin = (0,0)
            game.board_size = (12,12)

            game.max_moves = 12
            self.previous_button = "left"

            game.add_objects([
                moves_left(game),
                border(game, initial_direction=self.previous_button),
                floor(game),
                patrols(game, []),
                color_pads(game, []),
                players(game, [
                    {
                        "player": "yellow",
                        "position": (9,6),
                        "end": (2,3)
                    }
                ]),
                walls(game, [
                    "............",
                    "..x.........",
                    ".x..........",
                    ".......x....",
                    "......xxx...",
                    "......xxx...",
                    "......xx....",
                    ".oo.........",
                    ".o....xx....",
                    ".oo..xxx..x.",
                    ".........x..",
                    "............",
                ])
            ])
        elif game.level == 3:
            
            game.size = [16,16]
            game.resolution = [4,4]
            game.origin = (8,8)

            game.board_origin = (0,0)
            game.board_size = (12,12)
            
            game.max_moves = 18
            self.previous_button = "up"

            game.add_objects([
                moves_left(game),
                border(game, initial_direction=self.previous_button),
                floor(game),
                patrols(game, [
                    {
                        "position": (3,10),
                        "dx": 1,
                        "dy": 0
                    }
                ]),
                players(game, [
                    {
                        "player": "yellow",
                        "position": (4,7),
                        "end": (5,1)
                    }
                ]),
                color_pads(game, []),
                walls(game, [
                    "........x...",
                    "x...........",
                    "............",
                    "...xx.xx....",
                    "...x...x....",
                    "...x......x.",
                    "......xx..x.",
                    ".xx.........",
                    ".x..x.......",
                    "....ooo..xx.",
                    "....o.o.....",
                    "............",
                ])
            ])
        elif game.level == 4:
            
            game.size = [16,16]
            game.resolution = [4,4]
            game.origin = (4,8)

            game.board_origin = (0,0)
            game.board_size = (14,12)

            game.max_moves = 18
            self.previous_button = "down"

            game.add_objects([
                moves_left(game),
                border(game, initial_direction=self.previous_button),
                floor(game),
                patrols(game, []),
                players(game, [
                    {
                        "player": "cyan",
                        "position": (7,3),
                        "end": (2,4)
                    },
                    {
                        "player": "pink",
                        "position": (4,7),
                        "end": (4,1)
                    }
                ]),
                color_pads(game, []),
                walls(game, [
                    "..............",
                    "...x....xx....",
                    "..xx.....xx...",
                    "..............",
                    "..xx.....x....",
                    "..xxx...xx.x..",
                    ".oo.......xxx.",
                    ".c.........x..",
                    ".oo...x....x..",
                    "...opoxx..xxx.",
                    "...o.o.....x..",
                    ".............."
                ])
            ])
        elif game.level == 5:

            #game.size = [22, 22]
            game.resolution = [3,3]
            game.origin = (5,5)

            game.board_origin = (0,0)
            game.board_size = (18,18)

            game.max_moves = 20
            self.previous_button = "left"

            game.add_objects([
                moves_left(game),
                border(game, initial_direction=self.previous_button),
                floor(game),
                patrols(game, [
                    {
                        "position": (1,14),
                        "dy": -1
                    },
                    { "position": (6,10) },
                    { "position": (6,4) },
                    { "position": (12,2) },
                ]),
                players(game, [
                    {
                        "player": "cyan",
                        "position": (7,8),
                        "end": (3,13),
                        "end_color": "yellow"
                    }
                ]),
                color_pads(game, [
                    {
                        "color": "yellow",
                        "positions": [(10,12), (10,13), (10,14)]
                    }
                ]),
                walls(game, [
                    "..................",
                    "...xxxxx....xxx...",
                    "...ooxx.....xxx...",
                    "....yxx...........",
                    "...ooxxx..........",
                    "..................",
                    "...............x..",
                    "....x.....x.....x.",
                    "...xxxx.........x.",
                    "..xxxxx........xx.",
                    "..xxxxx....xx..x..",
                    "....x.......x..x..",
                    "..................",
                    "..................",
                    "..................",
                    "..................",
                    ".................."
                ])
            ])
        elif game.level == 6:

            game.resolution = [3,3]
            game.origin = (12,10)

            game.board_origin = (0,0)
            game.board_size = (13,15)

            game.max_moves = 16
            self.previous_button = "right"

            game.add_objects([
                moves_left(game),
                border(game, initial_direction=self.previous_button),
                floor(game),
                patrols(game, [
                    {
                        "position": (1,2),
                        "dx": 1,
                    }
                ]),
                players(game, [
                    {
                        "player": "pink",
                        "position": (8,5),
                        "end": (3,4),
                        "end_color": "soft blue"
                    }
                ]),
                color_pads(game, [
                    {
                        "color": "soft blue",
                        "positions": [(8,13), (9,13), (10,13)]
                    }
                ]),
                walls(game, [
                    ".............",
                    ".............",
                    ".............",
                    ".xx.......x..",
                    ".xxx.x..xxxx.",
                    "........xxx..",
                    ".........x...",
                    ".............",
                    ".............",
                    "..obo.x..x...",
                    "..o.o.xxxxx..",
                    ".......xxxxx.",
                    ".......xxxxx.",
                    "..........x..",
                    "............."
                ]),
            ])

        elif game.level == 7:

            game.resolution = [4,4]
            game.origin = (6,12)

            game.board_origin = (0,0)
            game.board_size = (13,10)

            game.max_moves = 160
            self.previous_button = "right"

            game.add_objects([
                moves_left(game),
                border(game, initial_direction=self.previous_button),
                floor(game),
                patrols(game, []),
                players(game, [
                    {
                        "player": "pink",
                        "position": (1,6),
                        "end": (1,11),
                        "end_color": "soft blue"
                    }
                ]),
                color_pads(game, [
                    {
                        "color": "soft blue",
                        "positions": [(6,5), (6,6), (6,7)]
                    }
                ]),
                walls(game, [
                    ".............",
                    ".........x...",
                    "..xx....xxxx.",
                    "..xx.....x...",
                    ".xxxx....x...",
                    "..xx.........",
                    ".............",
                    ".........obo.",
                    ".........o.o.",
                    ".............",
                ]),
            ])



    def begin(self, game):
        self.initialize_objects(game)

    def press_tile(self, game, x, y):
        pass

    def press_button(self, game, button):

        if self.previous_button == button.name:
            return
        
        if button.name not in ["up", "down", "left", "right"]:
            return
        
        self.previous_button = button.name

        for patrol in game.find_all("patrols"):
            patrol.move(game)
        
        game.find_object("border").direction(game, button.name)
        game.find_object("players").move(game, button.dx, button.dy)

        if game.is_modified():
            game.find_object("moves_left").use_move(game)


def choose_game(game_name, game):
    return ever_maze(game)



# class fruits:
#     def __init__(self, positions):
#         self.id = "fruits"
#         self.colors = {
#             "active fruit": "red",
#             "inactive fruit": "black"
#         }
#         self.active_fruit = positions[0]
#         self.inactive_fruit = positions[1:]

#     def render(self, game):
#         game.set(self.active_fruit, "active fruit")
#         for fruit in self.inactive_fruit:
#             game.set(fruit, "inactive fruit")

#     def collect(self, game):
#         self.active_fruit = None
#         if len(self.inactive_fruit):
#             self.active_fruit = self.inactive_fruit.pop(0)
#             game.set(self.active_fruit, "active fruit")

#     def no_more_fruits(self):
#         return self.active_fruit == None and self.inactive_fruit == []


# class snake:
#     def __init__(self, positions):
#         self.id = "snake"
#         self.colors = {
#             "head": "green",
#             "body": "dark green"
#         }
#         self.head = positions[-1]
#         self.body = positions

#     def render(self, game):
#         for body in self.body:
#             game.set(body, "body")
        
#         game.set(self.head, "head")

#     def move(self, game, dx, dy):
        
#         new_head = (self.head[0] + dx, self.head[1] + dy)

#         next_spot = game.get(new_head)
        
#         if next_spot not in ["empty", "active fruit"]:
#             return
        
#         self.body.append(new_head)
#         self.head = new_head

#         game.set(self.body[-2], "body")
#         game.set(self.head, "head")

#         if next_spot == "active fruit":
#             game.find_object("fruits").collect(game)

#         if new_head == (5,5):
#             game.lose = True

# def choose_game(game_name, game):
#     return snake(game)



# class snake_game:
#     def __init__(self, game):

#         game.size = [6,6]
#         game.resolution = 6
#         game.max_attempts = 2
#         game.max_levels = 2
#         game.max_moves = 27
#         game.set_background("gray")

#     def initialize_objects(self, game):
#         print('initialize_objects')
#         if game.level == 1:
#             snek = snake([(0,0)])
#             fruts = fruits([(4,1), (2,3), (1,0), (4,3)])
#         else:
#             snek = snake([(1,1)])
#             fruts = fruits([(4,1), (2,3), (1,0), (4,3)])

#         game.add_objects([snek, fruts])

#     def begin(self, game):
#         print('begin')
#         self.initialize_objects(game)

#     def press_button(self, game, button):

#         print(game.level, game.move, game.attempt)

#         for i in range(2):

#             game.find_object("snake").move(game, button.dx, button.dy)

#             if game.find_object("fruits").no_more_fruits():
#                 game.win = True
            
#             game.next_frame()

#     def press_tile(self, game, x, y):
#         print(x, y)
#         pass


# def choose_game(game_name, game):
#     return snake_game(game)




# class snake_game:

#     def __init__(self, game):
#         game.size = [6,6]
#         game.resolution = 6
#         game.max_attempts = 2
#         game.max_levels = 2
#         game.max_moves = 27
#         game.set_background("gray")

#         game.add_colors({
#             "head": "green",
#             "body": "dark green",
#             "fruit": "red",
#             "inactive fruit": "black"
#         })
        
#     def initialize_objects(self, game):
#         pass

#     def begin(self, game):

#         game.body = [(0,0)]
#         game.fruit = [(4,1), (2,3), (1,0), (4,3)]
#         game.current_fruit = game.fruit.pop(0)
#         game.set([0,0], "head")
#         for fruit in game.fruit:
#             game.set(fruit, "inactive fruit")
#         game.set(game.current_fruit, "fruit")


#     def press_button(self, game, button):

#         def snek():
#             head = game.body[-1]

#             head = (head[0] + button.dx, head[1] + button.dy)

#             if game.get(head) not in ["empty", "fruit"]:
#                 return

#             if game.get(head) == "fruit":
#                 if game.fruit:
#                     game.current_fruit = game.fruit.pop(0)
#                     game.set(game.current_fruit, "fruit")
#                 else:
#                     game.win = True

#             game.body.append(head)

#             game.set(head, "head")
#             game.set(game.body[-2], "body")

#             if head == (5,5):
#                 game.lose = True
        
#         snek()
#         game.next_frame()
#         snek()

#     def press_tile(self, game, x, y):
#         pass

# def choose_game(game_name, game):
#     return snake_game(game)

