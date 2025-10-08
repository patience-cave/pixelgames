try:
    from grid_methods.spotlight import spotlight_changes
except:
    from spotlight import spotlight_changes


def lose(self, animated=True, use_attempt=True):

    speed = (max(self.actual_size[0],self.actual_size[1]) / 2) / 20
    time = 0.4

    spots = spotlight_changes(self.actual_size[0], self.actual_size[1], speed / time )
    lose_color = self._colors["lose"].index

    if animated:

        for i in spots[::-1]:
            for j in i:
                self.set(j, lose_color, _resolution=False, _origin=False, _fast=True)
            self.next_frame()
    

    if use_attempt:
        on_attempt = self.current_state.attempt + 1
    else:
        on_attempt = self.current_state.attempt

    on_level = self.current_state.level

    self.current_state = self.states[0].duplicate()
    self.current_state.move = 0
    self.states = [self.states[0]]

    self.clear()

    if on_attempt > self.current_state.max_attempts:
        self.current_state.attempt = 1
        self.current_state.level = 1
    else:
        self.current_state.level = on_level
        self.current_state.attempt = on_attempt

    self.clear()

    self.begin()

    o = []
    for i in spots[::-1]:
        o.append([])
        for j in i:
            o[-1].append((j, self.get(j)))
            self.set(j, lose_color, _resolution=False, _origin=False, _fast=True)

    
    for i in o[::-1]:
        for j, k in i:
            self.set(j, k, _resolution=False, _origin=False, _fast=True)
        
        if animated:
            self.next_frame()
