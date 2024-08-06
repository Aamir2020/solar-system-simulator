from celestial_objects_plot import celestial_objects_plot
from orbit_builder import orbit
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


def zoom_factory(ax, base_scale):
    def zoom(event):
        current_xlim = ax.get_xlim()
        current_ylim = ax.get_ylim()
        xdata = event.xdata
        ydata = event.ydata
        if event.button == 'up':
            scale_factor = 1/base_scale
        elif event.button == 'down':
            scale_factor = base_scale
        else:
            scale_factor = 1
        up_height = (current_ylim[1] - ydata)*scale_factor
        down_height = (ydata - current_ylim[0])*scale_factor
        right_width = (current_xlim[1] - xdata)*scale_factor
        left_width = (xdata - current_xlim[0])*scale_factor
        ax.set_xlim([xdata - left_width,
                     xdata + right_width])
        ax.set_ylim([ydata - down_height,
                     ydata + up_height])
        ax.figure.canvas.draw_idle()
    fig = ax.get_figure()
    fig.canvas.mpl_connect('scroll_event', zoom)
    return zoom


def pan_factory(ax):
    def onPress(event):
        if event.inaxes != ax:
            return
        xdata = event.xdata
        ydata = event.ydata
        position = np.array([xdata, ydata], dtype=np.float64)
        list_of_bodies = [
            celestial_object_plot.get_celestial_object() for celestial_object_plot in list_of_celestial_object_plots]
        target_changed = False
        for object in list_of_bodies:
            if abs(position[0]-object.coordinate[0]) < 0.1 * 10**11 and abs(position[0]-object.coordinate[0]) < 0.1 * 10**11:
                celestial_objects_plot.set_target_body_to_center(object)
                target_changed = True

        if target_changed is False:
            celestial_objects_plot.set_target_body_to_center(None)
        else:
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()
            cur_xrange = (cur_xlim[1] - cur_xlim[0])*.5
            cur_yrange = (cur_ylim[1] - cur_ylim[0])*.5
            target = celestial_objects_plot.get_target_body_to_center()
            ax.set_xlim([target.coordinate[0] - cur_xrange,
                        target.coordinate[0] + cur_xrange])
            ax.set_ylim([target.coordinate[1] - cur_yrange,
                        target.coordinate[1] + cur_yrange])
    fig = ax.get_figure()
    fig.canvas.mpl_connect('button_press_event', onPress)
    return onPress


def update(frame):

    list_of_plot_elements_to_return = []
    list_of_final_coordinates = orbit.move_celestial_objects(
        [celestial_object_plot.get_celestial_object() for celestial_object_plot in list_of_celestial_object_plots])

    for index in range(len(list_of_final_coordinates)):
        list_of_celestial_object_plots[index].set_plot_offsets(
            list_of_final_coordinates[index])
        list_of_celestial_object_plots[index].add_updated_position_for_tracing(
            list_of_final_coordinates[index])
        list_of_celestial_object_plots[index].set_trace_data()
        list_of_celestial_object_plots[index].update_text_position(
            list_of_final_coordinates[index])
        list_of_plot_elements_to_return.append(
            list_of_celestial_object_plots[index].get_celestial_object_scatter_plot())
        list_of_plot_elements_to_return.append(
            list_of_celestial_object_plots[index].get_celestial_object_trace())
        list_of_plot_elements_to_return.append(
            list_of_celestial_object_plots[index].get_celestial_object_text())

    for body_one in list_of_celestial_object_plots:
        for body_two in list_of_celestial_object_plots:
            if body_one == body_two:
                continue
            body_one.check_text_overlap(body_two)

    target = celestial_objects_plot.get_target_body_to_center()
    if target is not None:
        cur_xlim = ax.get_xlim()
        cur_ylim = ax.get_ylim()
        cur_xrange = (cur_xlim[1] - cur_xlim[0])*.5
        cur_yrange = (cur_ylim[1] - cur_ylim[0])*.5
        ax.set_xlim([target.coordinate[0] - cur_xrange,
                    target.coordinate[0] + cur_xrange])
        ax.set_ylim([target.coordinate[1] - cur_yrange,
                    target.coordinate[1] + cur_yrange])

    return list_of_plot_elements_to_return


if __name__ == '__main__':

    fig, ax = plt.subplots()

    list_of_celestial_object_names = ["Sun", "Mercury", "Venus",
                                      "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]

    list_of_celestial_object_plots = []

    for item in list_of_celestial_object_names:
        list_of_celestial_object_plots.append(celestial_objects_plot(item, ax))

    ax.set(xlim=[-6*10**11, 6*10**11], ylim=[-6*10**11, 6*10**11],
           xlabel='x axis', ylabel='y axis')
    scale = 1.1
    zoom_factory_return = zoom_factory(ax, base_scale=scale)
    pan_factory_return = pan_factory(ax)

    ani = animation.FuncAnimation(fig=fig, frames=10, func=update, interval=30)
    plt.show()
