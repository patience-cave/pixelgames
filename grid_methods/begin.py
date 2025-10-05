from state import State

def begin(self):
    if not self.states: return
    if self.begin_method == None: return
    
    self.begin_method(self.states[0])
    
