from celestial_objects_plot import celestial_objects_plot
from matplotlib.backend_bases import MouseEvent
from matplotlib.image import AxesImage
from matplotlib.axes import Axes
from orbit_builder import orbit
from itertools import chain

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


def zoom_factory(ax: Axes, image_object: AxesImage, base_scale: float):
    def zoom(event: MouseEvent):
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
        target = celestial_objects_plot.get_target_body()
        if target != None:
            x_range = update_plot_axes(
                current_xlim, current_ylim, target.coordinate[0], target.coordinate[1], scale_factor, image_object)
        else:
            x_range = update_plot_axes(
                current_xlim, current_ylim, xdata, ydata, scale_factor, image_object)
        recreate_bbox_after_zoom()
        adjust_size_of_planets(x_range, base_scale)

    fig = ax.get_figure()
    fig.canvas.mpl_connect('scroll_event', zoom)


def pan_factory(ax: Axes):
    def onPress(event: MouseEvent):
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
            resize_bachground_image(target, cur_xrange, cur_yrange)
    fig = ax.get_figure()
    fig.canvas.mpl_connect('button_press_event', onPress)


def update(frame):

    list_of_plot_elements_to_return = []                               # Generic list
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

    handle_text_overlap(target)

    for index in range(len(list_of_final_coordinates)):
        list_of_plot_elements_to_return.append(
            list_of_celestial_object_plots[index].get_celestial_object_scatter_plot())
        list_of_plot_elements_to_return.append(
            list_of_celestial_object_plots[index].get_celestial_object_text())

    if target is not None:
        cur_xlim = ax.get_xlim()
        cur_ylim = ax.get_ylim()
        cur_xrange = (cur_xlim[1] - cur_xlim[0])*.5
        cur_yrange = (cur_ylim[1] - cur_ylim[0])*.5
        resize_bachground_image(target, cur_xrange, cur_yrange)

    return list_of_plot_elements_to_return


def resize_bachground_image(target, cur_xrange, cur_yrange):
    new_xlim = [target.coordinate[0] - cur_xrange,
                target.coordinate[0] + cur_xrange]
    new_ylim = [target.coordinate[1] - cur_yrange,
                target.coordinate[1] + cur_yrange]
    newlist = [new_xlim, new_ylim]
    image_object.set_extent(
        tuple(chain.from_iterable(newlist)))
    ax.set_xlim(new_xlim)
    ax.set_ylim(new_ylim)


def update_plot_axes(current_xlim, current_ylim, xdata, ydata, scale_factor, image_object: AxesImage):
    up_height = (current_ylim[1] - ydata)*scale_factor
    down_height = (ydata - current_ylim[0])*scale_factor
    right_width = (current_xlim[1] - xdata)*scale_factor
    left_width = (xdata - current_xlim[0])*scale_factor
    x_range = (current_xlim[1]-current_xlim[0])*scale_factor
    new_xlim = [xdata - left_width, xdata + right_width]
    new_ylim = [ydata - down_height, ydata + up_height]
    newlist = [new_xlim, new_ylim]
    image_object.set_extent(
        tuple(chain.from_iterable(newlist)))
    ax.set_xlim(new_xlim)
    ax.set_ylim(new_ylim)

    return x_range


def recreate_bbox_after_zoom():
    store_visibility: list[bool] = []
    for celestial_objects_plot_item in list_of_celestial_object_plots:
        store_visibility.append(
            celestial_objects_plot_item.get_celestial_object_text().get_visible())
        celestial_objects_plot_item.get_celestial_object_text().set(visible=True)
    for index in range(len(list_of_celestial_object_plots)):
        list_of_celestial_object_plots[index].recalculate_bounding_box()
        list_of_celestial_object_plots[index].get_celestial_object_text().set(
            visible=store_visibility[index])


def handle_text_overlap(target):
    overlapping_celestial_object_plots: set[celestial_objects_plot] = set()
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


def adjust_size_of_planets(x_range, base_scale):
    # Y = M*log(X)/log(base_scale) + C
    max = 100  # 10000
    min = 3  # 9
    slope = -2.00754523
    min_x_range = 6*10**8
    max_x_range = 6*10**10
    intercept = 525.7403356
    for celestial_objects_plot_item in list_of_celestial_object_plots:
        if x_range < min_x_range:
            new_radius = np.array([max], dtype=np.float64)
        elif min_x_range <= x_range <= max_x_range:
            new_radius = slope*np.log(x_range)/np.log(base_scale) + intercept
            new_radius = np.array([new_radius], dtype=np.float64)
        elif x_range > max_x_range:
            new_radius = np.array([min], dtype=np.float64)
        celestial_objects_plot_item.get_celestial_object_scatter_plot().set_sizes(new_radius**2)


if __name__ == '__main__':
    xmin = -6*10**11
    xmax = 6*10**11
    ymin = -6*10**11
    ymax = 6*10**11

    fig, ax = plt.subplots()

    img = plt.imread("background_image.png")
    image_object = ax.imshow(img, zorder=0, extent=[xmin,
                                                    xmax, ymin, ymax], aspect='auto')

    list_of_celestial_object_names = ["Sun", "Mercury", "Venus",
                                      "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]

    list_of_celestial_object_plots: list[celestial_objects_plot] = []

    for item in list_of_celestial_object_names:
        celestial_objects_plot_item = celestial_objects_plot(item, ax)
        list_of_celestial_object_plots.append(celestial_objects_plot_item)

    ax.set_aspect('auto')
    ax.axis('off')
    ax.set(xlim=[xmin, xmax], ylim=[ymin, ymax])
    scale = 1.1
    zoom_factory(ax, image_object, base_scale=scale)
    pan_factory(ax)

    ani = animation.FuncAnimation(fig=fig, frames=10, func=update, interval=30)
    plt.tight_layout()
    plt.show()
