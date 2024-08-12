from ephemeris_request_handler import ephemeris_request_handler_impl
from celestial_object import celestial_object
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from collections import deque
from matplotlib.patches import Rectangle


class celestial_objects_plot:

    max_positions = 50
    text_offset = 10**10
    target = None
    text_rect = None
    count = 1

    @classmethod
    def set_target_body_to_center(cls, celestial_object):
        cls.target = celestial_object

    @classmethod
    def get_target_body(cls):
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
        if self.count > 0:
            bbox = self.get_text_bbox()
            self.bbox_template = bounding_box_template(
                bbox.x0, bbox.x1, bbox.width, bbox.height)
            self.count -= 1
        self.celestial_object_text.set_position(
            (final_coordinate[0], final_coordinate[1] + self.text_offset))
        self.bbox_template.update_position(
            final_coordinate[0], final_coordinate[1] + self.text_offset)

    def get_celestial_object(self):
        return self.celestial_object

    def get_celestial_object_scatter_plot(self):
        return self.celestial_object_scatter_plot

    def get_celestial_object_trace(self):
        return self.celestial_object_trace

    def get_celestial_object_text(self):
        return self.celestial_object_text

    def get_text_bbox(self):
        renderer = self.ax.figure.canvas.get_renderer()
        bboxbase = self.celestial_object_text.get_window_extent(
            renderer=renderer)
        return bboxbase.transformed(self.ax.transData.inverted())

    def is_text_overlapping(self, other_celestial_plot):
        this_bbox = self.bbox_template
        other_bbox = other_celestial_plot.get_bbox_template()

        # Check if the bounding boxes overlap
        overlap = not (this_bbox.x0 > other_bbox.x1 or
                       this_bbox.x1 < other_bbox.x0 or
                       this_bbox.y0 > other_bbox.y1 or
                       this_bbox.y1 < other_bbox.y0)

        return overlap

    def update_text_boundary(self):
        if self.text_rect:
            self.text_rect.remove()  # Remove previous rectangle
        self.text_rect = Rectangle((self.bbox_template.x0, self.bbox_template.y0), self.bbox_template.width, self.bbox_template.height,
                                   linewidth=1, edgecolor='r', facecolor='none')
        self.ax.add_patch(self.text_rect)

    def get_bbox_template(self):
        return self.bbox_template


class bounding_box_template:
    def __init__(self, x, y, width, height):
        self.x0 = x
        self.x1 = x + width
        self.y0 = y
        self.y1 = y + height
        self.width = width
        self.height = height

    def update_position(self, x, y):
        self.x0 = x
        self.x1 = x + self.width
        self.y0 = y
        self.y1 = y + self.height
