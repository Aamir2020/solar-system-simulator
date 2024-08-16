from ephemeris_request_handler import ephemeris_request_handler_impl
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.collections import PathCollection
from matplotlib.collections import LineCollection
from celestial_object import celestial_object
from matplotlib.transforms import Bbox
from matplotlib.axes import Axes
from matplotlib.text import Text
from collections import deque

import numpy as np


class celestial_objects_plot:

    text_offset = 10**10
    target = None
    count = 1

    @classmethod
    def set_target_body_to_center(cls, celestial_object: celestial_object):
        cls.target = celestial_object

    @classmethod
    def get_target_body(cls) -> celestial_object:
        return cls.target

    def __init__(self, name: str, ax: Axes):
        self.name = name
        self.ax = ax
        coordinate, velocity, mass = ephemeris_request_handler_impl.send_request(
            name)
        self.celestial_object = celestial_object(
            name, coordinate, velocity, mass)

        self.celestial_object_scatter_plot = ax.scatter(
            self.celestial_object.coordinate[0], self.celestial_object.coordinate[1], c="w", s=5, marker='o')
        self.celestial_object_text = ax.text(
            self.celestial_object.coordinate[0], self.celestial_object.coordinate[1] + self.text_offset, name, c="w", clip_on=True)

        np_coordinate = np.array(coordinate, dtype=np.float64)
        distance = np.sqrt(np_coordinate.dot(np_coordinate))
        self.max_positions = int(distance/(2*10**9))
        if self.max_positions != 0:
            self.line_width = np.linspace(1, 2.23, self.max_positions-1)
        else:
            self.line_width = (0,)
        self.segments = []
        self.line_collection = LineCollection(
            self.segments, linewidths=self.line_width, color='white')
        self.ax.add_collection(self.line_collection)
        self.celestial_object_positions = deque(
            [self.celestial_object.coordinate], maxlen=self.max_positions)

    def set_plot_offsets(self, final_coordinate: np.ndarray):
        self.celestial_object_scatter_plot.set_offsets(final_coordinate)

    def add_updated_position_for_tracing(self, final_coordinate: np.ndarray):
        self.celestial_object_positions.append(final_coordinate)

    def set_trace_data(self):
        points = np.array(self.celestial_object_positions).reshape(-1, 1, 2)
        self.segments = np.concatenate([points[:-1], points[1:]], axis=1)
        self.line_collection.set_segments(self.segments)

    def update_text_position(self, final_coordinate: np.ndarray):
        if self.count > 0:
            self.recalculate_bounding_box()
            self.count -= 1
        self.celestial_object_text.set_position(
            (final_coordinate[0], final_coordinate[1] + self.text_offset))
        self.bbox_template.update_position(
            final_coordinate[0], final_coordinate[1] + self.text_offset)

    def recalculate_bounding_box(self):
        bbox = self.get_text_bbox()
        self.bbox_template = bounding_box_template(
            bbox.x0, bbox.x1, bbox.width, bbox.height)

    def get_celestial_object(self) -> celestial_object:
        return self.celestial_object

    def get_celestial_object_scatter_plot(self) -> PathCollection:
        return self.celestial_object_scatter_plot

    def get_celestial_object_text(self) -> Text:
        return self.celestial_object_text

    def get_text_bbox(self) -> Bbox:
        canvas: FigureCanvasAgg = self.ax.figure.canvas
        renderer = canvas.get_renderer()
        bboxbase = self.celestial_object_text.get_window_extent(
            renderer=renderer)
        return bboxbase.transformed(self.ax.transData.inverted())

    def is_text_overlapping(self, other_celestial_plot: 'celestial_objects_plot') -> bool:
        this_bbox = self.bbox_template
        other_bbox = other_celestial_plot.get_bbox_template()

        # Check if the bounding boxes overlap
        overlap = not (this_bbox.x0 > other_bbox.x1 or
                       this_bbox.x1 < other_bbox.x0 or
                       this_bbox.y0 > other_bbox.y1 or
                       this_bbox.y1 < other_bbox.y0)

        return overlap

    def get_bbox_template(self) -> 'bounding_box_template':
        return self.bbox_template


class bounding_box_template:
    def __init__(self, x: np.float64, y: np.float64, width: np.float64, height: np.float64):
        self.x0 = x
        self.x1 = x + width
        self.y0 = y
        self.y1 = y + height
        self.width = width
        self.height = height

    def update_position(self, x: np.float64, y: np.float64):
        self.x0 = x
        self.x1 = x + self.width
        self.y0 = y
        self.y1 = y + self.height
