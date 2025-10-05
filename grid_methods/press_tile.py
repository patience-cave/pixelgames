
def press_tile(self, position):
    if self.animations: return []
    if self.intended_actions[0]: return
    if self.press_tile_method == None: return

    self.current_state = self.current_state.duplicate()
    self.current_state.event = "press_button"

    self.press_tile_method(self.current_state, position[0], position[1])

    # do not save the new state if no changes happened on screen
    if self.has_intended_actions():
        self.states.append(self.current_state)