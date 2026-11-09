import pygame 
from ruleset import Ruleset, Checkers 
from gui import Gui 
from bot import Bot 

def main():
    gui = Gui()
    rules = Ruleset()
    rules = Checkers(rules)

    while True:
        # Maps the square(background) clicked (with the mouse) to iself.tile_size corresponding grid position
        # Row = x axis, Column = y axis 
        row = 0
        column = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gui.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
                mouse_x, mouse_y = event.pos
                print(f"mouse_x = {mouse_x}, mouse_y = {mouse_y}")
                row, column = mouse_y // gui.tile_size, mouse_x // gui.tile_size
                print(f"row/x-axis = {row}, column/y-axis = {column}")
                rules.progress_game(row, column)

        gui.update_window(column, row, rules.turn, rules.grid)

main()
