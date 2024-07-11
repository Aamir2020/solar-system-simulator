
# F=G*m1*m2/r^2
# F=m*a
# s = vi*t + 1/2*a*t^2
import math
import time
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


class Orbit:

    # Gravitational Constant
    Gravitational_Constant = 1
    tick_rate = 15

    @classmethod
    def move_celestial_objects(cls, list_of_celestial_objects):
        list_of_final_velocities = []
        list_of_final_coordinates = []

        for body_one in list_of_celestial_objects:
            force = np.array([0, 0], dtype=np.float64)
            force_angle = 0
            for body_two in list_of_celestial_objects:
                if np.array_equal(body_one.coordinate, body_two.coordinate):
                    continue

                distance_squared = ((body_one.coordinate[0] - body_two.coordinate[0])**2 +
                                    (body_one.coordinate[1] - body_two.coordinate[1])**2)
                if distance_squared == 0:
                    continue

                magnitude_of_force = cls.Gravitational_Constant * \
                    body_one.mass*body_two.mass / distance_squared
                force_angle = math.atan2(
                    (body_two.coordinate[1] - body_one.coordinate[1]), (body_two.coordinate[0] - body_one.coordinate[0]))
                force[0] += magnitude_of_force*math.cos(force_angle)
                force[1] += magnitude_of_force*math.sin(force_angle)

            acceleration = force/body_one.mass

            list_of_final_coordinates.append(
                body_one.coordinate + body_one.velocity*cls.tick_rate + 0.5*(acceleration)*cls.tick_rate**2)

            list_of_final_velocities.append(
                body_one.velocity + acceleration*cls.tick_rate)

            # if body_one.name == "Earth":
            #     print(
            #         f"Distance={distance_squared:.3}, velocity = {self.velocity}, acceleration={acceleration}, ", end="")
            # if self.name == "Sun":
            #     print(f"Angle={force_angle*180/math.pi:.4}")

        for index in range(len(list_of_celestial_objects)):
            list_of_celestial_objects[index].update_velocity(
                list_of_final_velocities[index])
            list_of_celestial_objects[index].update_coordinate(
                list_of_final_coordinates[index])


if __name__ == '__main__':
    # This code won't run if this file is imported.
    Sun = celestial_object("Sun", [0, 0], [0, 0], 100)
    Earth = celestial_object("Earth", [100, 0], [0, 1], 1)

    while (True):
        Orbit.move_celestial_objects([Sun, Earth])
        time.sleep(0.01)
        print(f"Coordinate = {Earth.coordinate}  Velocity= {Earth.velocity}")
