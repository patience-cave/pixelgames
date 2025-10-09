import json

class game_template:

    def __init__(self, game):
        pass

    def initialize_objects(self, game):

        try:
            json_file = f"levels/{self.game_name}-design.json"
            with open(json_file, "r") as f:
                data = json.load(f)
        except:
            json_file = f"{self.game_name}-design.json"
            with open(json_file, "r") as f:
                data = json.load(f)

        if "initialized" not in game:
            game.size = data.get("size") or [64, 64]
            game.resolution = data.get("resolution") or [1,1]
            game.origin = data.get("origin") or [0,0]
            game.level = data.get("level") or 1
            if "background" in data:
                game.set_background(data["background"])

        level_data = data["levels"][(game.level - 1) % len(data["levels"])]
        game["origin"] = [0,0]

        if "initialized" not in game:
            game.max_levels = data.get("max_levels") or len(data["levels"])
            game.initialized = True

        for item in level_data:
            if item == "objects":
                continue
            game[item] = level_data[item]

        # automatically calculate origin
        if "origin" not in level_data and "board_size" in level_data:
            game.origin = [
                (game.actual_size[0] - level_data["board_size"][0] * game.resolution[0]) // 2,
                (game.actual_size[1] - level_data["board_size"][1] * game.resolution[1]) // 2
            ]

        objects = level_data["objects"]

        unseen_objects = list(game.list_of_objects.keys())
        _objects = []

        for object_type in objects:

            object_class = game.list_of_objects[object_type]
            #o = object_class(game, *objects[object_type].values())
            if objects[object_type] == {}:
                o = object_class(game)
            else:
                o = object_class(game, objects[object_type])

            _objects.append(o)

            if object_type in unseen_objects:
                # remove object_type from unseen_objects
                unseen_objects = [o for o in unseen_objects if o != object_type]

        for object_type in unseen_objects:
            object_class = game.list_of_objects[object_type]
            o = object_class(game)
            _objects.append(o)

        game.add_objects(_objects)

    def begin(self, game):
        self.initialize_objects(game)
    
    def press_button(self, game, button):
        pass
    
    def press_tile(self, game, x, y):
        pass
