
def get(self, position):
    """
    get the symbol at a position on the grid
    i.e. get(([0,0])) -> 0
    """
    if self.current_grid().location_exists(position):
        return self.current_grid().get(position)
    return -1    
