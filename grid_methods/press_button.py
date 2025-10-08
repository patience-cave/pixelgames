from state import State

previous_button = None
current_button = None

def press_button(self, button):

    if self.animations: return []
    if self.intended_actions[0]: return

    if self.press_button_method == None: return

    button_state = State()
    button_state.dx = 0
    button_state.dy = 0
    button_state.up = button == 'up'
    button_state.down = button == 'down'
    button_state.right = button == 'right'
    button_state.left = button == 'left'
    button_state.name = button

    # lazy implementation of previous button
    global current_button
    global previous_button
    previous_button = current_button
    button_state.previous_button = previous_button
    current_button = button_state.name

    if button == "reset":
        self.reset()
        return
    elif button == "undo":
        self.undo()
        return

    if button_state.up or button_state.down:
        button_state.dy = 1 if button_state.up else -1
    elif button_state.right or button_state.left:
        button_state.dx = 1 if button_state.right else -1
    
    self.current_state = self.current_state.duplicate()
    self.current_state.event = "press_button"
    self.press_button_method(self.current_state, button_state)
    
    # do not save the new state if no changes happened on screen
    if self.has_intended_actions():
        self.states.append(self.current_state)


        
