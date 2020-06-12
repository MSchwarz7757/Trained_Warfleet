from random import randint
from termcolor import cprint
import random as random
from .Warships import Warships


class Board:

    """
    Class Board generates two (2-Dimensional) Arrays.
    Every Array is a Battlefield for the game.
    The Field at the bottom is the player/agent field
    The field at the toop is the Computer/Enemy field
    """

    def __init__(self, board_size):
        self.board_size = board_size
        self.enemy_board = []
        self.agent_board = []

        self.reset_board(board_size)

    def reset_board(self, board_size):
        """
        creates two array with empty strings inside.
        Start position for the game.
        :param board_size: defines which size the the battlefield should have
        """
        for x in range(board_size):
            self.enemy_board.append([" "] * board_size)
            self.agent_board.append([" "] * board_size)

    def choose_random_color(self):
        """
        Creates a list with colors and gives a random color back.
        Is used to give every ship a different color.
        """
        color_list = []
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        pink = '\033[95m'
        lightcyan = '\033[96m'

        color_list.append(black)
        color_list.append(red)
        color_list.append(green)
        color_list.append(orange)
        color_list.append(purple)
        color_list.append(cyan)
        color_list.append(lightgrey)
        color_list.append(darkgrey)
        color_list.append(lightred)
        color_list.append(lightgreen)
        color_list.append(yellow)
        color_list.append(pink)
        color_list.append(lightcyan)

        return str(random.choice(color_list))

    def draw_board(self):
        """
        The two arrays for eacht battlefield is printed inside the console.
        Some colors and numbers for the axis are added
        """

        # colors for the battlefield
        background = '\x1b[2;31;0m'
        x_axis_color = '\x1b[1;30;0m'
        y_axis_color = '\x1b[1;30;0m'
        terminal = '\x1b[0;0;0m'

        # just some space to get a nice output
        space_btw_ships = " "
        space_btw_axis = " "
        axis_numbers = " 0 1 2 3 4 5 6 7 8 9"

        # x = counter for the y a_axis
        x = 0
        # Clear Screen with empty lines
        print('\n' * 40)
        print("--- Computer Spielfeld ---")
        print(x_axis_color + space_btw_axis + axis_numbers + terminal) # x_axis
        for row in self.enemy_board:
            string = y_axis_color + str(x) + background+space_btw_axis + space_btw_ships.join(row) # y_axis + battelfield
            cprint(string, 'red', 'on_blue')
            x += 1
        print('\n')
        print("--- Spieler/Agent Spielfeld ---")
        # x = counter for the y a_axis
        x = 0
        print(x_axis_color + space_btw_axis + axis_numbers + terminal) # x_axis
        for row in self.agent_board:
            string = y_axis_color + str(x) + background + space_btw_axis + space_btw_ships.join(row) # y_axis + battelfield
            cprint(string, 'white', 'on_blue')
            x += 1

    def place_enemy_ship(self, r_pos_start, r_pos_end, r_orientation, r_row, size):

        start = r_pos_start
        end = r_pos_end
        orientation = r_orientation
        column = r_row
        position_free = True

        #  0 == horizontally
        if orientation == 0:
            start, end = self.move_ship(start, end)
            for row in range(start, end + 1):
                if self.empty_space(column, row, self.enemy_board):
                    position_free = True
                else:
                    # stop the for loop if any position is filled with "x"
                    position_free = False
                    break
            # if position is free then place the ship symbol
            if position_free:
                for row in range(start, end + 1):
                    # draw the shipsymbol whith a random color and the symbol
                    self.enemy_board[column][row] = self.choose_random_color() + Warships.check_size(size)
                # return the ship object with all necessary information
                return Warships(start, end, orientation, column, size)

        # 1 == vertically
        if orientation == 1:
            start, end = self.move_ship(start, end)
            for row in range(start, end + 1):
                if self.empty_space(row, column, self.enemy_board):
                    position_free = True
                else:
                    # stop the for loop if any position is filled with "x"
                    position_free = False
                    break
            # if position is free then place the ship symbol
            if position_free:
                for row in range(start, end + 1):
                    # draw the shipsymbol whith a random color and the symbol
                    self.enemy_board[row][column] = self.choose_random_color() + Warships.check_size(size)
                # return the ship object with all necessary information
                return Warships(start, end, orientation, column, size)

    def place_agent_ship(self, r_pos_start, r_pos_end, r_orientation, r_row, size):

        start = r_pos_start
        end = r_pos_end
        orientation = r_orientation
        column = r_row
        position_free = True

        #  0 == horizontally
        if orientation == 0:
            start, end = self.move_ship(start, end)
            color = self.choose_random_color()
            for row in range(start, end + 1):
                if self.empty_space(column, row, self.agent_board):
                    position_free = True
                else:
                    position_free = False
                    break
            if position_free:
                for row in range(start, end + 1):
                    self.agent_board[column][row] = color + Warships.check_size(size)
                return Warships(start, end, orientation, column, size)

        # 1 == vertically
        if orientation == 1:
            start, end = self.move_ship(start, end)
            color = self.choose_random_color()
            for row in range(start, end + 1):
                if self.empty_space(row, column, self.agent_board):
                    position_free = True
                else:
                    position_free = False
                    # stop the for loop if any position is filled with "x"
                    break
            if position_free:
                for row in range(start, end + 1):
                    self.agent_board[row][column] = color + Warships.check_size(size)
                return Warships(start, end, orientation, column, size)

    def empty_space(self, row, column, selected_board):
        """
        check if the position for the ship is empty
        :param selected_board: the agent or computer board
        """
        if selected_board[row][column] == " ":
            return True
        else:
            return False

    def move_ship(self, start, end):
        """
        If the end is not inside the battlefield, then move it to the middle
        :param start: ship start point
        :param end: ship end point
        :return: new position
        """
        if end > 9:
            end = end - 5 # move the ship 5 fields to the right side
            start = start - 5
            return start, end
        else:
            return start, end

    def hit(self, x, y, selected_board):
        '''
        This method checks if the coordinates have already been shot
        :return: True if board is marked with a shot
        '''
        string1 = "O"
        print(selected_board[y][x])
        print(string1)
        if selected_board[y][x] is string1:
            print("doppelter schuss")
            return True
        else:
            return False

    def place_hit(self, x, y, selected_board):
        '''
        This method is to place the hit on the board
        '''
        if not self.hit(x, y, selected_board):
            print("Gezeichnet")
            selected_board[y][x] = "O"
            return True
        else:
            return False

    # getter
    def get_enemy_board(self):
        return self.enemy_board
    # getter
    def get_agent_board(self):
        return self.agent_board

