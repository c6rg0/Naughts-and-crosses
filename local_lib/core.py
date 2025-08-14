import math

def test_function(): # Ignore this please
    print("Hello world")

def minimax(node, depth, maximizingPlayer):
    if depth == 0 or is_terminal(node):
        return heuristic_value(node)

    best_move = None
    
    if maximizingPlayer:
        value = -math.inf

        for child in get_children(node):
            value = max(value, minimax(child, depth - 1, False))
        return value

    else:
        value = math.inf

        for child in get_children(node):
            value = min(value, minimax(child, depth - 1, True))
        return value


def is_terminal(node):
    # Check if the node is a terminal node (no children - game over 
    #                                       state)
    pass

def get_children(node):
    #Return the list of child nodes (possible next moves).
    pass

def heuristic_value(node):
    #Evaluate the heuristic value of the node (e.g move/board evaluation_   
    pass

