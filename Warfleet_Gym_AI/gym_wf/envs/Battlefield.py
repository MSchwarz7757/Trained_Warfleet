from random import randint
from termcolor import cprint
import random as random
from .Warships import Warships


class Battlefield:

    """
    Class Board generates two (2-Dimensional) Arrays.
    Every Array represents one player's Battlefield for the game.
    The Field at the bottom is the player/agent field.
    The field at the top is the Computer/Enemy field.
    """

    def __init__(self, board_size, draw=False):
        self.board_size = board_size
        self.enemy_board = []
        self.agent_board = []
        self.draw = draw

    def reset_board(self, board_size):
        """
        Fills the boards with 1s.
        Initial state of the game.
        :param board_size: defines the battlefield size
        """
        self.agent_board = []
        self.enemy_board = []
        for x in range(board_size):
            self.enemy_board.append([1] * board_size)
            self.agent_board.append([1] * board_size)
        #self.draw_board()

    '''def choose_random_color(self):
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
    '''

    def draw_board(self):
        #if not self.draw:
        #    return
        """
        The two arrays for each battlefield are printed inside the console.
        """

        # Clear Screen with empty lines
        print('\n' * 40)
        print("--- Computer Battlefield ---")
        for row in self.enemy_board:
            print(row)
        print('\n')
        print("--- Player/Agent Battlefield ---")
        for row in self.agent_board:
            print(row)

    def place_ship(self, choose_board, r_pos_start, r_pos_end, r_orientation, r_row, size):

        """
        A single ship is created and placed on the battlefield.
        Is used for both players to create ships.
        :param choose_board: the board that you want to place the ship in
        :param r_pos_start: start position for the ship
        :param r_pos_end: end position for the ship
        :param r_orientation: vertically or horizontally
        :param r_row: row or column
        :param size: length of the ship
        :return: a single ship object
        """
        start = r_pos_start
        end = r_pos_end
        orientation = r_orientation
        column = r_row
        position_free = True

        # chose the correct board
        if choose_board is 0:
            board = self.enemy_board
        else:
            board = self.agent_board

        #  0 == horizontally
        if orientation == 0:
            # check if position is not outside the battlefield
            start, end = self.move_ship(start, end)
            for row in range(start, end + 1):
                if self.empty_space(column, row, board):
                    position_free = True
                else:
                    # stop the for loop if any of the positions is filled with the ship symbol
                    position_free = False
                    break
            # if position is free then place the ship symbol
            if position_free:
                for row in range(start, end + 1):
                    # draw the ship symbol (in a random color)
                    board[column][row] = Warships.check_size(size)
                # return the ship object with all necessary information
                return Warships(start, end, orientation, column, size)

        # 1 == vertically
        if orientation == 1:
            # check if position is not outside the battlefield
            start, end = self.move_ship(start, end)
            for row in range(start, end + 1):
                if self.empty_space(row, column, board):
                    position_free = True
                else:
                    # stop the for loop if any position is filled with the ship symbol
                    position_free = False
                    break
            # if position is free then place the ship symbol
            if position_free:
                for row in range(start, end + 1):
                    # draw the ship symbol (in a random color)
                    board[row][column] = Warships.check_size(size)
                # return the ship object with all necessary information
                return Warships(start, end, orientation, column, size)

    def empty_space(self, row, column, selected_board):
        """
        check if the position for the ship is empty
        :param selected_board: the agent's or computer's board
        """
        if selected_board[row][column] == 1:
            return True
        else:
            return False

    def move_ship(self, start, end):
        """
        If the end point is not inside the battlefield, then move it towards the middle
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
        """
        This method checks if the given coordinates have already been shot at
        :return: True if board is marked with a shot
        """
        shot_symbol = 0
        if selected_board[y][x] is shot_symbol:
            return True
        else:
            return False

    def place_hit(self, x, y, selected_board):
        """
        This method places a hit marker on the board
        """
        shot_symbol = 0
        if not self.hit(x, y, selected_board):
            selected_board[y][x] = shot_symbol
            return True
        else:
            return False

    # getter
    def get_enemy_board(self):
        return self.enemy_board

    # getter
    def get_agent_board(self):
        return self.agent_board
