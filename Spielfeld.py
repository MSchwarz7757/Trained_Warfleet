from random import randint
from termcolor import cprint

board = []
board_size = 8

for x in range(board_size):
    board.append([" "] * board_size)

def print_board(board):
    for row in board:
        cprint(row, 'yellow', 'on_blue')

print("Eine neue Runde statet!")
print_board(board)

def random_ship_row_placement(board):
    return randint(0, len(board) - 1)

def random_ship_col_placement(board):
    return randint(0, len(board[0]) - 1)

ship_row = random_ship_row_placement(board)
ship_col = random_ship_col_placement(board)

for turn in range(4):
    guess_row = int(input("Guess Row:"))
    guess_col = int(input("Guess Col:"))

    if guess_row == ship_row and guess_col == ship_col:
        print("Das Schiff wurde getroffen!")
        break
    else:
        if turn == 3:
            print("Spiel vorbei")
        elif (guess_row < 0 or guess_row > 8) or (guess_col < 0 or guess_col > 8):
            print("Das ist auserhalb des Spielfeldes")
        elif(board[guess_row][guess_col] == "X"):
            print("Hier wurde bereits hingeschossen")
        else:
            print("Du hast nicht getroffen!")
            board[guess_row - 1][guess_col - 1] = "X"
        print("Turn: {}".format(turn + 1))
    print_board(board)