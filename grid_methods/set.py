

def set(self, position, to):
    
    previous_state = self.current_grid().get(position)

    if self.current_grid().set(position, to):

        new_state = self.get(position)

        # if the previous color state equals the new color state cancel the action
        if previous_state == new_state:
            return

        self.intended_actions[-1].append({
            "type": "change_color",
            "position": position,
            "from_color": previous_state,
            "to_color": new_state
        })


        
