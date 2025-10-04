

def initialize(grid):
    grid.size = [6,6]
    grid.colors = ["gray", "dark green", "green", "black", "red"]
    # grid.maximum_moves = 10
    # grid.level = 10

def begin(grid, state):
    state.body = [(0,0)]
    state.fruit = [(4,1), (2,3), (1,0), (4,3)]
    state.current_fruit = state.fruit.pop(0)
    grid.set([0,0], 2)
    for fruit in state.fruit:
        grid.set(fruit, 3)
    grid.set(state.current_fruit, 4)

def press_button(grid, state, button):

    head = state.body[-1]

    head = (head[0] + button.dx, head[1] + button.dy)

    if grid.get(head) not in [0, 4]:
        return

    if grid.get(head) == 4:
        if state.fruit:
            state.current_fruit = state.fruit.pop(0)
            grid.set(state.current_fruit, 4)

    state.body.append(head)
    print(head)

    grid.set(head, 2)
    grid.set(state.body[-2], 1)



def press_tile(grid, state, x, y):
    pass


