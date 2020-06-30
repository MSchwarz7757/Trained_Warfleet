import gym
from gym import spaces
import numpy as np
import random as random
from .Battlefield import Battlefield
from .Warships import Warships


class CustomEnv(gym.Env):

    def __init__(self):
        # set to 10 to represent all possible coordinates in a 10x10 2D array
        self.action_space = spaces.MultiDiscrete([10, 10])
        # 3 stands for the amount of possible values at each board position
        self.observation_space = spaces.MultiDiscrete([
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
        ])

        # board size
        self.board = Battlefield(10)
        self.shot = "0"
        self.empty_field = "1"
        self.ship = "2"

        # a shiplist for every player/agent
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
        # define how many ships of each type should be placed
        small_ship = 4
        middle_ship = 2 +small_ship
        big_ship = 2 + middle_ship
        cruiser_ship = 2 + big_ship

        # place a ship and count how many ships are placed
        # Agent ships:
        if self.num_ship_agent < small_ship:
            self.ship_creation(2, 1, self.shiplist_agent)
        elif small_ship <= self.num_ship_agent < middle_ship:
            self.ship_creation(3, 1, self.shiplist_agent)
        elif middle_ship <= self.num_ship_agent < big_ship:
            self.ship_creation(4, 1, self.shiplist_agent)
        elif big_ship <= self.num_ship_agent < cruiser_ship:
            self.ship_creation(5, 1, self.shiplist_agent)

        # place a ship and count how many ships are placed
        # Computer ships:
        if self.num_ship_enemy < small_ship:
            self.ship_creation(2, 0, self.shiplist_enemy)
        elif small_ship <= self.num_ship_enemy < middle_ship:
            self.ship_creation(3, 0, self.shiplist_enemy)
        elif middle_ship <= self.num_ship_enemy < big_ship:
            self.ship_creation(4, 0, self.shiplist_enemy)
        elif big_ship <= self.num_ship_enemy < cruiser_ship:
            self.ship_creation(5, 0, self.shiplist_enemy)

    def ship_creation(self, size, player, shiplist):
        """
        Before a ship can be placed the Agent or Computer choose random position values.
        An Object of the Class: Warships is generated and added to the list.
        :param size: the size of the ship
        :param shiplist: the list that contains the ship-object
        """
        # choose random values
        r_pos_start = np.random.randint(0, 10)
        r_pos_end = r_pos_start + size-1
        r_orientation = np.random.randint(0, 2)
        r_row = np.random.randint(0, 10)

        # generate the object and place it on the battlefield
        if player is 0:
            ship = self.board.place_ship(player, r_pos_start, r_pos_end, r_orientation, r_row, size)
        else:
            ship = self.board.place_ship(player, r_pos_start, r_pos_end, r_orientation, r_row, size)

        # if the object could not be generated (e.g. position not free) -> don't add it to the list
        if ship is not None:
            # choose the shiplist based on player value
            if player is 0:
                # Computer/Enemy
                shiplist.insert(self.num_ship_enemy, ship)
                self.num_ship_enemy += 1
            else:
                # Agent/Player
                shiplist.insert(self.num_ship_agent, ship)
                self.num_ship_agent += 1

    def reset(self):
        """
        Reset the board and return the board as state.
        return:
            board as state of the environment
        """
        self.board.reset_board(10)
        return self.board

    def check_hit(self, player, x, y):

        """
        Detects if a ship was hit by a shot.
        :param player: Computer or Agent
        :param x: X shot position
        :param y: Y shot position
        :return: True if a ship was hit
        """

        # Agent/Player move
        if player == 0 and self.shiplist_enemy:
            for ship in self.shiplist_enemy:
                #  0 == horizontally
                if ship.orientation == 0:
                    # if position is inside a ships position
                    if ship.row_or_col == y and ship.pos_bow <= x <= ship.pos_stern:
                        # reduce shipsize to find out if a ship is destroyed
                        ship.size -= 1
                        if ship.size is 0:
                            # remove the ship is size is zero
                            self.shiplist_enemy.remove(ship)
                        return True

                # 1 == vertically
                elif ship.orientation == 1:
                    # if position is inside a ships position
                    if ship.row_or_col == x and ship.pos_bow <= y <= ship.pos_stern:
                        # reduce shipsize to find out if a ship is destroyed
                        ship.size -= 1
                        if ship.size is 0:
                            # remove the ship is size is zero
                            self.shiplist_enemy.remove(ship)
                            print("Schiff zerstört")
                        return True

        # Computer/Enemy move
        if player == 1 and self.shiplist_agent:
            for ship in self.shiplist_agent:
                #  0 == horizontally
                if ship.orientation == 0:
                    # if position is inside a ships position
                    if ship.row_or_col == y and ship.pos_bow <= x <= ship.pos_stern:
                        # reduce shipsize to find out if a ship is destroyed
                        ship.size -= 1
                        if ship.size is 0:
                            # remove the ship is size is zero
                            self.shiplist_agent.remove(ship)
                        return True

                # 1 == vertically
                elif ship.orientation == 1:
                    # if position is inside a ships position
                    if ship.row_or_col == x and ship.pos_bow <= y <= ship.pos_stern:
                        # reduce shipsize to find out if a ship is destroyed
                        ship.size -= 1
                        if ship.size is 0:
                            # remove the ship is size is zero
                            self.shiplist_agent.remove(ship)
                        return True

    def check_winner(self):
        """
        Check shiplists after every hit.
        return:
            boolean value and the player who has won the match
        """
        if not self.shiplist_enemy:
            print("---------------- End -------------------")
            print("The Agent has won the game")
            done = True
            return done, 1
        elif not self.shiplist_agent:
            print("---------------- End -------------------")
            print("The Computer has won the game")
            done = True
            return done, 2
        else:
            done = False
            return done, 3

    def computer_move(self):
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

    def agent_move(self):
        """
        Set a shot at a random free position of the board.
        return:
            The shot coordinates
        """
        r_shot_X = np.random.randint(0, 10)
        r_shot_Y = np.random.randint(0, 10)

        # for test only
        # r_shot_X = int(input("X:"))
        # r_shot_Y = int(input("Y:"))

        shot = [r_shot_X, r_shot_Y]
        return shot

    def apply_action(self, action, reward):
        """
        Applies the action and changes the board accordingly.
        """
        # input to go through all the steps -> for tests
        # input("Weiter....")

        # Agent move
        shot = self.computer_move()

        # first check if the position is not already shot then try to place the shot on the battlefield
        free_agent_field = self.board.place_hit(shot[0], shot[1], self.board.agent_board)
        free_enemy_field = self.board.place_hit(action[0], action[1], self.board.enemy_board)
        self.board.draw_board()

        # if position is free then check if a ship is hit
        if free_enemy_field:
            if self.check_hit(0, action[0], action[1]):
                # if agent hit the target
                reward += 1
                self.count_hit += 1
                self.hitlist_agent.insert(self.count_hit, [action[0], action[1]])
        if free_agent_field:
            self.check_hit(1, shot[0], shot[1])
        return reward

    def step(self, action):
        """
        Applies the action and changes the board accordingly.
        If the start value is True, then the ships will be placed.
        After the ships are placed every Player alternately shoots.
        The shot coordinates are checked and if the position is free,
        the shot is placed on the battlefield.
        If a ship is hit by a shot, then the reward is increased by 1.
        When a player has lost all of his ships, a winner is determined.
        A list contains all the shot coordinates made by the agent.
        If the agent wins a match the reward is increased by 10.
        action:
            a board position to set the shot ("o") (e.g. [x, y])
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
        reward += self.apply_action(action, reward)

        # check winner by shiplist
        done, player = self.check_winner()
        if player == 1:
            # if agent is the winner
            reward += 10
            return self.board.get_enemy_board(), reward, done, {}

        return self.board.get_enemy_board(), reward, done, {}

    # board wird gezeichnet
    def render(self, mode="human", close=False):
        print(self.board.reset_board(10))
