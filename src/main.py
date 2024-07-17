from ephemeris_request_handler import ephemeris_request_handler_impl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
from celestial_object import celestial_object
from orbit_builder import orbit


def update(frame):
    global sun_positions, earth_positions, mars_positions

    list_of_final_coordinates = orbit.move_celestial_objects(
        [Sun, Mercury, Venus, Earth, Mars])

    scat_sun.set_offsets(list_of_final_coordinates[0])
    scat_mercury.set_offsets(list_of_final_coordinates[1])
    scat_venus.set_offsets(list_of_final_coordinates[2])
    scat_earth.set_offsets(list_of_final_coordinates[3])
    scat_mars.set_offsets(list_of_final_coordinates[4])

    mercury_positions.append(list_of_final_coordinates[1])
    venus_positions.append(list_of_final_coordinates[2])
    earth_positions.append(list_of_final_coordinates[3])
    mars_positions.append(list_of_final_coordinates[4])

    mercury_trace.set_data([coordinate[0] for coordinate in mercury_positions],
                           [coordinate[1] for coordinate in mercury_positions])
    venus_trace.set_data([coordinate[0] for coordinate in venus_positions],
                         [coordinate[1] for coordinate in venus_positions])
    earth_trace.set_data([coordinate[0] for coordinate in earth_positions],
                         [coordinate[1] for coordinate in earth_positions])
    mars_trace.set_data([coordinate[0] for coordinate in mars_positions],
                        [coordinate[1] for coordinate in mars_positions])

    sun_text.set_position(
        (list_of_final_coordinates[0][0] + text_offset, list_of_final_coordinates[0][1] + text_offset))
    mercury_text.set_position(
        (list_of_final_coordinates[1][0] + text_offset, list_of_final_coordinates[1][1] + text_offset))
    venus_text.set_position(
        (list_of_final_coordinates[2][0] + text_offset, list_of_final_coordinates[2][1] + text_offset))
    earth_text.set_position(
        (list_of_final_coordinates[3][0] + text_offset, list_of_final_coordinates[3][1] + text_offset))
    mars_text.set_position(
        (list_of_final_coordinates[4][0] + text_offset, list_of_final_coordinates[4][1] + text_offset))

    return scat_sun, scat_mercury, scat_venus, scat_earth, scat_mars, mercury_trace, venus_trace, earth_trace, mars_trace, sun_text, mercury_text, venus_text, earth_text, mars_text


if __name__ == '__main__':

    text_offset = 10**10

    coordinate, vector, mass = ephemeris_request_handler_impl.send_request(
        "Sun")
    Sun = celestial_object("Sun", coordinate, vector, mass)

    coordinate, vector, mass = ephemeris_request_handler_impl.send_request(
        "Mercury")
    Mercury = celestial_object("Mercury", coordinate, vector, mass)

    coordinate, vector, mass = ephemeris_request_handler_impl.send_request(
        "Venus")
    Venus = celestial_object("Venus", coordinate, vector, mass)

    coordinate, vector, mass = ephemeris_request_handler_impl.send_request(
        "Earth")
    Earth = celestial_object("Earth", coordinate, vector, mass)

    coordinate, vector, mass = ephemeris_request_handler_impl.send_request(
        "Mars")
    Mars = celestial_object("Mars", coordinate, vector, mass)

    fig, ax = plt.subplots()

    scat_sun = ax.scatter(
        Sun.coordinate[0], Sun.coordinate[1], c="#FFDD21", s=300, marker='o')
    scat_mercury = ax.scatter(
        Mercury.coordinate[0], Mercury.coordinate[1], c="b", s=20, marker='o')
    scat_venus = ax.scatter(
        Venus.coordinate[0], Venus.coordinate[1], c="b", s=20, marker='o')
    scat_earth = ax.scatter(
        Earth.coordinate[0], Earth.coordinate[1], c="b", s=20, marker='o')
    scat_mars = ax.scatter(
        Mars.coordinate[0], Mars.coordinate[1], c="b", s=20, marker='o')

    sun_text = ax.text(Sun.coordinate[0], Sun.coordinate[1], "Sun")
    mercury_text = ax.text(
        Mercury.coordinate[0] + text_offset, Mercury.coordinate[1] + text_offset, "Mercury")
    venus_text = ax.text(
        Venus.coordinate[0] + text_offset, Venus.coordinate[1] + text_offset, "Venus")
    earth_text = ax.text(
        Earth.coordinate[0] + text_offset, Earth.coordinate[1] + text_offset, "Earth")
    mars_text = ax.text(
        Mars.coordinate[0] + text_offset, Mars.coordinate[1] + text_offset, "Mars")

    mercury_trace, = ax.plot([], [], 'k-', lw=1)
    venus_trace, = ax.plot([], [], 'k-', lw=1)
    earth_trace, = ax.plot([], [], 'k-', lw=1)
    mars_trace, = ax.plot([], [], 'k-', lw=1)

    max_positions = 50
    mercury_positions = deque([Mercury.coordinate], maxlen=max_positions)
    venus_positions = deque([Venus.coordinate], maxlen=max_positions)
    earth_positions = deque([Earth.coordinate], maxlen=max_positions)
    mars_positions = deque([Mars.coordinate], maxlen=max_positions)

    ax.set(xlim=[-0.25*10**12, 0.25*10**12], ylim=[-0.25*10**12, 0.25*10**12],
           xlabel='x axis', ylabel='y axis')
    # ax.set_xscale('log')
    # ax.set_yscale('log')

    ani = animation.FuncAnimation(fig=fig, frames=10, func=update, interval=30)
    plt.show()
