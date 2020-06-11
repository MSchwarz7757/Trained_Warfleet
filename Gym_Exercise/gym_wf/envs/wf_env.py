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
        self.start = True
        self.num_ship_agent = 0
        self.num_ship_enemy = 0

        self.test = 0
        #self.combat()

    def place_ships(self):

        small_ship = 4
        middle_ship = 2 +small_ship
        big_ship = 2 + middle_ship
        cruiser_ship = 2 + big_ship

        if self.num_ship_agent < small_ship:
            self.agent_placement(2, self.shiplist_agent)
        elif small_ship <= self.num_ship_agent < middle_ship:
            self.agent_placement(3, self.shiplist_agent)
        elif middle_ship <= self.num_ship_agent < big_ship:
            self.agent_placement(4, self.shiplist_agent)
        elif big_ship <= self.num_ship_agent < cruiser_ship:
            self.agent_placement(5, self.shiplist_agent)

        if self.num_ship_enemy < small_ship:
            self.enemy_placement(2, self.shiplist_enemy)
        elif small_ship <= self.num_ship_enemy < middle_ship:
            self.enemy_placement(3, self.shiplist_enemy)
        elif middle_ship <= self.num_ship_enemy < big_ship:
            self.enemy_placement(4, self.shiplist_enemy)
        elif big_ship <= self.num_ship_enemy < cruiser_ship:
            self.enemy_placement(5, self.shiplist_enemy)

    def enemy_placement(self, size, shiplist):
        r_pos_start = np.random.randint(0, 9)
        r_pos_end = r_pos_start + size-1
        r_orientation = np.random.randint(0, 2)
        r_row = np.random.randint(0, 9)

        ship = self.board.place_enemy_ship(r_pos_start, r_pos_end, r_orientation, r_row, size)
        if ship is not None:
            shiplist.insert(self.num_ship_enemy, ship)
            self.num_ship_enemy += 1

    def agent_placement(self, size, shiplist):
        r_pos_start = np.random.randint(0, 9)
        r_pos_end = r_pos_start + size - 1
        r_orientation = np.random.randint(0, 2)
        r_row = np.random.randint(0, 9)

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

    '''
    Problem bei check_hit ist, dass die Schiffsliste noch mit unsichtbaren schiffen gefüllt ist weil diese nicht korrekt positioniert werden.
    Auch weil das verschieben in Klasse Spielfeld die koordinaten verschiebt wenn die Schiffe zu nahe am Rand sind aber die Liste noch die alten koordinaten hat
    '''
    def check_hit(self, player, x, y):
        #Zug Agent
        if player == 0 and self.shiplist_enemy:
            for index in self.shiplist_enemy:
                #waagerecht
                if index.orientation == 0:
                    if index.row_or_col == y and index.pos_bow <= x <= index.pos_stern:
                        index.size -= 1
                        #print("Size: " + str(index.size))
                        #print("Spieler hat getroffen: {}/{}".format(x,y))
                        if index.size is 0:
                            self.shiplist_enemy.remove(index)
                            print("Schiff zerstört")
                        return True
                    else:
                        pass

                #senkrecht
                elif index.orientation == 1:
                    if index.row_or_col == x and index.pos_bow <= y <= index.pos_stern:
                        index.size -= 1
                        #print("Size: " + str(index.size))
                        #print("Spieler hat getroffen: {}/{}".format(x,y))
                        if index.size is 0:
                            self.shiplist_enemy.remove(index)
                            print("Schiff zerstört")
                        return True
                    else:
                        pass
            if index.size is 0:
                self.shiplist_enemy.remove(index)
                print("Schiff zerstört")

        # Zug Gegner
        if player == 1 and self.shiplist_agent:
            for index in self.shiplist_agent:
                # waagerecht
                if index.orientation == 0:
                    if index.row_or_col == y and index.pos_bow <= x <= index.pos_stern:
                        index.size -= 1
                        #print("Size: "+str(index.size))
                        #print("Computer hat getroffen {}/{}".format(x,y))
                        if index.size is 0:
                            self.shiplist_agent.remove(index)
                            print("Schiff zerstört")
                        return True
                    else:
                        pass

                # senkrecht
                elif index.orientation == 1:
                    if index.row_or_col == x and index.pos_bow <= y <= index.pos_stern:
                        index.size -= 1
                        #print("Size: "+str(index.size))
                        #print("Computer hat getroffen {}/{}".format(x,y))
                        if index.size is 0:
                            self.shiplist_agent.remove(index)
                            print("Schiff zerstört")
                        return True
                    else:
                        pass



    def check_winner(self):
        """
        Check shiplists after every hit.
        return:
            0 - no winner
            1 - current player is winner
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
        shot = self.check_shot_postion(r_shot_X, r_shot_Y)
        return shot

    def check_shot_postion(self, x, y):
        if x > 10 or x < 0 or y > 10 or y < 0:
            # chose new values
            x = np.random.randint(0, 10)
            y = np.random.randint(0, 10)
            return [x, y]
        else:
            return [x, y]

    def agent_move(self):
        """
        Set a circle at a random free position of the board.
        return:
            True, if board is completely filled.
            False, otherwise.
        """
        # just to get a neat output
        print("--------------------------------")
        r_shot_X = np.random.randint(0, 10)
        r_shot_X = int(input("X:"))
        r_shot_Y = np.random.randint(0, 10)
        r_shot_Y = int(input("Y:"))

        shot = self.check_shot_postion(r_shot_X, r_shot_Y)
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

        # Spielfeld aufbauen
        while self.start:
            # wenn alle Schiffe platziert wurden
            if self.num_ship_agent >= 10 and self.num_ship_enemy >= 10:
                if self.num_ship_agent == len(self.shiplist_agent):
                    self.start = False
            self.place_ships()
            self.board.draw_board()
        # abc = input("Klicke für jeden einzelnen Schritt")
        reward = 0
        done = False

        # Agent soll schießen
        shot = self.agent_move()
        # platziere denn Schuss auf dem Spielfeld und zeichne neu

        self.board.place_hit(action[0], action[1], self.board.agent_board)
        self.board.place_hit(shot[0], shot[1], self.board.enemy_board)
        self.board.draw_board()

        if self.check_hit(0, shot[0], shot[1]):
            reward += 1
        self.check_hit(1, action[0], action[1])
        if self.check_winner():
            done = True

        return self.board, reward, done, {}

    # board wird gezeichnet
    def render(self, mode="human", close=False):
        print(self.board)
