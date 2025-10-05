
def undo(self):
    if self.intended_actions[0]: return
    if self.animations: return
    if len(self.states) <= 1: return

    a = self.previous_state()

    self.intended_actions[-1].append({
        "type": "undo",
        "action": a["action"]
    })

    self.states.pop()
    self.current_state = self.states[-1].duplicate()



