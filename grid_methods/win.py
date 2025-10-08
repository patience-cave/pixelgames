try:
    from grid_methods.spotlight import spotlight_changes
except:
    from spotlight import spotlight_changes


def win(self):
    
    speed = (max(self.actual_size[0],self.actual_size[1]) / 2) / 20
    time = 0.8

    # speed needs to be 0.75 seconds
    spots = spotlight_changes(self.actual_size[0], self.actual_size[1], speed / time)

    win_color = self._colors["win"].index

    for i in spots:
        for j in i:
            self.set(j, win_color, _resolution=False, _origin=False, _fast=True)
        self.next_frame()

    
    on_level = self.current_state.level + 1
    
    if on_level > self.current_state.max_levels:
        return

    self.current_state = self.states[0].duplicate()
    self.states = [self.states[0]]

    self.current_state.attempt = 1
    self.current_state.level = on_level

    self.clear()

    self.begin()

    o = []
    for i in spots[::-1]:
        o.append([])
        for j in i:
            o[-1].append((j, self.get(j)))
            self.set(j, win_color, _resolution=False, _origin=False, _fast=True)
    

    for i in o:
        for j, k in i:
            self.set(j, k, _resolution=False, _origin=False, _fast=True)
        self.next_frame()

    self.states = [self.current_state]


