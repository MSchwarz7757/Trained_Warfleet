import gym
from gym import spaces
import numpy as np
import random as random
from .Spielfeld import Board
from .Warships import Warships


class CustomEnv(gym.Env):

    def __init__(self):
        # board position to set a cross (can be 0, 1, 2 in each dimension)
        self.action_space = spaces.MultiDiscrete([3, 3]) # wo wird das kreuz gesetzt?
        # board with circles and crosses  (can be 0, 1, 2 in each dimension)
        self.observation_space = spaces.MultiDiscrete([
            [3, 3, 3],
            [3, 3, 3],
            [3, 3, 3]])

        self.board = Board(10)
        self.free = " "
        self.ship = "x"
        self.hit = "O"

        self.shiplist_enemy = []
        self.shiplist_agent = []

        # zeichne das Spielfeld am Anfang leer
        self.board.draw_board()
        start = True
        self.num_ship = 0

        # Spielfeld aufbauen
        while start:
            self.place_ships()
            # wenn alle Schiffe platziert wurden
            if self.num_ship == 3:
                print("Alle Schiffe wurden platziert")
                start = False

        #self.combat()

    def place_ships(self):
        # frage den Spieler/Agenten nach den Positionen
        # self.board.place_agent_ship()

        # place 4 subs for each player
        if self.num_ship <= 8:
            r_pos_start, r_pos_end, r_orientation, r_row, size = self.board.place_agent_ship(2)
            self.shiplist_agent.insert(self.num_ship, Warships(r_pos_start, r_pos_end, r_orientation, r_row, size))
            self.enemy_placement(2)
            self.board.draw_board()
            self.num_ship += 1

        # place 3 destroyers for each player
        if 8 <= self.num_ship <= 14:
            r_pos_start, r_pos_end, r_orientation, r_row, size = self.board.place_agent_ship(3)
            self.shiplist_agent.insert(self.num_ship, Warships(r_pos_start, r_pos_end, r_orientation, r_row, size))
            self.enemy_placement(3)
            self.board.draw_board()
            self.num_ship += 1

        # place 2 cruisers for each player
        if 14 <= self.num_ship <= 18:
            r_pos_start, r_pos_end, r_orientation, r_row, size = self.board.place_agent_ship(4)
            self.shiplist_agent.insert(self.num_ship, Warships(r_pos_start, r_pos_end, r_orientation, r_row, size))
            self.enemy_placement(4)
            self.board.draw_board()
            self.num_ship += 1

        # place 1 battleship for each player
        if 18 <= self.num_ship <= 20:
            r_pos_start, r_pos_end, r_orientation, r_row, size = self.board.place_agent_ship(5)
            self.shiplist_agent.insert(self.num_ship, Warships(r_pos_start, r_pos_end, r_orientation, r_row, size))
            self.enemy_placement(5)
            self.board.draw_board()
            self.num_ship += 1

    def enemy_placement(self, size):
        r_pos_start = np.random.randint(0, 9)
        r_pos_end = r_pos_start + size-1
        r_orientation = np.random.randint(0, 2)
        r_row = np.random.randint(0, 9)

        self.shiplist_enemy.insert(self.num_ship, Warships(r_pos_start, r_pos_end, r_orientation, r_row, size))
        self.board.place_enemy_ship(self.shiplist_enemy[self.num_ship])

    def reset(self):
        """
        Reset the board and return the board as state.
        return:
            board as state of the environment
        """
        #self.board.reset_board(10)
        return self.board

    def check_hit(self, player, col, row):
        #Zug Agent
        if player == 0:
            for index in self.shiplist_enemy:
                #waagerecht
                print("test1 {}".format(index))
                if index.orientation == 0:
                    print("test2 {}".format(index.row_or_col))
                    print("test2 {}".format(row))
                    if index.row_or_col == row and index.pos_bow <= col <= index.pos_stern:
                    #if index.pos_bow <= row <= index.pos_stern:
                        index.size -= 1
                        print(index.size)
                        return True
                    else:
                        print("test3")
                        continue

                #senkrecht
                elif index.orientation == 1:
                    print("test4")
                    if index.row_or_col == col and index.pos_bow <= row <= index.pos_stern:
                        index.size -= 1
                        print(index.size)
                        return True
                    else:
                        print("test5")
                        continue
        else:
            print("test6")

        # Zug Gegner
        if player ==1:
            for index in self.shiplist_agent:
                # waagerecht
                if index.orientation == 0:

                    if index.row_or_col == row and index.pos_bow <= col <= index.pos_stern:
                        index.size -= 1
                        print("index.size")
                        print(index.size)
                        return True
                    else:
                        return False

                # senkrecht
                elif index.orientation == 1:
                    if index.row_or_col == col and index.pos_bow <= row <= index.pos_stern:
                        index.size -= 1
                        print(index.size)
                        return True
                    else:
                        return False

        else:
            print("test2")




    def check_winner(self):
        """
        Check shiplists after every hit.
        return:
            0 - no winner
            1 - current player is winner
        """
        if self.shiplist_enemy:
            return 0
        elif self.shiplist_agent:
            return 0
        else:
            return 1


    def sample(self):
        """
        Select a random position an try to hit the agent ships
        return:
            position which should be attacked
        """
        r_shot_X = np.random.randint(0, 9)
        r_shot_Y = np.random.randint(0, 9)

        shot = [r_shot_X, r_shot_Y]
        return shot

    def agent_move(self):
        """
        Set a circle at a random free position of the board.
        return:
            True, if board is completely filled.
            False, otherwise.
        """
        x = int(input("Schuss X Koordinate: "))
        y = int(input("Schuss Y Koordinate: "))
        shot = [x,y]
        return shot


    def compute_reward(self, winner):
        """
        winner:
            The winner symbol (self.free, self.circle, self.cross)
        return:
            Reward != self.free if winner is circle or cross and if game is
            over.
            Done, if winner is != self.free
        """
        """reward = 0
        done = False
        return reward, done"""

    def apply_action(self, action):
        """
        Applies the action and changes the board accordingly.
        """
        pass

    def step(self, action):
        """
        Applies the action and changes the board accordingly. A circle is set
        by the environment. The environment is done, if a winner is
        determinable. If the circle player wins the game a reward of -1 is
        returned. If the cross player wins the game a reward of 1 is
        returned. The environment returns 0 otherwise.
        action:
            a board position to set the cross (e.g. [x, y])
        return:
            state (board), reward, done, info
        """
        # check if action is valid board position
        reward = 0
        done = False
        count_shots = 0

        if action[0] > 9 or action[0] < 0:
            # do not change board
           return self.board, reward, done, {}

        # Agent soll schießen
        shot = self.agent_move()

        # platziere denn Schuss auf dem Spielfeld und zeichne neu
        self.check_hit(0, shot[0], shot[1])
        self.board.place_hit(action[0], action[1], self.board.agent_board)
        self.board.place_hit(shot[0], shot[1], self.board.enemy_board)
        self.board.draw_board()
        count_shots += 1

        # in der if abfrage ist noch ein fehler drinn !
        if self.board.enemy_board[shot[0]][shot[1]] is self.hit:
            # do not change board
            print("Hier war schon ein schuss")
            # return self.board, reward, done, {}

        if self.board.agent_board[action[0]][action[1]] is self.ship:
            print("Eins deiner Schiffe wurde getroffen")

        if self.board.enemy_board[shot[0]][shot[1]] is self.ship:
            print("Du hast ein Schiff getroffen")

        return self.board, reward, done, {}

    # board wird gezeichnet
    def render(self, mode="human", close=False):
        print(self.board)
