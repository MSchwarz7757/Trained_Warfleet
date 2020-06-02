import gym
from gym import spaces
import numpy as np
import random as random


class CustomEnv(gym.Env):

    def __init__(self):
        # board position to set a cross (can be 0, 1, 2 in each dimension)
        self.action_space = spaces.MultiDiscrete([3, 3]) # wo wird das kreuz gesetzt?
        # board with circles and crosses  (can be 0, 1, 2 in each dimension)
        self.observation_space = spaces.MultiDiscrete([
            [3, 3, 3],
            [3, 3, 3],
            [3, 3, 3]])

        # board as state representation
        self.board = np.zeros((3, 3), dtype=np.int32)
        self.cross = 1
        self.circle = -1
        self.free = 0

    def reset(self):
        """
        Reset the board and return the board as state.
        return:
            board as state of the environment
        """
        self.board[:, :] = 0
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
        Select a random free position of the board.
        return:
            Random free board position as array and number of free
            positions
        """
        board_pos = np.array([random.randrange(3), random.randrange(3)])
        n_free_pos = 0
        return board_pos, n_free_pos

    def opponent_move(self):
        """
        Set a circle at a random free position of the board.
        return:
            True, if board is completely filled.
            False, otherwise.
        """
        return False

    def compute_reward(self, winner):
        """
        winner:
            The winner symbol (self.free, self.circle, self.cross)
        return:
            Reward != self.free if winner is circle or cross and if game is
            over.
            Done, if winner is != self.free
        """
        reward = 0
        done = False
        return reward, done

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
        reward = 0
        done = False
        # check if action is valid board position
        invalid_idxs = np.argwhere((action > 2) | (action < 0))
        if invalid_idxs.shape[0] > 0:
            # do not change board
            return self.board, reward, done, {}
        # check if valid board position is already set
        if self.board[action[0], action[1]] != self.free:
            # do not change board
            return self.board, reward, done, {}
        # apply cross to board
        self.board[action[0], action[1]] = self.cross
        # can a winner be determined?
        winner_symbol = self.check_winner()
        reward, done = self.compute_reward(winner_symbol)
        if done:
            return self.board, reward, done, {}
        # apply opponent move and check if a winner can be determind
        filled = self.opponent_move()
        winner_symbol = self.check_winner()
        reward, done = self.compute_reward(winner_symbol)
        # if we got a winner or if board is full -> game over
        done = done or filled
        return self.board, reward, done, {}

    # board wird gezeichnet
    def render(self, mode="human", close=False):
        print(self.board)
