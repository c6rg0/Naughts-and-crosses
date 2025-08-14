import pygame
import sys
import time
import local_lib

turn = "X"
run = True
draw = False
game = True
is_terminal = False
winner = ""
turn_number = 0
score = 0

pygame.init()
window = pygame.display.set_mode((900, 900))
clock = pygame.time.Clock()

background = pygame.Surface(window.get_size())
ts, w, h, c1, c2 = 300, *background.get_size(), (128, 128, 128), (64, 64, 64)
tiles = [((x*ts, y*ts, ts, ts), c1 if (x+y) % 2 == 0 else c2) for x in range((w+ts-1)//ts) for y in range((h+ts-1)//ts)]
[pygame.draw.rect(background, color, rect) for rect, color in tiles]

x_img = pygame.image.load("~/image_folder/X.png") # loading the images as python object
y_img = pygame.image.load("~/image_folder/o.png")

x_img = pygame.transform.scale(x_img, (290, 290)) # resizing images
o_img = pygame.transform.scale(y_img, (290, 290))

grid = [["" for _ in range(3)] for _ in range(3)]
print(grid)


def drawXO(row, col, turn):
    global board
    posx = col * ts + 5     # for the second row, the image
    posy = row * ts + 5     # should be pasted at a x coordinate
                            # of x from the game line
    if turn == "X":                             # setting up the required board value to display
        window.blit(x_img, (posx, posy))        # pasting x_img over the screen at a coordinate position of (pos_y, posx) defined in the above code.

    elif turn == "O":
        window.blit(o_img, (posx, posy))

# Node = The board (the state it is in - as far as I'm aware). 
# Depth = Number of moves that the algorithm should 
#         analyze.
# MaximizingPlayer = The evaluated score of the players position/move.

def evaluation(): # Getting a score for the minimax algorithm

    if turn == "x":
        turn_number[1] = turn_number[1] + 1

        if turn_number[1] == 1:
            score[1] = 1

        if turn_number[1] > 1:

            for i in range(2):
                if grid[i][0] == grid[i][1] == grid[i][2] != "":
                    score[1] = 2

                if grid[0][i] == grid[1][i] == grid[2][i] != "":
                    score[1] = 2


            if [grid[i][i] for i in range(2)].count("X") == 3:
                score[1] = 2

            elif [grid[i][i] for i in range(2)].count("O") == 3:
                score[1] = 2

            if [grid[i][2-i] for i in range(2)].count("X") == 3:
                score[1] = 2

            elif [grid[i][2-i] for i in range(2)].count("O") == 3:
                score[1] = 2

    elif turn == "o":
        turn_number[0] = turn_number[0] + 1

        if turn_number[0] == 1:
            score[0] = 1

        if turn_number[0] > 1:

            for i in range(2):
                if grid[i][0] == grid[i][1] == grid[i][2] != "":
                    score[0] = 2
    

                if grid[0][i] == grid[1][i] == grid[2][i] != "":
                    score[0] = 2
    

            if [grid[i][i] for i in range(2)].count("X") == 2:
                score[0] = 2

            elif [grid[i][i] for i in range(2)].count("O") == 2:
                score[0] = 2

            if [grid[i][2-i] for i in range(2)].count("X") == 2:
                score[0] = 2

            elif [grid[i][2-i] for i in range(2)].count("O") == 2:
                score[0] = 2

    print(score)
    return score


minimax(score)


def validation(grid, is_terminal):
    global win, game, winner, draw

    for i in range(3):
        if grid[i][0] == grid[i][1] == grid[i][2] != "":
            win = True
            winner = grid[i][0]
            is_terminal = True
        
        if grid[0][i] == grid[1][i] == grid[2][i] != "":
            win = True
            winner = grid[0][i]
            is_terminal = True

    if [grid[i][i] for i in range(3)].count("X") == 3:
        win = True
        winner = "X"
        is_terminal = True

    elif [grid[i][i] for i in range(3)].count("O") == 3:
        win = True
        winner = "O"
        is_terminal = True

    if [grid[i][2-i] for i in range(3)].count("X") == 3:
        win = True
        winner = "X"
        is_terminal = True

    elif [grid[i][2-i] for i in range(3)].count("O") == 3:
        win = True
        winner = "O"
        is_terminal = True

    if all(cell != "" for row in grid for cell in row):
        draw = True
        is_terminal = True

    print("Is it a draw? =",draw)
    print("Is it terminal? =",is_terminal)
    return draw, is_terminal


def announcment(is_terminal, winner, draw):
    # Win Consequence
    if is_terminal  == True:
        print(winner+" has won the game.")
        time.sleep(3)
        pygame.quit()
        sys.exit()

    #Draw consequene
    if is_terminal == True:
        print("Draw")
        time.sleep(3)
        pygame.quit()
        sys.exit()


while run == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
        # Maps the square(background) clicked (with the mouse) to its corresponding grid position
        # Row = left to right, Column = up and down
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
            mx, my = event.pos # Mouse x and Mouse y
            row, col = my // ts, mx // ts
            print(row, col)
            
            if game == True:
            # Check bounds and update grid if cell is empty
                if (0 <= row < 3 and 0 <= col < 3):
                    if grid[row][col] == "":
                        grid[row][col] = turn
                        turn = "O" if turn == "X" else "X"
                        validation(grid)
                        print(f"Placed {turn} at ({row}, {col})") # the code runs the while loop for each (players) turn

                    else:
                        print(f"Cell ({row}, {col}) already occupied by {grid[row][col]}")
                    
    window.blit(background, (0, 0))

    for row in range(3):
        for col in range(3):
            if grid[row][col] != "":
                drawXO(row, col, grid[row][col])

    pygame.display.update()
    clock.tick(60)

    if not game:
        announcment(win, winner, draw)

