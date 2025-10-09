from helper import chunk_list_avg_size

class on_board:
    def __init__(self, game, input={}):
        self.positions = input.get("positions") or []
    
    def render(self, game):
        for position in self.positions:
            game.set(position, list(self.colors.keys())[0])



class levels_left:
    def __init__(self, game):
        self.id = "levels_left"
        self.colors = {
            "unused level": "black",
            "used level": "white"
        }
        game.protected_colors += ["used level", "unused level"]
        self.on_level = 0
    
    def render(self, game):

        positions_list = []
        for i in range(game.actual_size[0]):
            positions_list.append([i, 0])
        
        chunk_size = len(positions_list) / game.max_levels
        self.positions = chunk_list_avg_size(positions_list, chunk_size)

        self.update_level(game)

    def update_level(self, game):

        for i, ps in enumerate(self.positions):
            if game.level > i + 1:
                for j in ps:
                    game.set(j, "used level", _resolution=False, _origin=False)
            else:
                for j in ps:
                    game.set(j, "unused level", _resolution=False, _origin=False)



class moves_left:
    def __init__(self, game):
        self.id = "moves_left"
        self.colors = {
            "unused move": "orange",
            "used move": "dark red"
        }
        game.protected_colors += ["used move", "unused move"]
        self.on_move = 0

    def render(self, game):

        # paint the border
        for i in range(game.actual_size[0]):
            game.set((0,i), "unused move", _resolution=False, _origin=False)
            game.set((game.actual_size[0]-1,i), "unused move", _resolution=False, _origin=False)
            game.set((i,game.actual_size[1]-1), "unused move", _resolution=False, _origin=False)

        # generate the list of positions
        positions_list = []
        for i in range(game.actual_size[0]//2):
            halfway = game.actual_size[0]//2
            top = game.actual_size[1] - 1
            positions_list.append([(halfway-i-1, top), (halfway+i, top)])
        self.positions = positions_list

        for i in range(game.actual_size[1]-1)[::-1]:
            positions_list.append([(0,i), (game.actual_size[0]-1,i)])
        
        # chunk the list
        chunk_size = len(positions_list) / game.max_moves
        self.positions = chunk_list_avg_size(positions_list, chunk_size)

    def use_move(self, game):
        if self.on_move >= len(self.positions):
            return
        
        positions = self.positions[self.on_move]
        for i in positions:
            game.set(i[0], "used move", _resolution=False, _origin=False)
            game.set(i[1], "used move", _resolution=False, _origin=False)

        self.on_move += 1
