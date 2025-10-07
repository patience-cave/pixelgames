from state import State

def add_objects(self, objects):

    for object in objects:
        self.add_colors(object.colors)

    self.current_state.objects += objects

    for color in self.current_state.protected_colors:
        self._protected_colors.add( self._colors[color].index )


def find_all(self, type_name):
    items = self.current_state.objects
    # Get the actual class object from the built-in namespace
    found = []
    for item in items:
        if item.id == type_name:
            found.append(item)
    return found
    #return [item for item in items if item.id == type_name]

def find_object(self, name):
    o = self.find_all(name)
    return o[0]

