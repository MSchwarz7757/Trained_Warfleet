from random import randint
from termcolor import cprint


class Board:
    def __init__(self, board_size):
        self.board_size = board_size
        self.enemy_board = []
        self.agent_board = []

        self.reset_board(board_size)

    def reset_board(self, board_size):
        for x in range(board_size):
            self.enemy_board.append([" "] * board_size)
            self.agent_board.append([" "] * board_size)

    def draw_board(self):
        # Clear Screen: screen wird nur verschoben aber reicht auch zur übersicht
        print('\n' * 40)
        print("Gegnerisches Spielfeld")
        x = 0
        print("  "+" 0 1 2 3 4 5 6 7 8 9") # Obere leiste
        for row in self.enemy_board:
            string = str(x)+"  "+" ".join(row)
            cprint('\x1b[2;31;44m'+string, 'red', 'on_blue')
            x += 1
        print("Dein Spielfeld")
        x = 0
        print("  "+" 0 1 2 3 4 5 6 7 8 9") # Obere leiste
        for row in self.agent_board:
            string = str(x) + "  " + " ".join(row)
            cprint('\x1b[3;30;44m'+string, 'white', 'on_blue')
            x += 1

    # hier soll überprüft werden das die schiffe nicht übereinander liegen
    def check_double_position(self):
        pass

    def place_enemy_ship(self, ship):

        start = ship.pos_bow
        end = ship.pos_stern
        orientation = ship.orientation
        column = ship.row

        # tauschen der zahlen bei falscher eingabe
        if start >= end:
            temp = end
            end = start
            start = temp

        if orientation == 0:
            for row in range(start, end + 1):
                self.enemy_board[column][row] = "x"

        if orientation == 1:
            for row in range(start, end + 1):
                self.enemy_board[row][column] = "x"

    def place_agent_ship(self, size):
        orientation = int(input("Waagrecht(0) oder Senkrecht(1)? : "))
        # minus 1 weil der array immer bei 0 anfängt
        column = int(input("Welche Reihe/Spalte: "))
        start = int(input("Anfang Shiff: "))
        end = int(input("Ende Shiff: "))

        # tauschen der zahlen bei falscher eingabe
        if start >= end:
            temp = end
            end = start
            start = temp

        #waagrecht
        if orientation == 0:
            for row in range(start, end + 1):
                self.agent_board[column][row] = "x"

        #senkrecht
        if orientation == 1:
            for row in range(start, end + 1):
                self.agent_board[row][column] = "x"

        return start, end , orientation, column, size

    def empty_space(self, x, y, selected_board):
        if selected_board[y][x] == " ":
            return True
        else:
            return False

    def hit(self, x, y, selected_board):
        if selected_board[y][x] == "O":
            return True
        else:
            return False

    def place_hit(self, x, y, selected_board):
        if not self.hit(x, y, selected_board):
            selected_board[y][x] = "O"

    def get_enemy_board(self):
        return self.enemy_board

    def get_agent_board(self):
        return self.agent_board

