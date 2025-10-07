
def input(self, code):

    if type(code) is str:
        event = code
    else:
        event = code['event']

    if self.current_state != None:
        if self.current_state.level > self.current_state.max_levels:
            if event in ["undo", "reset"]:
                pass
            elif event == "press_button" and code["button"] in ["undo", "reset"]:
                pass
            else:
                return

    if event == "press_tile":
        self.press_tile(code['position'])

    elif event == "press_button":
        self.press_button(code['button'])
        if self.has_intended_actions():
            if code['button'] != "reset":
                self.current_state.move += 1
            if self.current_state.move == self.current_state.max_moves:
                self.current_state.lose = True

    elif event == "begin":
        self.begin()

    elif event == "undo":
        self.undo()

    elif event == "reset":
        self.reset()

    elif event == "init":
        self.initialize()

    elif event == "color_grid":
        return self.make_color_grid()

    elif event == "update":
        return self.update()

    elif event == "next_frame":
        self.next_frame()

    if self.current_state.win:
        self.win()
    elif self.current_state.lose:
        self.lose()
    
    