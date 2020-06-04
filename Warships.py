class Warships:

    """No separate constructors for ship types. Type is specified by size.
    Size is bound to bow and stern positions.
    """
    def __init__(self, bow_pos_x, bow_pos_y, stern_pos_x, stern_pos_y):

        self.bow_pos_x = bow_pos_x
        self.bow_pos_y = bow_pos_y
        self.stern_pos_x = stern_pos_x
        self.stern_pos_y = stern_pos_y


    def place(self):
        if self.valid_oriantation():
            return self.bow_pos_x, self.bow_pos_y, self.stern_pos_x, self.stern_pos_y
        else:
            print("diagonal placement not allowed !")


    def valid_oriantation(self):
        if self.bow_pos_x != self.stern_pos_x and self.bow_pos_y != self.stern_pos_y:
            return False
        else:
            return True




