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
        store_visibility = []
        for celestial_objects_plot_item in list_of_celestial_object_plots:
            store_visibility.append(
                celestial_objects_plot_item.get_celestial_object_text().get_visible())
            celestial_objects_plot_item.get_celestial_object_text().set(visible=True)
        for index in range(len(list_of_celestial_object_plots)):
            list_of_celestial_object_plots[index].recalculate_bounding_box()
            list_of_celestial_object_plots[index].get_celestial_object_text().set(
                visible=store_visibility[index])

    fig = ax.get_figure()
    fig.canvas.mpl_connect('scroll_event', zoom)


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
            if abs(position[0]-object.coordinate[0]) < 1 * 10**10 and abs(position[0]-object.coordinate[0]) < 1 * 10**10:
                celestial_objects_plot.set_target_body_to_center(object)
                target_changed = True

        if target_changed is False:
            celestial_objects_plot.set_target_body_to_center(None)
        else:
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()
            cur_xrange = (cur_xlim[1] - cur_xlim[0])*.5
            cur_yrange = (cur_ylim[1] - cur_ylim[0])*.5
            target = celestial_objects_plot.get_target_body()
            ax.set_xlim([target.coordinate[0] - cur_xrange,
                        target.coordinate[0] + cur_xrange])
            ax.set_ylim([target.coordinate[1] - cur_yrange,
                        target.coordinate[1] + cur_yrange])
    fig = ax.get_figure()
    fig.canvas.mpl_connect('button_press_event', onPress)


def update(frame):

    list_of_plot_elements_to_return = []
    list_of_final_coordinates = orbit.move_celestial_objects(
        [celestial_object_plot.get_celestial_object() for celestial_object_plot in list_of_celestial_object_plots])
    target = celestial_objects_plot.get_target_body()

    for index in range(len(list_of_final_coordinates)):
        list_of_celestial_object_plots[index].set_plot_offsets(
            list_of_final_coordinates[index])
        list_of_celestial_object_plots[index].add_updated_position_for_tracing(
            list_of_final_coordinates[index])
        list_of_celestial_object_plots[index].set_trace_data()
        list_of_celestial_object_plots[index].update_text_position(
            list_of_final_coordinates[index])

    text_overlap(target)

    for index in range(len(list_of_final_coordinates)):
        list_of_plot_elements_to_return.append(
            list_of_celestial_object_plots[index].get_celestial_object_scatter_plot())
        list_of_plot_elements_to_return.append(
            list_of_celestial_object_plots[index].get_celestial_object_trace())
        list_of_plot_elements_to_return.append(
            list_of_celestial_object_plots[index].get_celestial_object_text())

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


def text_overlap(target):
    overlapping_celestial_object_plots = set()
    for body_one_plot in list_of_celestial_object_plots:
        for body_two_plot in list_of_celestial_object_plots[list_of_celestial_object_plots.index(body_one_plot):]:
            if body_one_plot == body_two_plot:
                continue
            if body_one_plot.is_text_overlapping(body_two_plot) is True:
                overlapping_celestial_object_plots.add(body_one_plot)
                overlapping_celestial_object_plots.add(body_two_plot)
                break

    for body_plot in overlapping_celestial_object_plots:
        if target == body_plot.get_celestial_object():
            body_plot.get_celestial_object_text().set(visible=True)
        else:
            body_plot.get_celestial_object_text().set(visible=False)

    non_overlapping_celestial_object_plots = [e for e in list_of_celestial_object_plots if (
        e not in overlapping_celestial_object_plots)]

    for body_plot in non_overlapping_celestial_object_plots:
        body_plot.get_celestial_object_text().set(visible=True)


if __name__ == '__main__':

    fig, ax = plt.subplots()

    list_of_celestial_object_names = ["Sun", "Mercury", "Venus",
                                      "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]

    list_of_celestial_object_plots = []

    for item in list_of_celestial_object_names:
        celestial_objects_plot_item = celestial_objects_plot(item, ax)
        list_of_celestial_object_plots.append(celestial_objects_plot_item)

    ax.set(xlim=[-6*10**11, 6*10**11], ylim=[-6*10**11, 6*10**11],
           xlabel='x axis', ylabel='y axis')
    scale = 1.1
    zoom_factory(ax, base_scale=scale)
    pan_factory(ax)

    ani = animation.FuncAnimation(fig=fig, frames=10, func=update, interval=30)
    plt.show()
