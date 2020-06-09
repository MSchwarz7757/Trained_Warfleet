class Warships:

    def __init__(self, pos_bow, pos_stern, orientation, row_or_col, size):

        self.pos_bow = pos_bow
        self.pos_stern = pos_stern
        self.orientation = orientation
        self.row = row_or_col
        self.size = size

    def submarine(self, ship):
        if ship.pos_x and ship.pos_y >= 1 and ship.pos_y - ship.pos_x == 2:
            return self.pos_bow, self.pos_stern, self.orientation, self.row_or_col, self.size

    def get_position(self):
        return self.pos_bow, self.pos_stern, self.orientation, self.row_or_col

