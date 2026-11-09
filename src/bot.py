import math
import copy 

class Bot:
    def minimax(self, node, depth, maximizingPlayer, is_terminal):
        if depth == 0 or is_terminal == True:
            return self.heuristic_value(node)

        best_move = None
        player = "O" if maximizingPlayer else "X"

        if maximizingPlayer:
            value = -math.inf
            for child, _ in self.get_children(node, player):
                value = max(value, self.minimax(child, depth - 1, False))
            return value
        else:
            value = math.inf
            for child, _ in self.get_children(node, player):
                value = min(value, self.minimax(child, depth - 1, True))
            return value

    def get_children(self, node, player):
        children = []
        for row in range(3):
            for col in range(3):
                if node[row][col] == "":
                    new_node = copy.deepcopy(node)
                    new_node[row][col] = player
                    children.append((new_node, (row, col)))
        return children
        

    def heuristic_value(self, node):
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

    def find_best_move(self, grid, is_terminal):
        best_score = -math.inf
        best_move = None
        for child, move in self.get_children(grid, "O"):
            depth = 4
            maximizingPlayer = False
            score = self.minimax(child, is_terminal, depth, maximizingPlayer)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move
