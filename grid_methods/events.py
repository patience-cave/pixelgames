
def input(self, code):

    if type(code) is str:
        event = code
    else:
        event = code['event']

    if event == "press_tile":
        self.press_tile(code['position'])

    elif event == "press_button":
        self.press_button(code['button'])

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
    
    