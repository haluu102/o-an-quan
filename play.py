from state import *

board = Board()
board.initPosition(-1, -1, -1, -1)

board.print()
index = int(input())

while not board.terminalState():
    move = input().split(' ')
    position = int(move[0])
    direction = "right" if "r" in move[1] else "left"
    
    if index % 2 == 0:
        board.playerMove(position, direction)
    else:
        board.opponentMove(position, direction)
        
    index += 1
    board.print()