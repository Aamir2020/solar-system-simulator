import numpy as np


class celestial_object():

    def __init__(self, name: str, coordinate: list, velocity: list, mass: float):
        self.coordinate = np.array(coordinate, dtype=np.float64)
        self.velocity = np.array(velocity, dtype=np.float64)
        self.mass = mass
        self.name = name

    def update_coordinate(self, coordinate: np.ndarray):
        self.coordinate = coordinate

    def update_velocity(self, velocity: np.ndarray):
        self.velocity = velocity
