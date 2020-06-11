class Warships:

    small_ship = "S"
    middle_ship = "M"
    big_ship = "B"
    cruiser_ship = "C"

    def __init__(self, pos_bow, pos_stern, orientation, row_or_col, size):

        self.pos_bow = pos_bow
        self.pos_stern = pos_stern
        self.orientation = orientation
        self.row_or_col = row_or_col
        self.size = size

    @classmethod
    def check_size(cls, size):
        """
        defines the symbol for the ship
        """
        if size == 2:
            return Warships.small_ship
        if size == 3:
            return Warships.middle_ship
        if size == 4:
            return Warships.big_ship
        if size == 5:
            return Warships.cruiser_ship

    def submarine(self, ship):
        if ship.pos_x and ship.pos_y >= 1 and ship.pos_y - ship.pos_x == 2:
            return self.pos_bow, self.pos_stern, self.orientation, self.row_or_col, self.size

    def get_position(self):
        return self.pos_bow, self.pos_stern, self.orientation, self.row_or_col

