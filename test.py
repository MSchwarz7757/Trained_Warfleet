from Gym_Exercise.gym_ttt.envs.Warships import Warships


submarine_1 = Warships(1, 1, 1, 2)
print(submarine_1.pos_x, submarine_1.pos_y, submarine_1.orientation, submarine_1.row)
print(submarine_1.get_position())
print("----------------------------")

submarine_2 = Warships(2, 1, 1, 2)
print(submarine_2.pos_x, submarine_2.pos_y, submarine_2.orientation, submarine_2.row)
print(submarine_2.get_position())
print("----------------------------")

