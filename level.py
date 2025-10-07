

def initialize(game):
    game.size = [6,6]
    game.resolution = 6
    game.max_attempts = 2
    game.max_levels = 2
    game.max_moves = 27

    game.set_background("gray")

    game.add_colors({
        # "floor": "gray",
        "body": "dark green",
        "head": "green",
        "fruit": "red",
        "inactive fruit": "black",
    })



def begin(game):

    print("Attempt:", game.attempt, "Level:", game.level)

    #if game.level == 1:
    game.body = [(0,0)]
    game.fruit = [(4,1), (2,3), (1,0), (4,3)]
    game.current_fruit = game.fruit.pop(0)
    game.set([0,0], "head")
    for fruit in game.fruit:
        game.set(fruit, "inactive fruit")
    game.set(game.current_fruit, "fruit")


def press_button(game, button):

    print(game.move)

    head = game.body[-1]

    head = (head[0] + button.dx, head[1] + button.dy)

    if game.get(head) not in ["empty", "fruit"]:
        return

    if game.get(head) == "fruit":
        if game.fruit:
            game.current_fruit = game.fruit.pop(0)
            game.set(game.current_fruit, "fruit")
        else:
            game.win = True

    game.body.append(head)

    game.set(head, "head")
    game.set(game.body[-2], "body")
    
    #snek()
    #game.next_frame()
    #snek()

    if head == (5,5):
       game.lose = True



def press_tile(game, x, y):
    pass


