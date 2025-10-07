
def get(self, _position, resolution=True):
    """
    get the symbol at a position on the grid
    i.e. get(([0,0])) -> 0
    """

    if resolution:
        position = [i * j for i,j in zip(_position, self.resolution)]
    else:
        position = _position
    
    if self.current_grid().location_exists(position):
        return self.current_grid().get(position)
    return -1    


def special_get(self, _position, resolution=True):

    if resolution:
        position = [i * j for i,j in zip(_position, self.resolution)]
    else:
        position = _position

    o = set()

    for i in range(self.resolution[0]):
        for j in range(self.resolution[1]):
            o.add(self.get((position[0] + i, position[1] + j), False))
    
    if -1 in o:
        o.remove(-1)

    o = [self._color_map[i] for i in o]
    if len(o) == 1:
        return o[0]

    return o


def contains(self, _position, *states):

    s = [i for i in states]

    found = special_get(self, _position)
    if isinstance(found, str):
        found = [found]

    for i in s:
        if i not in found:
            return False

    return True


def contains_either(self, _position, *states):

    s = [i for i in states]

    found = special_get(self, _position)
    if isinstance(found, str):
        found = [found]

    for i in s:
        if i in found:
            return True

    return False

