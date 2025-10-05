

from hmac import new


def set(self, _position, to, resolution=True):

    positions = []

    if resolution:
        origin = [i * j for i,j in zip(_position, self.resolution)]
        for i in range(self.resolution[0]):
            for j in range(self.resolution[1]):
                positions.append((origin[0] + i, origin[1] + j))
    else:
        positions = [_position]

    for position in positions:

        previous_state = self.current_grid().get(position)

        if self.current_grid().set(position, to):

            new_state = self.current_grid().get(position)

            # if the previous color state equals the new color state cancel the action
            if previous_state == new_state:
                return

            self.intended_actions[-1].append({
                "type": "change_color",
                "position": position,
                "from_color": previous_state,
                "to_color": new_state
            })


        
