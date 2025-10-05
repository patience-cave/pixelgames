
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
