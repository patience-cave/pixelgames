from state import State

def add_object(self, object):
    self.add_colors(object.colors)
    self.current_state.objects.append(object)


def get_object(self, name, first_only=True):
    o = []
    for object in self.current_state.objects:
        if name in object.colors:
            if first_only:
                return object
            o.append(object)
    return o




# class fruits:
#     def __init__(self, positions):
#         self.colors = {
#             "active fruit": "red",
#             "inactive fruit": "black"
#         }
#         self.active_fruit = positions[0]
#         self.inactive_fruit = positions[1:]

#     def begin(self, game):
#         game.set(self.active_fruit, "active fruit")
#         for fruit in self.inactive_fruit:
#             game.set(fruit, "inactive fruit")

#     def collect(self, game):
#         if len(self.inactive_fruit):
#             self.active_fruit = self.inactive_fruit.pop(0)
#             game.set(self.active_fruit, "active fruit")

#     def any_fruit_left(self):
#         return self.inactive_fruit != []




# class snake:
#     def __init__(self, positions):
#         self.colors = {
#             "head": "light green",
#             "body": "green"
#         }
#         self.head = positions[-1]
#         self.body = positions

#     def begin(self, game):
#         for body in self.body:
#             game.set(body, "body")
        
#         game.set(self.head, "head")

#     def press_button(self, game, button):
#         new_head = (self.head[0] + button.dx, self.head[1] + button.dy)

#         next_spot = game.get(new_head)
        
#         if next_spot not in ["floor", "active fruit"]:
#             return
        
#         self.set(self.body[-2], "body")
#         self.set(self.head, "head")

#         if next_spot == "active fruit":
#             self.get_object("active fruit").collect(game)



