

def initialize(game):
    game.size = [6,6]
    game.resolution = 6
    game.max_attempts = 2
    game.max_levels = 2
    game.max_moves = 27
    game.colors = ["gray", "dark green", "green", "black", "red", "green", "red"]

def begin(game):

    print("Attempt:", game.attempt, "Level:", game.level)

    #if game.level == 1:
    game.body = [(0,0)]
    game.fruit = [(4,1), (2,3), (1,0), (4,3)]
    game.current_fruit = game.fruit.pop(0)
    game.set([0,0], 2)
    for fruit in game.fruit:
        game.set(fruit, 3)
    game.set(game.current_fruit, 4)


def press_button(game, button):


    head = game.body[-1]

    head = (head[0] + button.dx, head[1] + button.dy)

    if game.get(head) not in [0, 4]:
        return

    if game.get(head) == 4:
        if game.fruit:
            game.current_fruit = game.fruit.pop(0)
            game.set(game.current_fruit, 4)
        else:
            game.win = True

    game.body.append(head)

    game.set(head, 2)
    game.set(game.body[-2], 1)
    
    #snek()
    #game.next_frame()
    #snek()

    if head == (5,5):
       game.lose = True



def press_tile(game, x, y):
    pass


