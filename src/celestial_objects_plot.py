from ephemeris_request_handler import ephemeris_request_handler_impl
from celestial_object import celestial_object
from collections import deque


class celestial_objects_plot:

    max_positions = 50
    text_offset = 10**10

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

    def check_text_overlap(self, other_text):
        # TODO: Add dynamic text sizing here
        # Seems like text size is set in pixels, The text is drawn starting from the bottom left.
        # Find the figure's pixel to axis ratio.
        # approximate the pixel size for the default and use the above ratio to find the axis length
        # Use the axis lenght to draw an aproximate box around the text.
        # Iterate through each text to find outif there is an overlap
        # Rules: If either text1 or text2 are the target and they overlap
        #           make the target text visible and the other invisible
        #        If neither text1 or text2 are the target and they overlap name
        #           make both texts invisible
        #        If text1 and text2 don't overlap, make both visible
        width = self.ax.get_window_extent().width
        height = self.ax.get_window_extent().height

        current_xlim = self.ax.get_xlim()
        current_ylim = self.ax.get_ylim()

        width_ratio = current_xlim/width
        height_ratio = current_ylim/height

        default_text_size_In_Inches = 0.13
        width_of_box = default_text_size_In_Inches*width_ratio
        height_of_box = default_text_size_In_Inches*height_ratio
