
def get(self, _position):
    """
    get the symbol at a position on the grid
    i.e. get(([0,0])) -> 0
    """
    
    if self.current_grid().location_exists(_position):
        return self.current_grid().get(_position)
    return -1    

def special_get(self, _position, _resolution=None, _origin=None):

    if _resolution == None:
        _resolution = self.current_state.resolution
    elif _resolution == False:
        _resolution = [1,1]

    # origin is not given regarding the resolution
    if _origin == None:
        _origin = self.current_state.origin
    elif _origin == False:
        _origin = [0,0]

    o = set()

    for i in range(_resolution[0]):
        for j in range(_resolution[1]):
            result = self.get((_position[0] * _resolution[0] + _origin[0] + i, _position[1] * _resolution[1] + _origin[1] + j))
            o.add(result)
    
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

