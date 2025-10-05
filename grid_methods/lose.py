from grid_methods.spotlight import spotlight_changes

def lose(self):

    speed = (max(self.size[0],self.size[1]) / 2) / 20
    time = 0.3

    spots = spotlight_changes(self.size[0], self.size[1], speed / time )

    for i in spots[::-1]:
        for j in i:
            self.set(j, 4)
        self.next_frame()

    for i in spots:
        for j in i:
            self.set(j, 0)

    #self.states = [self.states[0]]
    self.current_state = self.states[0].duplicate()

    for i in self.iterate_grid():
        self.set(i, 0)

    self.begin()

    o = []
    for i in spots[::-1]:
        o.append([])
        for j in i:
            o[-1].append((j, self.get(j)))
            self.set(j, 4)

    for i in o[::-1]:
        for j, k in i:
            self.set(j, k)
        self.next_frame()
