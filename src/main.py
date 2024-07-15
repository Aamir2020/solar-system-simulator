from EphemerisRequestHandler import Ephemeris_Request_Handler_Impl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
from CelestialObject import Celestial_object
from EulerIntegrationOrbit import Orbit


def update(frame):
    global sun_positions, earth_positions, mars_positions

    list_of_final_coordinates = Orbit.move_celestial_objects(
        [Sun, Earth, Mars])

    scat_sun.set_offsets(list_of_final_coordinates[0])
    scat_earth.set_offsets(list_of_final_coordinates[1])
    scat_mars.set_offsets(list_of_final_coordinates[2])

    sun_positions.append(list_of_final_coordinates[0])
    earth_positions.append(list_of_final_coordinates[1])
    mars_positions.append(list_of_final_coordinates[2])

    sun_trace.set_data([coordinate[0] for coordinate in sun_positions], [
                       coordinate[1] for coordinate in sun_positions])
    earth_trace.set_data([coordinate[0] for coordinate in earth_positions], [
                         coordinate[1] for coordinate in earth_positions])
    mars_trace.set_data([coordinate[0] for coordinate in mars_positions], [
                        coordinate[1] for coordinate in mars_positions])

    sun_text.set_position(
        (list_of_final_coordinates[0][0], list_of_final_coordinates[0][1]))
    earth_text.set_position(
        (list_of_final_coordinates[1][0], list_of_final_coordinates[1][1]))
    mars_text.set_position(
        (list_of_final_coordinates[2][0], list_of_final_coordinates[2][1]))

    return scat_sun, scat_earth, scat_mars, sun_trace, earth_trace, mars_trace, sun_text, earth_text, mars_text


if __name__ == '__main__':

    coordinate, vector, mass = Ephemeris_Request_Handler_Impl.send_request(
        "Sun")
    Sun = Celestial_object("Sun", coordinate, vector, mass)
    Earth = Celestial_object("Earth", [400, 0], [0, 1.5], 1)
    coordinate, vector, mass = Ephemeris_Request_Handler_Impl.send_request(
        "Mars")
    Mars = Celestial_object("Mars", coordinate, vector, mass)
    coordinate, vector, mass = Ephemeris_Request_Handler_Impl.send_request(
        "Earth")
    Earth = Celestial_object("Earth", coordinate, vector, mass)

    fig, ax = plt.subplots()

    scat_sun = ax.scatter(
        Sun.coordinate[0], Sun.coordinate[1], c="y", s=200, marker='o')
    scat_earth = ax.scatter(
        Earth.coordinate[0], Earth.coordinate[1], c="b", s=20, marker='o')
    scat_mars = ax.scatter(
        Mars.coordinate[0], Mars.coordinate[1], c="r", s=20, marker='o')

    sun_text = ax.text(Sun.coordinate[0], Sun.coordinate[1], "Sun")
    earth_text = ax.text(
        Earth.coordinate[0], Earth.coordinate[1], "Earth")
    mars_text = ax.text(Mars.coordinate[0],
                        Mars.coordinate[1], "Mars")

    sun_trace, = ax.plot([], [], 'y-', lw=1)
    earth_trace, = ax.plot([], [], 'b-', lw=1)
    mars_trace, = ax.plot([], [], 'r-', lw=1)

    max_positions = 100
    sun_positions = deque([Sun.coordinate], maxlen=max_positions)
    earth_positions = deque([Earth.coordinate], maxlen=max_positions)
    mars_positions = deque([Mars.coordinate], maxlen=max_positions)

    ax.set(xlim=[-1*10**12, 1*10**12], ylim=[-1*10**12, 1*10**12],
           xlabel='x axis', ylabel='y axis')
    # ax.set_xscale('log')
    # ax.set_yscale('log')

    ani = animation.FuncAnimation(fig=fig, func=update, interval=30)
    plt.show()
