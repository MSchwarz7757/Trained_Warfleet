class Warships:

    """No separate constructors for ship types. Type is specified by size.
    Size is bound to bow and stern positions.
    """

    def __init__(self, pos_x, pos_y, orientation, row):

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.orientation = orientation
        self.row = row

    def two_space_ship(self,ship):
        if ship.pos_x and ship.pos_y >= 1:
            return self.pos_x, self.pos_y, self.orientation, self.row

    # ist das gewählte schiff ein richtiger shiffstyp?
    def ship_in_list(self):
        pass

    def get_position(self):
        return self.pos_x, self.pos_y, self.orientation, self.row

