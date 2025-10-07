try:
    from grid_methods.spotlight import spotlight_changes
except:
    from spotlight import spotlight_changes


def lose(self, animated=True, use_attempt=True):

    speed = (max(self.actual_size[0],self.actual_size[1]) / 2) / 20
    time = 0.3

    spots = spotlight_changes(self.actual_size[0], self.actual_size[1], speed / time )
    lose_color = self._colors["lose"].index

    if animated:

        for i in spots[::-1]:
            for j in i:
                self.set(j, lose_color, False)
            self.next_frame()


    for i in spots:
        for j in i:
            self.set(j, 0, False)


    if use_attempt:
        on_attempt = self.current_state.attempt + 1
    else:
        on_attempt = self.current_state.attempt

    on_level = self.current_state.level

    self.current_state = self.states[0].duplicate()
    self.current_state.move = 0
    self.states = [self.states[0]]

    if on_attempt > self.current_state.max_attempts:
        self.current_state.attempt = 1
        self.current_state.level = 1
    else:
        self.current_state.level = on_level
        self.current_state.attempt = on_attempt

    for i in self.iterate_grid():
        self.set(i, 0, False)

    self.begin()

    o = []
    for i in spots[::-1]:
        o.append([])
        for j in i:
            o[-1].append((j, self.get(j, False)))
            self.set(j, lose_color, False)

    
    for i in o[::-1]:
        for j, k in i:
            self.set(j, k, False)
        
        if animated:
            self.next_frame()
