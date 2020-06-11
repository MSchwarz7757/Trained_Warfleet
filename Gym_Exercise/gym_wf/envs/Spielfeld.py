from random import randint
from termcolor import cprint
import random as random


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

    def choose_random_color(self):
        color_list = []
        PURPLE = '\033[95m'
        color_list.append(PURPLE)
        CYAN = '\033[96m'
        color_list.append(CYAN)
        DARKCYAN = '\033[36m'
        color_list.append(DARKCYAN)
        BLUE = '\033[94m'
        color_list.append(BLUE)
        GREEN = '\033[92m'
        color_list.append(GREEN)
        YELLOW = '\033[93m'
        color_list.append(YELLOW)
        RED = '\033[91m'
        color_list.append(RED)

        return str(random.choice(color_list))

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
        column = ship.row_or_col
        print("Ship start: {}".format(ship.pos_bow))
        print("Ship End: {}".format(ship.pos_stern))

        if orientation == 0:
            if self.empty_space(start, end, column, orientation, self.enemy_board):
                start, end = self.move_ship(start, end)
                color = self.choose_random_color()
                for row in range(start, end + 1):
                    self.enemy_board[column][row] = color+"x"

        if orientation == 1:
            if self.empty_space(start, end, column, orientation, self.enemy_board):
                start, end = self.move_ship(start, end)
                color = self.choose_random_color()
                for row in range(start, end + 1):
                    self.enemy_board[row][column] = color+"x"

    def place_agent_ship(self, ship):
        '''orientation = int(input("Waagrecht(0) oder Senkrecht(1)? : "))
        # minus 1 weil der array immer bei 0 anfängt
        column = int(input("Welche Reihe/Spalte: "))
        start = int(input("Anfang Shiff: "))
        #end = int(input("Ende Shiff: "))'''

        start = ship.pos_bow
        end = ship.pos_stern
        orientation = ship.orientation
        column = ship.row_or_col
        print("Ship start: {}".format(ship.pos_bow))
        print("Ship End: {}".format(ship.pos_stern))

        #waagerecht
        if orientation == 0:
            if self.empty_space(start, end, column, orientation, self.agent_board):
                start, end = self.move_ship(start, end)
                color = self.choose_random_color()
                for row in range(start, end + 1):
                    self.agent_board[column][row] = color+"x"
            else:
                print("kein platz")

        #senkrecht
        if orientation == 1:
            if self.empty_space(start, end, column, orientation, self.agent_board):
                start, end = self.move_ship(start, end)
                color = self.choose_random_color()
                for row in range(start, end + 1):
                    self.agent_board[row][column] = color+"x"
                else:
                    print("kein platz")

        #return start, start + size, orientation, column, size

    def empty_space(self, start, end, column, orientation, selected_board):
        #print(selected_board[start][end] == " ")
        for pos in range(start, end+1):
            if orientation == 0:
                if selected_board[column][pos] == " ":
                    return True
                else:
                    return False

            if orientation == 1:
                if selected_board[pos][column] == " ":
                    return True
                else:
                    return False

    def move_ship(self, start, end):
        if end > 9:
            end = end-9
            start = start - end
            return start, end
        else:
            return start, end

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

