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

        level_data = data["levels"][(game.level - 1) % len(data["levels"])]

        for item in level_data:
            if item == "objects":
                continue
            game[item] = level_data[item]

        objects = level_data["objects"]

        unseen_objects = set(game.list_of_objects.keys())
        _objects = []

        for object_type in objects:

            object_class = game.list_of_objects[object_type]
            o = object_class(game, *objects[object_type].values())
            _objects.append(o)

            if object_type in unseen_objects:
                unseen_objects.remove(object_type)

        for object_type in unseen_objects:
            object_class = game.list_of_objects[object_type]
            o = object_class(game)
            _objects.append(o)

        game.add_objects(_objects)

    def begin(self, game):
        pass
    
    def press_button(self, game, button):
        pass
    
    def press_tile(self, game, x, y):
        pass
