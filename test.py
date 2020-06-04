from Warships import Warships


submarine_1 = Warships(1, 1, 1, 2)
print(submarine_1.bow_pos_x, submarine_1.bow_pos_y, submarine_1.stern_pos_x, submarine_1.stern_pos_y)
print(submarine_1.place())
print("----------------------------")

submarine_2 = Warships(2, 1, 1, 2)
print(submarine_2.bow_pos_x, submarine_2.bow_pos_y, submarine_2.stern_pos_x, submarine_2.stern_pos_y)
print(submarine_2.place())
print("----------------------------")

