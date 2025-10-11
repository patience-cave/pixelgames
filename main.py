
import pygame
from grid import grid_stateful
from level import choose_game

THE_GAME = "chase"

class game:

    def __init__(self, margin_px=1, block_bx=10):

        self.board = grid_stateful()

        chosen_game = choose_game(THE_GAME, self.board)
        self.board.level = chosen_game

        # self.board.begin_method = chosen_game.begin
        # self.board.press_button_method = chosen_game.press_button
        # self.board.press_tile_method = chosen_game.press_tile
        # self.board.initialize_method = chosen_game.__init__
        
        self.input({"event": "init"})
        width = self.board.actual_size[0]
        height = self.board.actual_size[1]

        # ---- configurable bits ----
        self.N_COLS = width
        self.N_ROWS = height
        self.MARGIN_PX = margin_px
        self.INITIAL_SIZE = (width * block_bx, height * block_bx)
        self.CELL_SIZE = 0
        self.X0 = 0
        self.Y0 = 0

        self.layout(*self.INITIAL_SIZE)

    def input(self, code):
        return self.board.input(code)

    def layout(self, w, h):
        rows = self.N_ROWS
        cols = self.N_COLS
        margin = self.MARGIN_PX

        cell = min(
            (w - (cols + 1) * margin) // cols,
            (h - (rows + 1) * margin) // rows
        )
        self.CELL_SIZE = cell
        grid_w = cols * cell + (cols + 1) * margin
        grid_h = rows * cell + (rows + 1) * margin
        x0 = (w - grid_w) // 2
        y0 = (h - grid_h) // 2
        self.X0 = x0
        self.Y0 = y0

        return x0, y0, cell

    def build_rects(self):
        x0 = self.X0
        y0 = self.Y0
        cell = self.CELL_SIZE
        margin = self.MARGIN_PX
        rows = self.N_ROWS
        cols = self.N_COLS

        rects = []
        for r in range(rows):
            row_rects = []
            for c in range(cols):
                x = x0 + margin + c * (cell + margin)
                y = y0 + margin + (rows - 1 - r) * (cell + margin)
                # y = y0 + margin + r * (cell + margin)
                row_rects.append(pygame.Rect(x, y, cell, cell))
            rects.append(row_rects)
        return rects

    def cell_at(self, pos):
        cols = self.N_COLS
        rows = self.N_ROWS
        margin = self.MARGIN_PX
        cell = self.CELL_SIZE
        x0 = self.X0
        y0 = self.Y0

        mx, my = pos
        rel_x, rel_y = mx - x0, my - y0
        if rel_x < 0 or rel_y < 0: return None
        stride = cell + margin
        c = rel_x // stride
        r = rel_y // stride
        if 0 <= r < rows and 0 <= c < cols:
            #if (rel_x % stride) > margin and (rel_y % stride) > margin:
            # return int(r), int(c)
            return int(rows - 1 - r), int(c)
        return None


def main():
    game_board = game()

    pygame.init()
    pygame.display.set_caption("Tap a Block to Turn It White")
    
    screen = pygame.display.set_mode(game_board.INITIAL_SIZE, pygame.RESIZABLE)
    screen.fill((25,25,25))
    clock = pygame.time.Clock()

    colors = game_board.input("color_grid")
    rects = game_board.build_rects()
    
    for r in range(game_board.N_ROWS):
        for c in range(game_board.N_COLS):
            pygame.draw.rect(screen, colors[r][c], rects[r][c])


    game_board.input({"event": "begin"})
    pygame.display.flip()


    running = True

    while running:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                running = False
            
            #elif event.type == pygame.VIDEORESIZE:
            #    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                hit = game_board.cell_at(event.pos)
                if hit:
                    r, c = hit
                    game_board.input({
                        "event": "press_tile",
                        "position": [c, r]
                    })

            elif event.type == pygame.KEYDOWN:

                keys = {
                    pygame.K_SPACE: "space",
                    pygame.K_a: "left",
                    pygame.K_w: "up",
                    pygame.K_s: "down",
                    pygame.K_d: "right",
                    pygame.K_p: "p",
                    pygame.K_UP: "up",
                    pygame.K_DOWN: "down",
                    pygame.K_LEFT: "left",
                    pygame.K_RIGHT: "right",
                    pygame.K_RETURN: "undo",
                    pygame.K_0: "reset",
                }

                if event.key in keys:
                    game_board.input({
                        "event": "press_button",
                        "button": keys[event.key]
                    })

        dirty = []
        for i in game_board.input("update"):
            if i['result'] == "change_color":
                r = i["position"][1]
                c = i["position"][0]
                colors[r][c] = i["to_color"]
                pygame.draw.rect(screen, colors[r][c], rects[r][c])
                dirty.append(rects[r][c])

        if dirty:
            pygame.display.update(dirty)
            dirty.clear()

        if game_board.board.animations:
            clock.tick(20)
        else:
            clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()