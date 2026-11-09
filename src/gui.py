import pygame
import sys

class Gui:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((900,900))
        self.clock = pygame.time.Clock()
        self.background = pygame.Surface(self.window.get_size())

        self.tile_size = 300
        self.window_size, self.h = self.background.get_size()
        self.c1 = (128, 128, 128)
        self.c2 = (64, 64, 64)

        #TODO: refactor
        self.tiles = [((x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size), self.c1 if (x + y) % 2 == 0 else self.c2) for x in range((self.window_size+self.tile_size-1)//self.tile_size) for y in range((self.h+self.tile_size-1)//self.tile_size)]
        [pygame.draw.rect(self.background, color, rect) for rect, color in self.tiles]

        self.Image.x = pygame.image.load("assets/x.png")
        self.Image.x = pygame.transform.scale(self.Image.x, (290, 290))
        self.Image.o = pygame.image.load("assets/o.png")
        self.Image.o = pygame.transform.scale(self.Image.o, (290, 290))

    def quit(self):
        print("See you next time")
        pygame.quit()
        sys.exit()

    def draw_piece(self, column, row, turn):
        # global board

        """
        For the second row, the image should be pasted at a x coordinate
        of x from the game line (what is the game line?)
        """

        x = column * self.tile_size + 5
        y = row * self.tile_size + 5
        
        """
        Setting up the required board value to display
        pasting Image.x over the screen at a coordinate position of (pos_y, posx) o
        defined in the above code.
        """

        if turn == "X":
            self.window.blit(self.Image.x, (x, y))

        elif turn == "O":
            self.window.blit(self.Image.o, (x, y))

    # What is coulmn, what is row, where do they come from (grid[0,1]?)

    def update_window(self, column, row, turn, grid):
        self.window.blit(self.background, (0, 0))

        for row in range(3):
            for column in range(3):
                if grid[row][column] != "":
                    self.draw_piece(row, column, turn)

        pygame.display.update()
        self.clock.tick(60)

    class Image:
        pass
