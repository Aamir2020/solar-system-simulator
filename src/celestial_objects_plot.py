from ephemeris_request_handler import ephemeris_request_handler_impl
from celestial_object import celestial_object
from collections import deque


class celestial_objects_plot:

    max_positions = 50
    text_offset = 10**10
    target = None

    @classmethod
    def set_target_body_to_center(cls, celestial_object):
        cls.target = celestial_object

    @classmethod
    def get_target_body_to_center(cls):
        return cls.target

    def __init__(self, name, ax):
        self.name = name
        self.ax = ax
        coordinate, velocity, mass = ephemeris_request_handler_impl.send_request(
            name)
        self.celestial_object = celestial_object(
            name, coordinate, velocity, mass)
        self.celestial_object_scatter_plot = ax.scatter(
            self.celestial_object.coordinate[0], self.celestial_object.coordinate[1], c="b", s=20, marker='o')
        self.celestial_object_text = ax.text(
            self.celestial_object.coordinate[0], self.celestial_object.coordinate[1] + self.text_offset, name)
        self.celestial_object_trace, = ax.plot([], [], 'k-', lw=1)
        self.celestial_object_positions = deque(
            [self.celestial_object.coordinate], maxlen=self.max_positions)

    def set_plot_offsets(self, final_coordinate):
        self.celestial_object_scatter_plot.set_offsets(final_coordinate)

    def add_updated_position_for_tracing(self, final_coordinate):
        self.celestial_object_positions.append(final_coordinate)

    def set_trace_data(self):
        self.celestial_object_trace.set_data([coordinate[0] for coordinate in self.celestial_object_positions],
                                             [coordinate[1] for coordinate in self.celestial_object_positions])

    def update_text_position(self, final_coordinate):
        self.celestial_object_text.set_position(
            (final_coordinate[0], final_coordinate[1] + self.text_offset))

    def get_celestial_object(self):
        return self.celestial_object

    def get_celestial_object_scatter_plot(self):
        return self.celestial_object_scatter_plot

    def get_celestial_object_trace(self):
        return self.celestial_object_trace

    def get_celestial_object_text(self):
        return self.celestial_object_text

    def check_text_overlap(self, other_celestial_plot):
        other_text = other_celestial_plot.get_celestial_object_text()

        width_of_window_in_inches = self.ax.get_window_extent().width
        height_of_window_in_inches = self.ax.get_window_extent().height

        current_xlim = self.ax.get_xlim()
        current_ylim = self.ax.get_ylim()

        xrange_in_meter = current_xlim[1] - current_xlim[0]
        yrange_in_meter = current_ylim[1] - current_ylim[0]

        width_ratio = xrange_in_meter/width_of_window_in_inches
        height_ratio = yrange_in_meter/height_of_window_in_inches

        width_of_text_box_in_inches = self.celestial_object_text.get_window_extent().width
        height_of_text_box_in_inches = self.celestial_object_text.get_window_extent().height

        width_of_text_box = width_of_text_box_in_inches*width_ratio
        height_of_text_box = height_of_text_box_in_inches*height_ratio

        this_text_x_position, this_text_y_position = self.celestial_object_text.get_position()
        that_text_x_position, that_text_y_position = other_text.get_position()

        if self.target == self.celestial_object or self.target == other_celestial_plot.get_celestial_object():
            if (this_text_x_position + width_of_text_box < that_text_x_position) or (this_text_y_position + height_of_text_box < that_text_y_position):
                if self.target != self.celestial_object:
                    self.celestial_object_text.set(visible=False)
                else:
                    other_text.set(visible=False)
            else:
                self.celestial_object_text.set(visible=True)
                other_text.set(visible=True)
        else:
            if (this_text_x_position + width_of_text_box < that_text_x_position) or (this_text_y_position + height_of_text_box < that_text_y_position):
                self.celestial_object_text.set(visible=False)
                other_text.set(visible=False)
            else:
                self.celestial_object_text.set(visible=True)
                other_text.set(visible=True)
