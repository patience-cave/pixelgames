from state import State

def begin(self):
    if not self.states: return
    if self.begin_method == None: return
    
    self.current_state.objects = []
    self.begin_method(self.current_state)

    for object in self.current_state.objects:
        object.render(self.current_state)
    

    #print(self.current_state)
    #print(self.intended_actions)