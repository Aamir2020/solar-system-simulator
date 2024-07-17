import numpy as np


class celestial_object():

    def __init__(self, name, coordinate, velocity, mass):
        self.coordinate = np.array(coordinate, dtype=np.float64)
        self.velocity = np.array(velocity, dtype=np.float64)
        self.mass = float(mass)
        self.name = name

    def update_coordinate(self, coordinate):
        self.coordinate = coordinate

    def update_velocity(self, velocity):
        self.velocity = velocity
