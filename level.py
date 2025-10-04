

# the beginning state

def initialize():
    return {
        "size": [6, 6],
        "colors": ["gray", "dark green", "green", "black", "red"]
    }

def begin(state, paint):
    state['body'] = [(0,0)]
    state['fruit'] = [(4,1), (2,3), (1,0), (4,3)]
    state['current_fruit'] = state['fruit'].pop(0)
    paint([0,0], 2)
    for fruit in state['fruit']:
        paint(fruit, 3)
    paint(state['current_fruit'], 4)

def press_button(button, state, paint, get):

    head = state['body'][-1]

    if button == 'up':
        head = (head[0], head[1]+1)
    elif button == "down":
        head = (head[0], head[1]-1)
    elif button == "right":
        head = (head[0]+1, head[1])
    elif button == "left":
        head = (head[0]-1, head[1])

    if get(head) not in [0, 4]:
        return

    if get(head) == 4:
        if state['fruit']:
            state['current_fruit'] = state['fruit'].pop(0)
            paint(state['current_fruit'], 4)

    state['body'].append(head)

    #if len(game_state['body']) > 4:
    #    tail = game_state['body'].pop(0)
    #    if not tail in game_state['body']:
    #        paint(tail, 0)

    paint(head, 2)
    paint(state['body'][-2], 1)


def press_tile(x, y, game_state, paint, get):
    #print(x, y)
    pass


# maybe add a begin update and finish update functions...

# def update(event, game_state, board):

#     if event['type'] == "press_button":
#         if event['button'] == "up":

#             head = game_state['body'][-1]
#             head[1] += 1
#             board.set([0,0], 1)

