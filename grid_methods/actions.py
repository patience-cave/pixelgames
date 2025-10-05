
def remove_empty_elements(l):
    return [x for x in l if x != []]


def next_frame(self):
    self.intended_actions.append([])

# returns the current action plus and animation buffer
# returns the full animation [[action], [action], [action], ...]
def resolve_action(self, a, isundo=False):

    if a == None:
        return []

    if a["type"] == "change_color":

        # swap colors if undoing, don't forget to force change the color state
        # I am forcing the color change by calling self.grid.set instead of self.set
        if isundo:
            self.current_grid().set(a["position"], a["from_color"])
            a["from_color"], a["to_color"] = a["to_color"], a["from_color"]

        return [[{
            "result": "change_color",
            "position": a["position"],
            "to_color": self._state_to_color(a["to_color"])
        }]]

    elif a["type"] == "animation":

        # play the animation backwards if you are undoing
        if isundo:
            a["list"] = a["list"][::-1]

        o = []
        for i in a['list']:
            p = self.resolve_action(i, isundo)
            o += p
        return o

    elif a["type"] == "many":

        # it probably makes sense to play all changes backwards too if undoing
        if isundo:
            a["list"] = a["list"][::-1]

        o = [[]]
        for i in a['list']:
            p = self.resolve_action(i, isundo)
            if len(p) == 1:
                o[-1] += p[0]
            else:
                o += p
                o += [[]]
        o = remove_empty_elements(o)

        return o

    elif a["type"] == "undo":
        assert(not isundo)
        return self.resolve_action(a["action"], True)

def has_intended_actions(self):

    self.intended_actions = remove_empty_elements(self.intended_actions)

    for i in self.intended_actions:
        if i: return True

    self.intended_actions = [[]]
    return False

def resolve_intended_actions(self, ia):

    if not self.has_intended_actions(): return
    # if the final animation has not been populated, remove it
    while len(ia) and (not ia[-1]): ia.pop(-1)
    assert(ia)

    # if there is only one action to animate
    if len(ia) == 1:

        _intended_action = ia[0]

        if len(_intended_action) == 1:
            return _intended_action[0]
        else:
            return {
                "type": "many",
                "list": _intended_action
            }

    # longer animation
    else:
        return {
            "type": "animation",
            "list": [self.resolve_intended_actions([i]) for i in ia]
        }
