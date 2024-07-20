from ephemeris_request_handler import ephemeris_request_handler_impl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
from celestial_object import celestial_object
from orbit_builder import orbit


def zoom_factory(ax, base_scale):
    def zoom(event):
        current_xlim = ax.get_xlim()
        current_ylim = ax.get_ylim()
        current_xrange = (current_xlim[1] - current_xlim[0])*.5
        current_yrange = (current_ylim[1] - current_ylim[0])*.5
        xdata = event.xdata
        ydata = event.ydata
        if event.button == 'up':
            scale_factor = 1/base_scale
        elif event.button == 'down':
            scale_factor = base_scale
        else:
            scale_factor = 1
        ax.set_xlim([xdata - current_xrange*scale_factor,
                     xdata + current_xrange*scale_factor])
        ax.set_ylim([ydata - current_yrange*scale_factor,
                     ydata + current_yrange*scale_factor])
        ax.figure.canvas.draw_idle()
    fig = ax.get_figure()
    fig.canvas.mpl_connect('scroll_event', zoom)
    return zoom


def update(frame):
    global sun_positions, earth_positions, mars_positions

    list_of_final_coordinates = orbit.move_celestial_objects(
        [Sun, Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune])

    scat_sun.set_offsets(list_of_final_coordinates[0])
    scat_mercury.set_offsets(list_of_final_coordinates[1])
    scat_venus.set_offsets(list_of_final_coordinates[2])
    scat_earth.set_offsets(list_of_final_coordinates[3])
    scat_mars.set_offsets(list_of_final_coordinates[4])
    scat_jupiter.set_offsets(list_of_final_coordinates[5])
    scat_saturn.set_offsets(list_of_final_coordinates[6])
    scat_uranus.set_offsets(list_of_final_coordinates[7])
    scat_neptune.set_offsets(list_of_final_coordinates[8])

    mercury_positions.append(list_of_final_coordinates[1])
    venus_positions.append(list_of_final_coordinates[2])
    earth_positions.append(list_of_final_coordinates[3])
    mars_positions.append(list_of_final_coordinates[4])
    jupiter_positions.append(list_of_final_coordinates[5])
    saturn_positions.append(list_of_final_coordinates[6])
    uranus_positions.append(list_of_final_coordinates[7])
    neptune_positions.append(list_of_final_coordinates[8])

    mercury_trace.set_data([coordinate[0] for coordinate in mercury_positions],
                           [coordinate[1] for coordinate in mercury_positions])
    venus_trace.set_data([coordinate[0] for coordinate in venus_positions],
                         [coordinate[1] for coordinate in venus_positions])
    earth_trace.set_data([coordinate[0] for coordinate in earth_positions],
                         [coordinate[1] for coordinate in earth_positions])
    mars_trace.set_data([coordinate[0] for coordinate in mars_positions],
                        [coordinate[1] for coordinate in mars_positions])
    jupiter_trace.set_data([coordinate[0] for coordinate in jupiter_positions],
                           [coordinate[1] for coordinate in jupiter_positions])
    saturn_trace.set_data([coordinate[0] for coordinate in saturn_positions],
                          [coordinate[1] for coordinate in saturn_positions])
    uranus_trace.set_data([coordinate[0] for coordinate in uranus_positions],
                          [coordinate[1] for coordinate in uranus_positions])
    neptune_trace.set_data([coordinate[0] for coordinate in neptune_positions],
                           [coordinate[1] for coordinate in neptune_positions])

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
    jupiter_text.set_position(
        (list_of_final_coordinates[5][0] + text_offset, list_of_final_coordinates[5][1] + text_offset))
    saturn_text.set_position(
        (list_of_final_coordinates[6][0] + text_offset, list_of_final_coordinates[6][1] + text_offset))
    uranus_text.set_position(
        (list_of_final_coordinates[7][0] + text_offset, list_of_final_coordinates[7][1] + text_offset))
    neptune_text.set_position(
        (list_of_final_coordinates[8][0] + text_offset, list_of_final_coordinates[8][1] + text_offset))

    return scat_sun, scat_mercury, scat_venus, scat_earth, scat_mars, scat_jupiter, scat_saturn, scat_uranus, scat_neptune, \
        mercury_trace, venus_trace, earth_trace, mars_trace, jupiter_trace, saturn_trace, uranus_trace, neptune_trace, \
        sun_text, mercury_text, venus_text, earth_text, mars_text, jupiter_text, saturn_text, uranus_text, neptune_text


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

    coordinate, vector, mass = ephemeris_request_handler_impl.send_request(
        "Jupiter")
    Jupiter = celestial_object("Jupiter", coordinate, vector, mass)

    coordinate, vector, mass = ephemeris_request_handler_impl.send_request(
        "Saturn")
    Saturn = celestial_object("Saturn", coordinate, vector, mass)

    coordinate, vector, mass = ephemeris_request_handler_impl.send_request(
        "Uranus")
    Uranus = celestial_object("Uranus", coordinate, vector, mass)

    coordinate, vector, mass = ephemeris_request_handler_impl.send_request(
        "Neptune")
    Neptune = celestial_object("Neptune", coordinate, vector, mass)

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
    scat_jupiter = ax.scatter(
        Jupiter.coordinate[0], Jupiter.coordinate[1], c="b", s=20, marker='o')
    scat_saturn = ax.scatter(
        Saturn.coordinate[0], Saturn.coordinate[1], c="b", s=20, marker='o')
    scat_uranus = ax.scatter(
        Uranus.coordinate[0], Uranus.coordinate[1], c="b", s=20, marker='o')
    scat_neptune = ax.scatter(
        Neptune.coordinate[0], Neptune.coordinate[1], c="b", s=20, marker='o')

    sun_text = ax.text(Sun.coordinate[0], Sun.coordinate[1], "Sun")
    mercury_text = ax.text(
        Mercury.coordinate[0] + text_offset, Mercury.coordinate[1] + text_offset, "Mercury")
    venus_text = ax.text(
        Venus.coordinate[0] + text_offset, Venus.coordinate[1] + text_offset, "Venus")
    earth_text = ax.text(
        Earth.coordinate[0] + text_offset, Earth.coordinate[1] + text_offset, "Earth")
    mars_text = ax.text(
        Mars.coordinate[0] + text_offset, Mars.coordinate[1] + text_offset, "Mars")
    jupiter_text = ax.text(
        Jupiter.coordinate[0] + text_offset, Jupiter.coordinate[1] + text_offset, "Jupiter")
    saturn_text = ax.text(
        Saturn.coordinate[0] + text_offset, Saturn.coordinate[1] + text_offset, "Saturn")
    uranus_text = ax.text(
        Uranus.coordinate[0] + text_offset, Uranus.coordinate[1] + text_offset, "Uranus")
    neptune_text = ax.text(
        Neptune.coordinate[0] + text_offset, Neptune.coordinate[1] + text_offset, "Neptune")

    mercury_trace, = ax.plot([], [], 'k-', lw=1)
    venus_trace, = ax.plot([], [], 'k-', lw=1)
    earth_trace, = ax.plot([], [], 'k-', lw=1)
    mars_trace, = ax.plot([], [], 'k-', lw=1)
    jupiter_trace, = ax.plot([], [], 'k-', lw=1)
    saturn_trace, = ax.plot([], [], 'k-', lw=1)
    uranus_trace, = ax.plot([], [], 'k-', lw=1)
    neptune_trace, = ax.plot([], [], 'k-', lw=1)

    max_positions = 50
    mercury_positions = deque([Mercury.coordinate], maxlen=max_positions)
    venus_positions = deque([Venus.coordinate], maxlen=max_positions)
    earth_positions = deque([Earth.coordinate], maxlen=max_positions)
    mars_positions = deque([Mars.coordinate], maxlen=max_positions)
    jupiter_positions = deque([Jupiter.coordinate], maxlen=max_positions)
    saturn_positions = deque([Saturn.coordinate], maxlen=max_positions)
    uranus_positions = deque([Uranus.coordinate], maxlen=max_positions)
    neptune_positions = deque([Neptune.coordinate], maxlen=max_positions)

    ax.set(xlim=[-6*10**12, 6*10**12], ylim=[-6*10**12, 6*10**12],
           xlabel='x axis', ylabel='y axis')
    # ax.set_xscale('log')
    # ax.set_yscale('log')
    scale = 1.1
    zoom_factory_return = zoom_factory(ax, base_scale=scale)

    ani = animation.FuncAnimation(fig=fig, frames=10, func=update, interval=30)
    plt.show()
