import math
import numpy as np


class orbit:

    # Gravitational Constant
    Gravitational_Constant = 6.67430*10**(-11)
    time_step = 24*60*60

    @classmethod
    def move_celestial_objects(cls, list_of_celestial_objects):
        list_of_final_velocities = []
        list_of_final_coordinates = []
        list_of_Intermediate_Orbital_State = []

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

            intermediate_coordinate = body_one.coordinate + body_one.velocity * \
                cls.time_step + 0.5*(acceleration)*cls.time_step**2

            intermediate_velocities = body_one.velocity + acceleration*cls.time_step

            list_of_Intermediate_Orbital_State.append(
                intermediate_orbital_state(intermediate_coordinate, body_one.coordinate, intermediate_velocities, body_one.velocity, force, body_one.mass))

        for body_one in list_of_Intermediate_Orbital_State:
            force = np.array([0, 0], dtype=np.float64)
            force_angle = 0
            for body_two in list_of_Intermediate_Orbital_State:
                if np.array_equal(body_one.intermediate_coordinate, body_two.intermediate_coordinate):
                    continue

                distance_squared = ((body_one.intermediate_coordinate[0] - body_two.intermediate_coordinate[0])**2 +
                                    (body_one.intermediate_coordinate[1] - body_two.intermediate_coordinate[1])**2)
                if distance_squared == 0:
                    continue

                magnitude_of_force = cls.Gravitational_Constant * \
                    body_one.mass*body_two.mass / distance_squared
                force_angle = math.atan2(
                    (body_two.intermediate_coordinate[1] - body_one.intermediate_coordinate[1]), (body_two.intermediate_coordinate[0] - body_one.intermediate_coordinate[0]))
                force[0] += magnitude_of_force*math.cos(force_angle)
                force[1] += magnitude_of_force*math.sin(force_angle)

            average_force = 0.5*(force + body_one.force)

            acceleration = average_force/body_one.mass

            list_of_final_coordinates.append(
                body_one.initial_coordinate + body_one.initial_velocity*cls.time_step + 0.5*(acceleration)*cls.time_step**2)

            list_of_final_velocities.append(
                body_one.initial_velocity + acceleration*cls.time_step)

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

        return list_of_final_coordinates


class intermediate_orbital_state:

    def __init__(self, intermediate_coordinate, initial_coordinate, intermediate_velocity, initial_velocity, force, mass):
        self.intermediate_coordinate = np.array(
            intermediate_coordinate, dtype=np.float64)
        self.initial_coordinate = np.array(
            initial_coordinate, dtype=np.float64)
        self.intermediate_velocity = np.array(
            intermediate_velocity, dtype=np.float64)
        self.initial_velocity = np.array(
            initial_velocity, dtype=np.float64)
        self.force = np.array(
            force, dtype=np.float64)
        self.mass = float(mass)
