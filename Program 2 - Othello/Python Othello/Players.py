'''
- Modified By: Santosh Ramesh (April 2022)
- Original Creator: Erich Kramer (April 2017)
- Description: This program implements Othello, a game where you play against an opponent to flip as many tiles as possible in your favor. The "minimax" player uses AI to play.

'''

import random
import copy

class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    #PYTHON: use obj.symbol instead
    def get_symbol(self):
        return self.symbol
    
    #parent get_move should not be called
    def get_move(self, board):
        raise NotImplementedError()

class HumanPlayer(Player):
    def __init__(self, symbol):
        Player.__init__(self, symbol)

    def clone(self):
        return HumanPlayer(self.symbol)
        
    #PYTHON: return tuple instead of change reference as in C++
    def get_move(self, board):
        col = int(input("Enter col:"))
        row = int(input("Enter row:"))
        return  (col, row)

class MinimaxPlayer(Player):
    def __init__(self, symbol):
        self.states = []
        Player.__init__(self, symbol)
        if symbol == 'X':
            self.oppSym = 'O'
        else:
            self.oppSym = 'X'
    
    # Remove and modify with a minimax algorithm here
    def get_move(self, board):
        (col, row) = self.minimax_decision(board)
        return (col, row)

    # minimax function
    def minimax_decision(self, board):
        maxes = []
        self.states = self.successors(board, self.symbol)
        action = (0, 0)
        max = -99999
        current = 0

        # loops through the possible decisions to be made, holding the highest one
        for state in self.states:
            duplicate = copy.deepcopy(board)
            (col, row) = state
            duplicate.play_move(col,row, self.symbol)
            current = self.min_value(duplicate, state, self.symbol)
            maxes.append((state, current))          # this list "maxes" is simply used for error checking; can be printed out for debugging purposes
            if current > max:
                max = current
                action = state
        return action
    
    # max function (used in minimax to return max utility value)
    def max_value(self, board, state, curr_symbol):
        states = []
        
        # changes the symbol for the next move
        if curr_symbol == 'X':
            symbol = 'O'
        else:
            symbol = 'X'

        if not board.has_legal_moves_remaining(symbol):
            return self.utility(board)
        
        # Generates all of the successor states
        v = -99999
        states = self.successors(board, symbol)
        for state in states:
            duplicate = copy.deepcopy(board)
            (col, row) = state
            duplicate.play_move(col,row,symbol)
            v = max(v, self.min_value(duplicate, state, symbol))
        return v

    # min function (used in minimax to return min utility value)
    def min_value(self, board, state, curr_symbol):
        states = []

        # changes the symbol for the next move
        if curr_symbol == 'X':
            symbol = 'O'
        else:
            symbol = 'X'

        if not board.has_legal_moves_remaining(symbol):
            return self.utility(board)
        
        # Generates all of the successor states
        v = 99999
        states = self.successors(board, symbol)
        for state in states:
            duplicate = copy.deepcopy(board)
            (col, row) = state
            duplicate.play_move(col,row,symbol)
            v = min(v, self.max_value(duplicate, state, symbol))
        return v

    # successor function
    def successors(self, board, symbol):
        states = []

        # Goes through a for loop of all the rows and columns and uses the "is_legal_move" function to check for legality
        for c in range (0, board.cols):
            for r in range (0, board.rows):
                if(board.is_legal_move(c, r, symbol)):
                    states.append((c, r))

        return states

    # utility function: prints out a positive or negative value for the minimax evaluation
    def utility(self, board):
        evaluation = 0
        player_one = 0
        player_two = 0

        if self.symbol == 'X':
            opposite = 'O'
        else:
            opposite = 'X'

        # Adds up the number of "X's" on the board
        for c in range (0, board.cols):
            for r in range (0, board.rows):
                if board.grid[c][r] == self.symbol:
                    player_one+=1

        # Adds up the number of ")'s" on the board
        for c in range (0, board.cols):
            for r in range (0, board.rows):
                if board.grid[c][r] == opposite:
                    player_two+=1

        # Subtracts the score of player two and player one to evaluate
        evaluation = player_two - player_one

        return evaluation