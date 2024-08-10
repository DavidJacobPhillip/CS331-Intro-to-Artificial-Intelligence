'''
- Modified By: Santosh Ramesh (April 2022)
- Original Creator: Erich Kramer (April 2017)
- Description: This program implements Othello, a game where you play against an opponent to flip as many tiles as possible in your favor. The "minimax" player uses AI to play.

'''

from Board import Board

x = Board(4, 4)     # this was (15, 15) prior to changing it
x.set_cell( 4, 4, 'x')
x.set_cell( 1, 3, 'B')
x.display()

y = x.cloneBoard()
y.display()
