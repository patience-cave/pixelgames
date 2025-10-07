from state import State

def add_objects(self, objects):

    for object in objects:
        self.add_colors(object.colors)

    self.current_state.objects += objects


def find_all(type_name, items):
    # Get the actual class object from the built-in namespace
    return [item for item in items if item.id == type_name]

def find_object(self, name):
    o = find_all(name, self.current_state.objects)
    return o[0]

