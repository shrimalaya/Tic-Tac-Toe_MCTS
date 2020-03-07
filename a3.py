# a3.py

# TIC-TAC-TOE game using monte-carlo-tree-search

import random
import copy

""" Class for Tic-tac-toe game board. Allows for the game to be played.
"""
class TicTacToe:
    def __init__(self):
        self.currentPlayer = 'X'
        self.game_active = True
        self.game = ["-", "-", "-",
                     "-", "-", "-",
                     "-", "-", "-"]
        self.winner = None
        self.computer = 'O'
        self.user = 'X'

    def display_game(self):
        # Added spaces because of difference in tab sizes in Linux VS PyCharm
        print("User is: '" + self.user + "'")
        print(f' 1 | 2 | 3             {self.game[0]} | {self.game[1]} | {self.game[2]}')
        print(f' 4 | 5 | 6             {self.game[3]} | {self.game[4]} | {self.game[5]}')
        print(f' 7 | 8 | 9             {self.game[6]} | {self.game[7]} | {self.game[8]}')
        print("Board Format           Your game")
        print("")

    def set_players(self, userpref):
        self.user = userpref
        if userpref == 'X':
            self.computer = 'O'
        else:
            self.computer = 'X'

    def switch_player(self):
        if self.currentPlayer == 'X':
            self.currentPlayer = 'O'
        else:
            self.currentPlayer = 'X'

    def legal_moves(self):
        indexes = []
        for i in range(9):
            if self.game[i] == "-":
                indexes.append(i)
        return indexes

    def make_move(self, index, currPlayer):
        while self.game[index] != "-":
            print("ERROR: Invalid Move!")
            index = int(input("Enter a position between 1-9: ")) - 1
        self.game[index] = currPlayer

    # Take input and display the game's layout
    def take_input(self):
        self.display_game()
        self.make_move(int(input("Choose a position for your next move: ")) - 1, self.currentPlayer)

    # Check if the game is still running or not
    def check_state(self):
        self.check_for_winner()
        self.check_for_tie()

    # Check to see if somebody has won
    # Check all rows, columns, and diagonals
    def check_for_winner(self):
        row_winner = self.check_rows()
        column_winner = self.check_columns()
        diagonal_winner = self.check_diagonals()

        if row_winner:
            self.winner = row_winner
        elif column_winner:
            self.winner = column_winner
        elif diagonal_winner:
            self.winner = diagonal_winner
        else:
            self.winner = None

    # Check the rows for a win
    # Check if any of the rows have all values same and not empty
    def check_rows(self):
        row1 = self.game[0] == self.game[1] == self.game[2] != "-"
        row2 = self.game[3] == self.game[4] == self.game[5] != "-"
        row3 = self.game[6] == self.game[7] == self.game[8] != "-"
        # If any row has a match, there is a win
        if row1 or row2 or row3:
            self.game_active = False
        # Return the winner
        if row1:
            return self.game[0]
        elif row2:
            return self.game[3]
        elif row3:
            return self.game[6]
        # Or return None if there is no winner
        else:
            return None

    # Check the columns for a win
    # Check if any of the columns have all values same and not empty
    def check_columns(self):
        col1 = self.game[0] == self.game[3] == self.game[6] != "-"
        col2 = self.game[1] == self.game[4] == self.game[7] != "-"
        col3 = self.game[2] == self.game[5] == self.game[8] != "-"
        # If any column has a match, there is a win
        if col1 or col2 or col3:
            self.game_active = False
        # Return the winner
        if col1:
            return self.game[0]
        elif col2:
            return self.game[1]
        elif col3:
            return self.game[2]
        # Or return None if there is no winner
        else:
            return None

    # Check the diagonals for a win
    # Check if any of the diagonals have all values same and not empty
    def check_diagonals(self):
        diagonal1 = self.game[0] == self.game[4] == self.game[8] != "-"
        diagonal2 = self.game[2] == self.game[4] == self.game[6] != "-"
        # If any diagonal has a match, there is a win
        if diagonal1 or diagonal2:
            self.game_active = False
        # Return the winner
        if diagonal1:
            return self.game[0]
        elif diagonal2:
            return self.game[2]
        # Or return None if there is no winner
        else:
            return None

    # Check if there is a tie
    # if the board is full, there's a tie
    def check_for_tie(self):
        if "-" not in self.game:
            self.game_active = False
            return True
        else:
            return False


# End of CLASS
# _________________________________________________________________________

DEPTH = 900 # Depth of Monte Carlo tree search
currGame = TicTacToe() # global variable


"""The following function makes a simulation
    It makes a move based on random selection
    The simulation is processed on a separate game object
        which is a deepCopy of the current game"""
def MCTS_trial(position):
    copyGame = copy.deepcopy(currGame)
    copyGame.make_move(position, copyGame.currentPlayer)
    copyGame.switch_player()
    copyGame.check_state()

    while copyGame.game_active is True:
        legalIndexes = copyGame.legal_moves()
        randMove = random.randint(0, 8)

        while randMove not in legalIndexes:
            randMove = random.randint(0, 8)

        copyGame.make_move(randMove, copyGame.currentPlayer)
        copyGame.check_state()
        copyGame.switch_player()

    if copyGame.computer == 'X':
        if copyGame.winner == 'O':
            return -2
        elif copyGame.winner == 'X':
            return 2
        else:
            return 1
    elif copyGame.computer == 'O':
        if copyGame.winner == 'X':
            return -2
        elif copyGame.winner == 'O':
            return 2
        else:
            return 1


"""Function that calls the Monte Carlo Search function
    This function makes the best move depending on the highest probability
        wins"""
def make_move_MCTS():
    legalIndexes = currGame.legal_moves()
    winCount = {}

    for i in legalIndexes:
        winCount[i] = 0

    for i in legalIndexes:
        for j in range(DEPTH):
            winCount[i] += MCTS_trial(i)

    nextMove = legalIndexes[0]
    nextMoveWins = winCount[nextMove]

    for i in winCount:
        if winCount[i] >= nextMoveWins:
            nextMove = i
            nextMoveWins = winCount[nextMove]

    currGame.make_move(nextMove, currGame.currentPlayer)


"""Function to play game. Uses a global variable for TicTacToe object
    The global variable is useful for the pure MCTS functions"""
def play_game():
    global currGame
    currGame = TicTacToe()
    currGame.display_game()
    currGame.set_players(input("'X' goes first. Do you want to be 'X' or 'O'? ").upper())

    if currGame.user == 'X':
        currGame.take_input()
    else:
        make_move_MCTS()
        currGame.switch_player()
        currGame.take_input()

    while currGame.game_active is True:
        currGame.switch_player()
        make_move_MCTS()
        currGame.display_game()
        currGame.check_state()
        if currGame.game_active is True:
            currGame.switch_player()
            currGame.take_input()
            currGame.display_game()
            currGame.check_state()

    print("----------------Game over-------------------\n")
    if currGame.winner == currGame.user:
        print("User Wins!")
    elif currGame.winner == currGame.computer:
        print("Computer Wins!")
    else:
        print("It's a Tie!")


if __name__ == '__main__':
    play_game()


# End of assignment
#_________________________________________________________________________
