
try:
    from levels.as66 import as66_game
except:
    from as66 import as66_game


def choose_game(game_name, game):
    return as66_game(game)


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

