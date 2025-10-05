from grid_methods.spotlight import spotlight_changes

def win(self):
    
    speed = (max(self.size[0],self.size[1]) / 2) / 20
    time = 0.5

    # speed needs to be 0.75 seconds
    spots = spotlight_changes(self.size[0], self.size[1], speed / time)

    for i in spots:
        for j in i:
            self.set(j, 2)
        self.next_frame()

