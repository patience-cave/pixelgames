


def reset(self, _animated=True):

    if self.intended_actions[0]: return
    if self.animations: return
    if len(self.states) <= 1: return

    on_level = self.current_state.level
    on_attempt = self.current_state.attempt

    if _animated:

        self.intended_actions[-1].append({
            "type": "undo",
            "action": {
                "type": "animation",
                "list": [ i.action for i in self.states[1:]]
            }
        })

        self.states = [self.states[0]]
        self.current_state = self.states[0]
        self.current_state.level = on_level
        self.current_state.attempt = on_attempt

    else:

        self.lose(animated=False, use_attempt=False)

        
        # self.animations = []
        # self.intended_actions = [[]]

        # self.states = [self.states[0]]
        # self.current_state = self.states[0]
        # self.current_state.level = on_level
        # self.current_state.attempt = on_attempt
        
        # self.begin()
