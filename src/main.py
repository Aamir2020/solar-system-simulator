
# F=G*m1*m2/r^2
# F=m*a
# s = vi*t + 1/2*a*t^2
import math
import time
import numpy as np


class celestial_object():
    # Gravitational Constant
    Gravitational_Constant = 1
    tick_rate = 0.01

    def __init__(self, name, coordinate, initial_velocity, mass_of_object):
        self.coordinate = np.array(coordinate, dtype=np.float64)
        self.initial_velocity = np.array(initial_velocity, dtype=np.float64)
        self.mass_of_object = float(mass_of_object)
        self.name = name

    def advance_to_next_position(self, list_of_celestial_objects):
        force = np.array([0, 0], dtype=np.float64)
        force_angle = 0
        for body in list_of_celestial_objects:
            if np.array_equal(self.coordinate, body.coordinate):
                continue

            distance_squared = ((self.coordinate[0] - body.coordinate[0])**2 +
                                (self.coordinate[1] - body.coordinate[1])**2)
            if distance_squared == 0:
                continue

            magnitude_of_force = self.Gravitational_Constant * \
                self.mass_of_object*body.mass_of_object / distance_squared
            force_angle = math.atan2(
                (body.coordinate[1] - self.coordinate[1]), (body.coordinate[0] - self.coordinate[0]))
            force[0] += magnitude_of_force*math.cos(force_angle)
            force[1] += magnitude_of_force*math.sin(force_angle)

        acceleration = force/self.mass_of_object

        self.coordinate += self.initial_velocity * \
            self.tick_rate + 0.5*(acceleration)*self.tick_rate**2

        self.initial_velocity += acceleration*self.tick_rate

        if self.name == "Earth":
            print(
                f"Distance={distance_squared:.3}, velocity = {self.initial_velocity}, acceleration={acceleration}, ", end="")
        if self.name == "Sun":
            print(f"Angle={force_angle*180/math.pi:.4}")


if __name__ == '__main__':
    # This code won't run if this file is imported.
    Sun = celestial_object("Sun", [0, 0], [0, 0], 100)
    Earth = celestial_object("Earth", [100, 0], [0, 1], 1)

    while (True):
        Sun.advance_to_next_position([Earth])
        Earth.advance_to_next_position([Sun])
        # time.sleep(0.01)
