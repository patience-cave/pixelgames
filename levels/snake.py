from game_template import game_template
from useful_objects import levels_left, moves_left

class border:
    def __init__(self, game, input={}):
        self.id = "border"
        self.colors = {
            "border": "black",
            "floor": "light gray"
        }
    
    def render(self, game):
        for i in range(-1, game.board_size[0]+1):
            game.set((i, -1), "border")
            game.set((i, game.board_size[1]), "border")
        for i in range(-1, game.board_size[1]+1):
            game.set((-1, i), "border")
            game.set((game.board_size[0], i), "border")

class floor:
    def __init__(self, game, input={}):
        self.id = "floor"
        self.colors = {
            "floor": "light gray"
        }

    def render(self, game):
        for i in range(0, game.board_size[0]):
            for j in range(0, game.board_size[1]):
                game.set((i, j), "floor")

class fruits:
    def __init__(self, game, input={}):
        self.id = "fruits"
        self.colors = {
            "active fruit": "red",
            "inactive fruit": "black"
        }
        positions = input["positions"]
        self.active_fruit = positions[0]
        self.inactive_fruit = positions[1:]

    def render(self, game):
        game.set(self.active_fruit, "active fruit")
        for fruit in self.inactive_fruit:
            game.set(fruit, "inactive fruit")

    def collect(self, game):
        self.active_fruit = None
        if len(self.inactive_fruit):
            self.active_fruit = self.inactive_fruit.pop(0)
            game.set(self.active_fruit, "active fruit")

    def no_more_fruits(self):
        return self.active_fruit == None and self.inactive_fruit == []



class snake:
    def __init__(self, game, input={}):
        self.id = "snake"
        self.colors = {
            "head": "green",
            "body": "dark green"
        }
        positions = input["positions"]
        self.head = positions[-1]
        self.body = positions

    def render(self, game):
        for body in self.body:
            game.set(body, "body")
        
        game.set(self.head, "head")

    def move(self, game, dx, dy):
        
        new_head = (self.head[0] + dx, self.head[1] + dy)

        if new_head[0] < 0 or new_head[0] >= game.board_size[0] or new_head[1] < 0 or new_head[1] >= game.board_size[1]:
            return

        next_spot = game.get(new_head)
        
        if next_spot not in ["floor", "active fruit"]:
            return
        
        self.body.append(new_head)
        self.head = new_head

        game.set(self.body[-2], "body")
        game.set(self.head, "head")

        if next_spot == "active fruit":
            game.find_object("fruits").collect(game)

        # if new_head == (5,5):
            # game.lose = True




class snake_game(game_template):
    def __init__(self, game):
        self.game_name = "snake"
        game.size = [64, 64]
        
        game.list_of_objects = {
            "moves_left": moves_left,
            "levels_left": levels_left,
            "border": border,
            "floor": floor,
            "snake": snake,
            "fruits": fruits
        }

    def press_button(self, game, button):
        
        game.find_object("snake").move(game, button.dx, button.dy)

        if game.find_object("fruits").no_more_fruits():
            game.win = True

        if game.is_modified():
            game.find_object("moves_left").use_move(game)
            game.find_object("levels_left").update_level(game)




