from helper import chunk_list_avg_size

class moves_left:
    def __init__(self, game):
        self.id = "moves_left"
        self.colors = {
            "unused move": "orange",
            "used move": "dark red"
        }
        self.on_move = 0

    def render(self, game):
        for i in range(game.actual_size[0]):
            game.set((0,i), "unused move", resolution=False)
            game.set((game.actual_size[0]-1,i), "unused move", resolution=False)
            game.set((i,game.actual_size[1]-1), "unused move", resolution=False)

        positions_list = []
        for i in range(game.actual_size[0]//2):
            halfway = game.actual_size[0]//2
            top = game.actual_size[1] - 1
            positions_list.append([(halfway-i-1, top), (halfway+i, top)])
        self.positions = positions_list

        for i in range(game.actual_size[1]-1)[::-1]:
            positions_list.append([(0,i), (game.actual_size[0]-1,i)])
        
        chunk_size = len(positions_list) / game.max_moves
        self.positions = chunk_list_avg_size(positions_list, chunk_size)

    def use_move(self, game):
        if self.on_move >= len(self.positions):
            return
        positions = self.positions[self.on_move]
        for i in positions:
            game.set(i[0], "used move", resolution=False)
            game.set(i[1], "used move", resolution=False)

        self.on_move += 1

class patrol:
    def __init__(self, game, position, dx, dy):
        self.id = "patrol"
        self.colors = {
            "patrol body": "orange",
            "patrol eye": "dark red"
        }
        self.position = position
        self.dx = dx
        self.dy = dy

    def render(self, game):
        for i in [(0,0), (0,-1), (0,1), (1,-1), (-1,1), (-1,0), (-1,-1), (1,0), (1,1)]:
            game.set((self.position[0]+i[0], self.position[1]+i[1]), "patrol body")
        
        game.set([self.position[0]+self.dx, self.position[1]+self.dy], "patrol eye")
    
    def move(self, game):
        if self.check_collision(game):
            self.flip(game)
        else:

            if self.dx != 0:
                for i in [-1, 0, 1]:
                    game.set((self.position[0]-self.dx, self.position[1]+i), "floor")
            if self.dy != 0:
                for i in [-1, 0, 1]:
                    game.set((self.position[0]+i, self.position[1]-self.dy), "floor")

            self.position = (self.position[0]+self.dx, self.position[1]+self.dy)
            self.render(game)

            if self.check_collision(game):
                self.flip(game)

    def check_collision(self, game):

        edge_positions = set()
        if self.dx != 0:
            for i in [-1, 0, 1]:
                edge_positions.add((self.position[0]+self.dx+self.dx, self.position[1]+i))
        if self.dy != 0:
            for i in [-1, 0, 1]:
                edge_positions.add((self.position[0]+i, self.position[1]+self.dy+self.dy))

        print(edge_positions)
        for position in edge_positions:
            print(position, game.get(position))
            if game.get(position) not in ["floor"]:
                return True
        return False
    
    def flip(self, game):
        game.set([self.position[0]+self.dx, self.position[1]+self.dy], "patrol body")
        self.dx = -self.dx
        self.dy = -self.dy
        game.set([self.position[0]+self.dx, self.position[1]+self.dy], "patrol eye")



class border:
    def __init__(self, game, initial_direction='up'):
        self.id = "border"
        self.colors = {
            "corner": "dark gray",
            "active border": "green",
            "inactive border": "light gray"
        }
        self.initial_direction = initial_direction

    def render(self, game):
        game.set((1,1), "corner")
        game.set((1,14), "corner")
        game.set((14,1), "corner")
        game.set((14,14), "corner")

        dir = self.initial_direction
        self.direction(game, "")
        self.direction(game, dir)

    def direction(self, game, dir):
        
        if dir == self.initial_direction:
            return
        
        self.initial_direction = dir

        for i in range(2,14):
            game.set((i,1), "inactive border")
            game.set((i,14), "inactive border")
            game.set((1,i), "inactive border")
            game.set((14,i), "inactive border")

            if dir == "right":
                game.set((14,i), "active border")
            elif dir == "left":
                game.set((1,i), "active border")
            elif dir == "up":
                game.set((i,14), "active border")
            elif dir == "down":
                game.set((i,1), "active border")


class floor:
    def __init__(self, game):
        self.id = "floor"
        self.colors = {
            "floor": "purple"
        }

    def render(self, game):
        for i in range(2,14):
            for j in range(2,14):
                game.set((i,j), "floor")


class walls:
    def __init__(self, game, positions):
        self.id = "walls"
        self.colors = {
            "wall": "dark gray",
            "white wall": "white"
        }
        self.walls = []
        self.white_walls = []
        y = 13
        for i in positions:
            x = 2
            for j in i:
                if j == "x":
                    self.walls.append((x, y))
                if j == "o":
                    self.white_walls.append((x, y))
                x += 1
            y -= 1

    def render(self, game):
        for position in self.walls:
            game.set(position, "wall")

        for position in self.white_walls:
            game.set(position, "white wall")


class players:
    def __init__(self, game, player_data):
        self.id = "players"
        self.colors = {
            "player-1": "red",
            "player-2": "yellow"
        }
        self.player_data = player_data

    def render(self, game):
        for i in self.player_data:
            pos = i["position"]
            id = i["player"]
            game.set(pos, f"player-{id}")

    def move(self, game, dx, dy):

        original_positions = { i["player"]: i["position"] for i in self.player_data }

        while True:

            still_moving = False

            if dx == 1:
                sorted_players = sorted(self.player_data, key=lambda x: x["position"][0])
            elif dx == -1:
                sorted_players = sorted(self.player_data, key=lambda x: x["position"][0], reverse=True)
            elif dy == 1:
                sorted_players = sorted(self.player_data, key=lambda x: x["position"][1])
            elif dy == -1:
                sorted_players = sorted(self.player_data, key=lambda x: x["position"][1], reverse=True)

            for player in sorted_players:

                id = player["player"]

                previous_position = player["position"]
                new_position = [previous_position[0] + dx, previous_position[1] + dy]

                if new_position[0] == 1: new_position[0] = 13
                if new_position[0] == 14: new_position[0] = 2
                if new_position[1] == 1: new_position[1] = 13
                if new_position[1] == 14: new_position[1] = 2

                if new_position == original_positions[id]:
                    continue
                if game.get(new_position) in ["wall", "white wall"]:
                    continue
                if game.get(new_position).startswith("patrol"):
                    game.lose = True
                    continue
                if game.get(new_position).startswith("player-"):
                    continue

                game.set(previous_position, "floor")
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
            for i in zip(player["position"], player["end"]):
                if i[0] != i[1]:
                    game_win = False
                    break

        if game_win:
            game.win = True



class ever_maze:

    def __init__(self, game):
        game.size = [16,16]
        game.resolution = 4
        game.max_levels = 9
        game.set_background("gray")

    def initialize_objects(self, game):

        if game.level == 3:
            game.max_moves = 15
            self.previous_button = "up"
            game.add_objects([
                moves_left(game),
                border(game, initial_direction=self.previous_button),
                floor(game),
                players(game, [
                    {
                        "player": 1,
                        "position": (10,11),
                        "end": (6,5)
                    }
                ]),
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
            game.max_moves = 12
            self.previous_button = "left"
            game.add_objects([
                moves_left(game),
                border(game, initial_direction=self.previous_button),
                floor(game),
                players(game, [
                    {
                        "player": 2,
                        "position": (11,8),
                        "end": (4,5)
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
        elif game.level == 1:
            game.max_moves = 18
            self.previous_button = "up"
            game.add_objects([
                moves_left(game),
                border(game, initial_direction=self.previous_button),
                floor(game),
                patrol(game, (5,12), 1, 0),
                players(game, [
                    {
                        "player": 2,
                        "position": (6,9),
                        "end": (7,3)
                    }
                ]),
                walls(game, [
                    "........x...",
                    "............",
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

    def begin(self, game):
        self.initialize_objects(game)

    def press_tile(self, game, x, y):
        pass

    def press_button(self, game, button):
        
        if button.name == self.previous_button:
            return
        
        if button.name not in ["up", "down", "left", "right"]:
            return
        
        self.previous_button = button.name

        for patrol in game.find_all("patrol"):
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

