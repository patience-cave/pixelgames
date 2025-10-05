
# TODO: Remember to make a new state even when animating, just increase the frame lol

def update(self):


    # if an animation is currently happening, keep resolving it each update
    if self.animations:
        #print('animating...')

        current_animation = self.animations[0]
        self.animations = self.animations[1:]

        return current_animation


    # if there is no action, kill the function early
    if not self.intended_actions[0]:
        return []

    # print('updating...')

    action = self.resolve_intended_actions(self.intended_actions)
    self.intended_actions = [[]]

    # if the action is not an undo, preserve it in the action history
    if not action["type"] == "undo":
        self.current_state.action = action

    # if it returns more than one action
    # pop the other actions into the animation
    
    actions = self.resolve_action(action)

    first_action = actions.pop(0)
    self.animations = actions

    return first_action
