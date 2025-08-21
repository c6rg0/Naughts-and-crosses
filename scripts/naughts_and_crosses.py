import pygame
import sys
import time
import copy
import math

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

x_img = pygame.image.load("image_folder/x.png") # loading the images as python object
y_img = pygame.image.load("image_folder/o.png")

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


def is_terminal(node):
    for i in range(3):
        if node[i][0] == node[i][1] == node[i][2] != "":
            return True
        if node[0][i] == node[1][i] == node[2][i] != "":
            return True

    if node[0][0] == node[1][1] == node[2][2] != "":
        return True
    if node[0][2] == node[1][1] == node[2][0] != "":
        return True

    if all(cell != "" for row in node for cell in row):
        return True

    return False


def minimax(node, depth, maximizingPlayer):
    if depth == 0 or is_terminal(node):
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


def find_best_move():
    best_score = -math.inf
    best_move = None
    for child, move in get_children(grid, "O"):
        score = minimax(child, depth=4, maximizingPlayer=False)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move


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
                        if turn == "O":
                            move = find_best_move()
                            if move:
                                row, col = move
                                grid[row][col] = "O"
                                turn = "X"
                        validation(grid, is_terminal)
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

