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
        list_of_half_step_velocities = []
        list_of_first_step_orbital_elements = []
        list_of_second_step_accelerations = []

        # Finds half step velocity and full step orbital elements
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

            first_step_acceleration = force/body_one.mass
            first_step_velocity = body_one.coordinate + body_one.velocity * \
                cls.time_step + 0.5*(first_step_acceleration)*cls.time_step**2
            first_step_position = body_one.coordinate + body_one.velocity * \
                cls.time_step + 0.5*(first_step_acceleration)*cls.time_step**2

            half_step_velocity = body_one.velocity + \
                first_step_acceleration*cls.time_step/2

            list_of_half_step_velocities.append(half_step_velocity)
            list_of_first_step_orbital_elements.append(
                intermediate_orbital_state(first_step_position, first_step_velocity))

        # Finds acceleration for second step
        for body_one_index in range(len(list_of_first_step_orbital_elements)):
            force = np.array([0, 0], dtype=np.float64)
            force_angle = 0
            for body_two_index in range(len(list_of_first_step_orbital_elements)):
                if np.array_equal(list_of_first_step_orbital_elements[body_one_index].intermediate_coordinate, list_of_first_step_orbital_elements[body_two_index].intermediate_coordinate):
                    continue

                distance_squared = ((list_of_first_step_orbital_elements[body_one_index].intermediate_coordinate[0] - list_of_first_step_orbital_elements[body_two_index].intermediate_coordinate[0])**2 +
                                    (list_of_first_step_orbital_elements[body_one_index].intermediate_coordinate[1] - list_of_first_step_orbital_elements[body_two_index].intermediate_coordinate[1])**2)
                if distance_squared == 0:
                    continue

                magnitude_of_force = cls.Gravitational_Constant * \
                    list_of_celestial_objects[body_one_index].mass * \
                    list_of_celestial_objects[body_two_index].mass / \
                    distance_squared
                force_angle = math.atan2(
                    (list_of_first_step_orbital_elements[body_two_index].intermediate_coordinate[1] - list_of_first_step_orbital_elements[body_one_index].intermediate_coordinate[1]), (list_of_first_step_orbital_elements[body_two_index].intermediate_coordinate[0] - list_of_first_step_orbital_elements[body_one_index].intermediate_coordinate[0]))
                force[0] += magnitude_of_force*math.cos(force_angle)
                force[1] += magnitude_of_force*math.sin(force_angle)

            second_step_acceleration = force / \
                list_of_celestial_objects[body_one_index].mass
            list_of_second_step_accelerations.append(second_step_acceleration)

        # Combines all the results for implementing 'kick-drift-kick' form
        for body_one_index in range(len(list_of_celestial_objects)):

            first_step_position = list_of_celestial_objects[body_one_index].coordinate + \
                list_of_half_step_velocities[body_one_index]*cls.time_step
            first_step_velocity = list_of_half_step_velocities[body_one_index] + \
                list_of_second_step_accelerations[body_one_index] * \
                cls.time_step/2

            list_of_final_coordinates.append(first_step_position)
            list_of_final_velocities.append(first_step_velocity)

        for index in range(len(list_of_celestial_objects)):
            list_of_celestial_objects[index].update_velocity(
                list_of_final_velocities[index])
            list_of_celestial_objects[index].update_coordinate(
                list_of_final_coordinates[index])

        return list_of_final_coordinates


class intermediate_orbital_state:

    def __init__(self, intermediate_coordinate, intermediate_velocity):
        self.intermediate_coordinate = np.array(
            intermediate_coordinate, dtype=np.float64)
        self.intermediate_velocity = np.array(
            intermediate_velocity, dtype=np.float64)
