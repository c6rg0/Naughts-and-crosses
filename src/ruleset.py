import time
from bot import Bot
from gui import Gui

class Ruleset:
    def __init__(self):
        self.turn = 0
        self.score = 0
        self.ending = False
        self.draw = False
        self.winner = ""

    def check_for_ending(self):
        pass

    def validation(self):
        pass

    def progress_game(self):
        pass


class Checkers(Ruleset):
    def __init__(self, Ruleset):
        super().__init__()
        self.turn = "X"
        self.grid = [["" for _ in range(3)] for _ in range(3)]
        self.bot = Bot()

    def check_for_ending(self):
        for i in range(3):
            if self.grid[i][0] == self.grid[i][1] == self.grid[i][2] != "":
                self.ending = True
                return self.ending
            if self.grid[0][i] == self.grid[1][i] == self.grid[2][i] != "":
                self.ending = True
                return self.ending

        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] != "":
            self.ending = True
            return self.ending

        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] != "":
            self.ending = True
            return self.ending

        if all(cell != "" for row in self.grid for cell in row):
            self.ending = True
            return self.ending

        self.ending = False
        return self.ending

    def validation(self):
        for i in range(3):
            if self.grid[i][0] == self.grid[i][1] == self.grid[i][2] != "":
                self.winner = self.grid[i][0]
                self.ending = True
            
            if self.grid[0][i] == self.grid[1][i] == self.grid[2][i] != "":
                self.winner = self.grid[0][i]
                self.ending = True

        if [self.grid[i][i] for i in range(3)].count("X") == 3:
            self.winner = "X"
            self.ending = True

        elif [self.grid[i][i] for i in range(3)].count("O") == 3:
            self.winner = "O"
            self.ending = True

        if [self.grid[i][2-i] for i in range(3)].count("X") == 3:
            self.winner = "X"
            self.ending = True

        elif [self.grid[i][2-i] for i in range(3)].count("O") == 3:
            self.winner = "O"
            self.ending = True

        if all(cell != "" for row in self.grid for cell in row):
            self.draw = True
            self.ending = True

        print(f"Is it a draw? = {self.draw}")
        print(f"Is it the ending? = {self.ending}")
        self.announcment()

    def progress_game(self, row, column):
        if self.ending == True:
            self.announcment()

        if (0 <= row < 3 and 0 <= column < 3):
            if self.grid[row][column] != "":
                print(f"Cell ({row}, {column}) already occupied by {self.grid[row][column]}")

            self.grid[row][column] = self.turn
            self.turn = "O" if self.turn == "X" else "X"

            if self.turn == "O": # TODO: Allow configuring this
                move = self.bot.find_best_move(self.grid, self.ending)
                if move:
                    row, column = move
                    self.grid[row][column] = "O"
                    self.turn = "X"

            self.validation() #TODO: merge with check_for_ending
            print(f"Placed {self.turn} at ({row}, {column})")

    def announcment(self):
        gui = Gui()
        print (self.draw + self.ending)
        if self.ending == True:
            if self.winner == "X" or "O":
                print(f"{self.winner} has won the game.")

            if self.draw == True:
                print("Draw")

            time.sleep(3)
            gui.quit()
