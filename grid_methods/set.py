

def clear(self):
    # self.set([0,0], 0, _resolution=self.actual_size, _origin=[0,0], _fast=True)
    for i in self.current_grid().bitgrids:
        i.bits = 0


def set_rect(self, _to, _position, _size):
    offset = self.current_state.origin
    _resolution = self.current_state.resolution
    _origin = [i * j + k for i,j,k in zip(_position, _resolution, offset)]
    self.set([0,0], _to, _resolution=[i*j for i,j in zip(_size, self.current_state.resolution)], _origin=_origin)


def set(self, _position, _to, _resolution=None, _origin=None, _fast=False):

    if _resolution == None:
        _resolution = self.current_state.resolution
    elif _resolution == False:
        _resolution = [1,1]

    # origin is not given regarding the resolution
    if _origin == None:
        _origin = self.current_state.origin
    elif _origin == False:
        _origin = [0,0]

    # convert string to index
    if isinstance(_to, str):
        _to = self._colors[_to].index

    positions = []

    origin = [i * j for i,j in zip(_position, _resolution)]
    for i in range(_resolution[0]):
        for j in range(_resolution[1]):
            positions.append((origin[0] + i + _origin[0], origin[1] + j + _origin[1]))

    for position in positions:

        # you cannot undo a fast action
        if _fast:
            self.intended_actions[-1].append({
                "type": "change_color",
                "position": position,
                "to_color": _to
            })
            continue
    
        previous_state = self.current_grid().get(position)

        # if you are trying to write over a "used move" or "unused move" ... return
        if previous_state in self._protected_colors:
            if _to > 2 and _to not in self._protected_colors:
                continue

        if self.current_grid().set(position, _to):

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


