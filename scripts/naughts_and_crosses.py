import pygame
import sys
import time
import copy
import math

pygame.init()
window = pygame.display.set_mode((900,900))
clock = pygame.time.Clock()

run = True
turn = "X"
draw = False
is_terminal = False
winner = ""
turn_number = 0
score = 0

background = pygame.Surface(window.get_size())
ts, w, h, c1, c2 = 300, *background.get_size(), (128, 128, 128), (64, 64, 64)
tiles = [((x*ts, y*ts, ts, ts), c1 if (x+y) % 2 == 0 else c2) for x in range((w+ts-1)//ts) for y in range((h+ts-1)//ts)]
[pygame.draw.rect(background, color, rect) for rect, color in tiles]

x_img = pygame.image.load("image_folder/x.png") # loading the images as python object
y_img = pygame.image.load("image_folder/o.png")

x_img = pygame.transform.scale(x_img, (290, 290)) # resizing images
o_img = pygame.transform.scale(y_img, (290, 290))

grid = [["" for _ in range(3)] for _ in range(3)]

def drawXO(row, col, turn):
    global board
    posx = col * ts + 5     # for the second row, the image
    posy = row * ts + 5     # should be pasted at a x coordinate
                            # of x from the game line
    if turn == "X":                             # setting up the required board value to display
        window.blit(x_img, (posx, posy))        # pasting x_img over the screen at a coordinate position of (pos_y, posx) defined in the above code.

    elif turn == "O":
        window.blit(o_img, (posx, posy))


def check_for_terminal(is_terminal):
    for i in range(3):
        if grid[i][0] == grid[i][1] == grid[i][2] != "":
            is_terminal = True
            return is_terminal
        if grid[0][i] == grid[1][i] == grid[2][i] != "":
            is_terminal = True
            return is_terminal

    if grid[0][0] == grid[1][1] == grid[2][2] != "":
        is_terminal = True
        return is_terminal

    if grid[0][2] == grid[1][1] == grid[2][0] != "":
        is_terminal = True
        return is_terminal

    if all(cell != "" for row in grid for cell in row):
        is_terminal = True
        return is_terminal

    is_terminal = False
    return is_terminal

def minimax(node, depth, maximizingPlayer, is_terminal):
    if depth == 0 or is_terminal == True:
        return heuristic_value(node)

    best_move = None
    player = "O" if maximizingPlayer else "X"

    if maximizingPlayer:
        value = -math.inf
        for child, _ in get_children(node, player):
            value = max(value, minimax(child, depth - 1, False))
        return value
    else:
        value = math.inf
        for child, _ in get_children(node, player):
            value = min(value, minimax(child, depth - 1, True))
        return value


def get_children(node, player):
    children = []
    for row in range(3):
        for col in range(3):
            if node[row][col] == "":
                new_node = copy.deepcopy(node)
                new_node[row][col] = player
                children.append((new_node, (row, col)))
    return children
    

def heuristic_value(node):
    for i in range(3):
        if node[i][0] == node[i][1] == node[i][2] != "":
            return 10 if node[i][0] == "O" else -10
        if node[0][i] == node[1][i] == node[2][i] != "":
            return 10 if node[0][i] == "O" else -10

    if node[0][0] == node[1][1] == node[2][2] != "":
        return 10 if node[0][0] == "O" else -10
    if node[0][2] == node[1][1] == node[2][0] != "":
        return 10 if node [0][2] == "O" else -10

    return 0


def find_best_move(is_terminal):
    best_score = -math.inf
    best_move = None
    for child, move in get_children(grid, "O"):
        depth = 4
        maximizingPlayer = False
        score = minimax(child, is_terminal, depth, maximizingPlayer)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move


def validation(grid, is_terminal, winner, draw):

    for i in range(3):
        if grid[i][0] == grid[i][1] == grid[i][2] != "":
            winner = grid[i][0]
            is_terminal = True
        
        if grid[0][i] == grid[1][i] == grid[2][i] != "":
            winner = grid[0][i]
            is_terminal = True

    if [grid[i][i] for i in range(3)].count("X") == 3:
        winner = "X"
        is_terminal = True

    elif [grid[i][i] for i in range(3)].count("O") == 3:
        winner = "O"
        is_terminal = True

    if [grid[i][2-i] for i in range(3)].count("X") == 3:
        winner = "X"
        is_terminal = True

    elif [grid[i][2-i] for i in range(3)].count("O") == 3:
        winner = "O"
        is_terminal = True

    if all(cell != "" for row in grid for cell in row):
        draw = True
        is_terminal = True

    print("Is it a draw? =",draw)
    print("Is it terminal? =",is_terminal)
    announcment(is_terminal, winner, draw)

def announcment(is_terminal, winner, draw):
    # Win Consequence
    print (draw + is_terminal)
    if is_terminal == True:
        if winner == "X" or "O":
            print(winner+" has won the game.")
            time.sleep(3)
            pygame.quit()
            sys.exit()

        #Draw consequene
        if draw == True:
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
            
            if is_terminal == False:
            # Check bounds and update grid if cell is empty
                if (0 <= row < 3 and 0 <= col < 3):
                    if grid[row][col] == "":
                        grid[row][col] = turn
                        turn = "O" if turn == "X" else "X"
                        if turn == "O":
                            move = find_best_move(is_terminal)
                            if move:
                                row, col = move
                                grid[row][col] = "O"
                                turn = "X"
                        validation(grid, is_terminal, winner, draw)
                        print(f"Placed {turn} at ({row}, {col})")
                        
                    else:
                        print(f"Cell ({row}, {col}) already occupied by {grid[row][col]}")

            if is_terminal == True:
                announcment(is_terminal, winner, draw)

    window.blit(background, (0, 0))

    for row in range(3):
        for col in range(3):
            if grid[row][col] != "":
                drawXO(row, col, grid[row][col])

    pygame.display.update()
    clock.tick(60)
