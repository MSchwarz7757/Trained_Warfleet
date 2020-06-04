import gym
from gym import spaces
import numpy as np
import random as random
from .Spielfeld import Board


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

        # zeichne das Spielfeld am Anfang leer
        self.board.draw_board()
        start = True
        numb_of_ships = 0

        # Spielfeld aufbauen
        while start:
            # frage den Spieler/Agenten nach den positionen
            self.board.place_agent_ship()
            numb_of_ships += 1

            # platziere die Schiffe zufällig -> sollte später durch schiffsklasse ersetzt werden
            r_pos_start = np.random.randint(0, 9)
            r_pos_end = np.random.randint(0, 9)
            r_orientation = np.random.randint(0, 2)
            r_row = np.random.randint(0, 9)

            self.board.place_enemy_ship(r_orientation, r_pos_start, r_pos_end, r_row)
            self.board.draw_board()

            # wenn alle Schiffe platziert wurden
            if numb_of_ships is 1:
                print("Alle Schiffe wurden platziert")
                start = False


    def reset(self):
        """
        Reset the board and return the board as state.
        return:
            board as state of the environment
        """
        #self.board.reset_board(10)
        return self.board

    def check_winner(self):
        """
        check all rows, columns and the diagonals for a winner
        (3 times cross or circle)
        return:
            self.free if no winner can be determined, winner symbol
            otherwise (self.circle or self.cross).
        """
        #if vector
        #return self.free

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

    def opponent_move(self):
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
        shot = self.opponent_move()

        # platziere denn Schuss auf dem Spielfeld und zeichne neu
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
