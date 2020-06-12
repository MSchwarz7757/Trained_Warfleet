import gym
from gym import spaces
import numpy as np
import random as random
from .Battlefield import Board
from .Warships import Warships


class CustomEnv(gym.Env):

    def __init__(self):
        # board position to set a cross (can be 0, 1, 2 in each dimension)
        self.action_space = spaces.MultiDiscrete([3, 3])
        # board with circles and crosses  (can be 0, 1, 2 in each dimension)
        self.observation_space = spaces.MultiDiscrete([
            [3, 3, 3],
            [3, 3, 3],
            [3, 3, 3]])

        self.board = Board(10)
        self.free = " "
        self.ship = "x"
        self.hit = "O"

        # a shiplis for every player/agent
        self.shiplist_enemy = []
        self.shiplist_agent = []

        # to collect all the hits made by the agent
        self.hitlist_agent = []
        self.count_hit = 0

        # draw an empty board without ships
        self.board.draw_board()
        self.start = True

        # counter for amount of ships
        self.num_ship_agent = 0
        self.num_ship_enemy = 0

    def place_ships(self):

        """
        A ship is placed based on the shipsize.
        Every ship is counted and added to a list
        """
        # define how many shiptypes should be placed
        small_ship = 4
        middle_ship = 2 +small_ship
        big_ship = 2 + middle_ship
        cruiser_ship = 2 + big_ship

        # place a ship and count how many ships are placed
        # Agent ships:
        if self.num_ship_agent < small_ship:
            self.agent_placement(2, self.shiplist_agent)
        elif small_ship <= self.num_ship_agent < middle_ship:
            self.agent_placement(3, self.shiplist_agent)
        elif middle_ship <= self.num_ship_agent < big_ship:
            self.agent_placement(4, self.shiplist_agent)
        elif big_ship <= self.num_ship_agent < cruiser_ship:
            self.agent_placement(5, self.shiplist_agent)

        # place a ship and count how many ships are placed
        # Computer ships:
        if self.num_ship_enemy < small_ship:
            self.enemy_placement(2, self.shiplist_enemy)
        elif small_ship <= self.num_ship_enemy < middle_ship:
            self.enemy_placement(3, self.shiplist_enemy)
        elif middle_ship <= self.num_ship_enemy < big_ship:
            self.enemy_placement(4, self.shiplist_enemy)
        elif big_ship <= self.num_ship_enemy < cruiser_ship:
            self.enemy_placement(5, self.shiplist_enemy)

    def enemy_placement(self, size, shiplist):
        """
        Before a ship can be placed the Agent or Computer choose some random positon values.
        A Object by Class: Warships is generated and added to the list.
        :param size: the size of the ship
        :param shiplist: the list that contains the ship-object
        """
        # choose random values
        r_pos_start = np.random.randint(0, 10)
        r_pos_end = r_pos_start + size-1
        r_orientation = np.random.randint(0, 2)
        r_row = np.random.randint(0, 10)

        # generate the object and place it on the battlefield
        ship = self.board.place_enemy_ship(r_pos_start, r_pos_end, r_orientation, r_row, size)

        # if the object could not be generated (e.g. position not free) -> dont add it to the list
        if ship is not None:
            shiplist.insert(self.num_ship_enemy, ship)
            self.num_ship_enemy += 1

    def agent_placement(self, size, shiplist):
        """
        Before a ship can be placed the Agent or Computer choose some random positon values.
        A Object by Class: Warships is generated and added to the list.
        :param size: the size of the ship
        :param shiplist: the list that contains the ship-object
        """
        # choose random values
        r_pos_start = np.random.randint(0, 10)
        r_pos_end = r_pos_start + size - 1
        r_orientation = np.random.randint(0, 2)
        r_row = np.random.randint(0, 10)

        # generate the object and place it on the battlefield
        ship = self.board.place_agent_ship(r_pos_start, r_pos_end, r_orientation, r_row, size)
        if ship is not None:
            shiplist.insert(self.num_ship_agent, ship)
            self.num_ship_agent += 1

    def reset(self):
        """
        Reset the board and return the board as state.
        return:
            board as state of the environment
        """
        #self.board.reset_board(10)
        return self.board

    def check_hit(self, player, x, y):

        """
        Detects if a ship is hit by a shot.
        :param player: Computer or Agent
        :param x: X shot position
        :param y: Y shot position
        :return: True if a ship is hit
        """

        # Agent/Player move
        if player == 0 and self.shiplist_enemy:
            for index in self.shiplist_enemy:
                #  0 == horizontally
                if index.orientation == 0:
                    # if position is inside a ships position
                    if index.row_or_col == y and index.pos_bow <= x <= index.pos_stern:
                        # reduce shipsize to find out if a ship is destroyed
                        index.size -= 1
                        if index.size is 0:
                            # remove the ship is size is zero
                            self.shiplist_enemy.remove(index)
                            print("Schiff zerstört")
                        return True

                # 1 == vertically
                elif index.orientation == 1:
                    # if position is inside a ships position
                    if index.row_or_col == x and index.pos_bow <= y <= index.pos_stern:
                        # reduce shipsize to find out if a ship is destroyed
                        index.size -= 1
                        if index.size is 0:
                            # remove the ship is size is zero
                            self.shiplist_enemy.remove(index)
                            print("Schiff zerstört")
                        return True

        # Computer/Enemy move
        if player == 1 and self.shiplist_agent:
            for index in self.shiplist_agent:
                #  0 == horizontally
                if index.orientation == 0:
                    # if position is inside a ships position
                    if index.row_or_col == y and index.pos_bow <= x <= index.pos_stern:
                        # reduce shipsize to find out if a ship is destroyed
                        index.size -= 1
                        if index.size is 0:
                            # remove the ship is size is zero
                            self.shiplist_agent.remove(index)
                            print("Schiff zerstört")
                        return True

                # 1 == vertically
                elif index.orientation == 1:
                    # if position is inside a ships position
                    if index.row_or_col == x and index.pos_bow <= y <= index.pos_stern:
                        # reduce shipsize to find out if a ship is destroyed
                        index.size -= 1
                        if index.size is 0:
                            # remove the ship is size is zero
                            self.shiplist_agent.remove(index)
                            print("Schiff zerstört")
                        return True

    def check_winner(self):
        """
        Check shiplists after every hit.
        return:
            boolean value
        """
        if not self.shiplist_enemy:
            print("---------------- Ende -------------------")
            print("Der Agent hat gewonnen")
            return True
        elif not self.shiplist_agent:
            print("---------------- Ende -------------------")
            print("Der Computer hat gewonnen")
            return True
        else:
            return False

    def sample(self):
        """
        Select a random position an try to hit the agent ships
        return:
            position which should be attacked
        """
        r_shot_X = np.random.randint(0, 10)
        r_shot_Y = np.random.randint(0, 10)

        # check if action is valid board position
        shot = [r_shot_X, r_shot_Y]
        return shot

    '''def check_shot_postion(self, x, y):
        if x > 10 or x < 0 or y > 10 or y < 0:
            # chose new values
            x = np.random.randint(0, 10)
            y = np.random.randint(0, 10)
            return [x, y]
        else:
            return [x, y]'''

    def agent_move(self):
        """
        Set a circle at a random free position of the board.
        return:
            True, if board is completely filled.
            False, otherwise.
        """
        r_shot_X = np.random.randint(0, 10)
        r_shot_Y = np.random.randint(0, 10)

        # for test only
        # r_shot_X = int(input("X:"))
        # r_shot_Y = int(input("Y:"))

        shot = [r_shot_X, r_shot_Y]
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

        # creates the ships and add them to the battlefield
        while self.start:
            # place a specific number for every battlefield
            if self.num_ship_agent >= 10 and self.num_ship_enemy >= 10:
                if self.num_ship_agent == len(self.shiplist_agent):
                    self.start = False
            self.place_ships()
            self.board.draw_board()
        reward = 0
        done = False

        # input to go through all the steps -> for tests
        #input("Weiter....")

        # Agent move
        shot = self.agent_move()

        # first check if the position is not alreasy shot and try to place the shot on the Battlefield
        free_agent = self.board.place_hit(action[0], action[1], self.board.agent_board)
        free_enemy = self.board.place_hit(shot[0], shot[1], self.board.enemy_board)
        self.board.draw_board()

        # if position is free then check if a ship is hit
        if free_enemy:
            if self.check_hit(0, shot[0], shot[1]):
                reward += 1
                self.count_hit += 1
                self.hitlist_agent.insert(self.count_hit, [shot[0], shot[1]])
        if free_agent:
            self.check_hit(1, action[0], action[1])

        # check winner by shiplist
        if self.check_winner():
            done = True

        return self.board, reward, done, {}

    # board wird gezeichnet
    def render(self, mode="human", close=False):
        print(self.board)
