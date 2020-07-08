class Warships:

    """
    This class represents ships.
    The generated Objects contain all attributes of a ship.
    """
    small_ship = 2
    middle_ship = 2
    big_ship = 2
    cruiser_ship = 2

    def __init__(self, pos_bow, pos_stern, orientation, row_or_col, size):

        self.pos_bow = pos_bow
        self.pos_stern = pos_stern
        self.orientation = orientation
        self.row_or_col = row_or_col
        self.size = size

    @classmethod
    def check_size(cls, size):
        """
        Defines the symbol inside the console for the ship based on the ship size.
        """
        if size == 2:
            return Warships.small_ship
        if size == 3:
            return Warships.middle_ship
        if size == 4:
            return Warships.big_ship
        if size == 5:
            return Warships.cruiser_ship


